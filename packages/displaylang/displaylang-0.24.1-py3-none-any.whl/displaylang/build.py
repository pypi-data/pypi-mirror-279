# --------------------------------------------------------------------------- #
#   DisplayLang                                                               #
#                                                                             #
#   Copyright (c) 2020-2024 DisplayLang Contributors                          #
#                                                                             #
#   Licensed under the Apache License, Version 2.0 (the "License");           #
#   you may not use this file except in compliance with the License.          #
#   You may obtain a copy of the License at                                   #
#                                                                             #
#       http://www.apache.org/licenses/LICENSE-2.0                            #
#                                                                             #
#   Unless required by applicable law or agreed to in writing, software       #
#   distributed under the License is distributed on an "AS IS" BASIS,         #
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.  #
#   See the License for the specific language governing permissions and       #
#   limitations under the License.                                            #
# --------------------------------------------------------------------------- #


"""
Build HTML, by evaluating DisplayLang.
"""

import ast
import copy

from .builtins import (
    basic_callables as builtin_basic_callables,
    other_callables as builtin_other_callables,
)
from .depth import check_displaylang_dims
from .evaluate import ExpressionEvaluator, reject, NestedCodeBlockProcessor
from .exceptions import ControlledEvaluationException


FSTRING_CONVERSION_CODES = {
    115: "!s", 114: "!r", 97: "!a"
}


class Assignment:

    def __init__(self, target, value):
        self.target = target
        self.value = value


class DisplayLangEvaluator(ExpressionEvaluator):
    """
    The NodeTransformer class for evaluating DisplayLang.
    """

    def add_current_name(self, name, value):
        """
        Use this to record names that have been defined during a current
        parsing process, e.g. 'x' if a previous line made the
        assignment 'x = Symbol("x")'.
        """
        self.local_vars[name] = value

    ###########################################################################
    # While our `generic_visit()` method provides a catch-all for node types we
    # simply have not thought about, here we define visitors for node types we
    # definitely want to reject.

    def visit_Import(self, node):
        reject('Import statements are not allowed.', node)

    def visit_ImportFrom(self, node):
        reject('Import statements are not allowed.', node)

    ###########################################################################
    # Supported statement types.
    # (ast.Expr is already supported in our subclass.)

    def visit_Assign(self, node, use_prebuilt_value=False, prebuilt_value=None):
        """
        Handle any type of assignment, including multiple and unpacking.
        Each assignment is recorded as a local var, available for subsequent
        statements.
        Return list of `Assignment` instances.

        The kwargs concerning "prebuilt values" help us re-use this method in
        places like our `visit_For` method. The reason we need a separate `user_prebuilt_value`
        kwarg is because we can't rely on truthiness of the `prebuilt_value` kwarg to tell
        us whether we want to use it; the desired value could be e.g. False, None, etc.
        """
        built_value = prebuilt_value if use_prebuilt_value else self.visit(node.value)
        assignments = []
        for target in node.targets:
            addresses = self.unpack_assignment_target(target, node)
            for target_name, address in addresses.items():
                v = built_value
                for i in address:
                    try:
                        v = v[i]
                    except (IndexError, TypeError):
                        msg = 'Cannot unpack assignment.'
                        reject(msg, node)
                self.add_current_name(target_name, v)
                a = Assignment(target_name, v)
                assignments.append(a)
        return assignments

    def unpack_assignment_target(self, target, node=None):
        """
        Recursively explore the structure of an assignment target, determining
        the addresses of all the names found therein.

        :param target: one of the targets of an ast.Assign. Should be either
            an ast.Tuple, ast.List, or ast.Name.
        :param node: you can pass the ast.Assign node where the target comes
            from, to get better error messages.
        :return: dict giving the addresses of the names in the target.
            Keys are names (strings), and values are their "addresses" i.e.
            tuples of indices.
            If the target is just a single ast.Name, then its address will be
            an empty tuple.
        """
        if isinstance(target, (ast.List, ast.Tuple)):
            addresses = {}
            for i, elt in enumerate(target.elts):
                a = self.unpack_assignment_target(elt, node)
                for name, address in a.items():
                    addresses[name] = (i,) + address
            return addresses
        elif isinstance(target, ast.Name):
            return {target.id: ()}
        else:
            msg = 'Assignment targets may be only lists, tuples, or names.'
            reject(msg, node=node)

    def visit_AugAssign(self, node):
        """
        Handle an augmented assignment, and record the updated value as a
        local var.
        """
        target_name = node.target.id
        self.recurse(node)
        built_value = node.op(node.target, node.value)
        self.add_current_name(target_name, built_value)
        return Assignment(target_name, built_value)

    def visit_Return(self, node):
        """
        This is meant to work with the `DisplayLangProcessor.process()` method,
        which expects a whole ast.Return node.
        """
        self.recurse(node)
        return node

    ###########################################################################
    # Comprehensions

    def handle_comprehension(self, node):
        """
        Handles any of the four types of comprehensions: List, Set, Dict, and
        GeneratorExp.

        Always returns a list. It is up to the caller to convert this into the
        required form.
        """
        gens = node.generators
        if len(gens) != 1:
            reject('Currently only comprehensions with exactly one generator are supported.', node)
        gen = gens[0]
        tgt = gen.target

        names = []
        if isinstance(tgt, ast.Name):
            names.append(tgt.id)
        elif isinstance(tgt, ast.Tuple):
            if not all(isinstance(elt, ast.Name) for elt in tgt.elts):
                reject('Target in comprehension must be name or tuple of names.', tgt)
            names = [elt.id for elt in tgt.elts]
        else:
            reject('Target in comprehension must be name or tuple of names.', tgt)

        # Save any existing values for the bound names:
        prev_bound_values = {}
        for name in names:
            if name in self.bound_vars:
                prev_bound_values[name] = self.bound_vars[name]

        L = []
        n = len(names)
        if n == 0:
            reject('Need at least one name.', node=gen)
        it = self.visit(gen.iter)

        ifs = gen.ifs

        is_dict_comp = isinstance(node, ast.DictComp)
        if is_dict_comp:
            key_form = node.key
            value_form = node.value
        else:
            elt = node.elt

        for values in it:
            if n == 1:
                self.bound_vars[names[0]] = values
            else:
                if len(values) != n:
                    reject('Wrong number of values in comprehension.', node=gen)
                for name, value in zip(names, values):
                    self.bound_vars[name] = value

            next_ifs = [self.visit(i) for i in copy.deepcopy(ifs)]

            if all(c for c in next_ifs):
                if is_dict_comp:
                    next_key = self.visit(copy.deepcopy(key_form))
                    next_value = self.visit(copy.deepcopy(value_form))
                    L.append((next_key, next_value))
                else:
                    next_elt = self.visit(copy.deepcopy(elt))
                    L.append(next_elt)

        # Restore previous values / clean up:
        for name in names:
            if name in prev_bound_values:
                self.bound_vars[name] = prev_bound_values[name]
            elif name in self.bound_vars:
                del self.bound_vars[name]

        return L

    def visit_ListComp(self, node):
        return self.handle_comprehension(node)

    def visit_SetComp(self, node):
        return set(self.handle_comprehension(node))

    def visit_GeneratorExp(self, node):
        return tuple(self.handle_comprehension(node))

    def visit_DictComp(self, node):
        return {k: v for k, v in self.handle_comprehension(node)}

    ###########################################################################

    def visit_IfExp(self, node):
        self.recurse(node)
        return node.body if node.test else node.orelse

    def visit_JoinedStr(self, node):
        s = ''
        for v in node.values:
            if isinstance(v, ast.Constant):
                s += v.value
            elif isinstance(v, ast.FormattedValue):
                val = self.visit(v.value)
                t = "{" + FSTRING_CONVERSION_CODES.get(v.conversion, '')
                if v.format_spec:
                    # For now we only support the case of a single Constant:
                    fsv = v.format_spec.values
                    if len(fsv) == 1 and isinstance(fsv[0], ast.Constant):
                        t += ":" + fsv[0].value
                t += "}"
                s += t.format(val)
        return s

    ###########################################################################

    def visit_Break(self, node):
        raise DisplayLangBreakException

    def visit_Continue(self, node):
        raise DisplayLangContinueException

    def visit_FunctionDef(self, node):
        self.recurse(node, fields=['args'])
        p = DisplayLangNestedCodeBlockProcessor(self, node.body,
                                                signature=node.args, return_just_value=True)
        name = node.name
        self.add_current_name(node.name, p)
        return Assignment(name, p)

    def visit_Lambda(self, node):
        self.recurse(node, fields=['args'])
        code = [ast.Return(node.body)]
        p = DisplayLangNestedCodeBlockProcessor(self, code,
                                                signature=node.args, return_just_value=True)
        return p

    def visit_arguments(self, node):
        self.recurse(node)
        return node

    def visit_arg(self, node):
        return node.arg

    def visit_For(self, node):
        self.recurse(node, fields=['iter'])
        p = DisplayLangNestedCodeBlockProcessor(self, node.body)
        for value in node.iter:
            asgn = ast.Assign([node.target], value)
            self.visit_Assign(asgn, use_prebuilt_value=True, prebuilt_value=value)
            try:
                p()
            except DisplayLangBreakException:
                break
            except DisplayLangContinueException:
                continue
        else:
            if node.orelse:
                p = DisplayLangNestedCodeBlockProcessor(self, node.orelse)
                p()

    def visit_If(self, node):
        self.recurse(node, fields=['test'])
        code = node.body if node.test else node.orelse
        p = DisplayLangNestedCodeBlockProcessor(self, code)
        r, _ = p()
        # Not sure there's actually any need to return anything here...
        return r


class DisplayLangNestedCodeBlockProcessor(NestedCodeBlockProcessor):
    """
    Forms an object which can be invoked (called) in order to evaluate a nested code
    block, as found in function definitions, and control structures like for-loops
    and if-else structures.

    May be invoked multiple times, since only a *deep copy* of the nested code block
    is ever processed and transformed by the evaluation process.
    """

    def __init__(self, evaluator, body, signature=None, return_just_value=False):
        """
        :param evaluator: the DisplayLangEvaluator that wants to process a nested
            code block.
        :param body: list of ast statement nodes, representing the block of code
            to be processed.
        :param signature: optional `ast.arguments` node, representing expected
            arguments that can be passed into the evaluation.
        """
        NestedCodeBlockProcessor.__init__(self, evaluator)
        self.body = body
        self.signature = signature
        self.return_just_value = return_just_value

    def receive_args(self, *args, **kwargs):
        """
        Our job is to interpret the passed args and kwargs according to `self.signature`
        (which is an ast.arguments in which all of the subfields have been evaluated
        already), and then store the results as local vars in `self.evaluator`.

        FOR NOW: We are only interpreting the `args` and `defaults` in the signature.
        This means that we are currently ignoring `kw_defaults`, `kwarg`, `kwonlyargs`,
        `posonlyargs`, and `vararg`. So, right now, the only type of function signature
        we support is one with a finite list of pos args, followed immediately (no star)
        by a finite set of kwargs. In the future, we can try to support everything.
        """

        # FIXME:
        #  Should we just be reusing our AllowedCallable class here?
        #  Didn't we already do all the work of receiving a set of expected arguments?

        sig = self.signature
        n0 = len(sig.args)
        k0 = len(sig.defaults)
        a0 = n0 - k0
        args0 = sig.args[:a0]
        kwargs0 = {k: v for k, v in zip(sig.args[-k0:], sig.defaults)}

        a1 = len(args)
        k1 = len(kwargs)
        n1 = a1 + k1

        if a1 < a0:
            raise TypeError(f'Not enough positional args. Expecting {args0}.')
        if n1 > n0:
            raise TypeError(f'Too many args. Expecting {sig.args}.')

        keys0 = set(kwargs0.keys())
        keys1 = set(kwargs.keys())
        X = keys1 - keys0
        if X:
            raise TypeError(f'Unexpected keyword arguments {X}. Expecting {keys0}.')

        new_vars = {}
        new_vars.update({
            k: v for k, v in zip(sig.args, args)
        })
        for k in sig.args[a1:]:
            new_vars[k] = kwargs.get(k, kwargs0[k])

        for k, v in new_vars.items():
            self.evaluator.add_current_name(k, v)

    def __call__(self, *args, **kwargs):
        """
        Call the `process_displaylang()` function on the code block, and return its
        return value.
        """
        if self.signature:
            self.receive_args(*args, **kwargs)
        code = copy.deepcopy(self.body)
        ret_val, loc_vars = process_displaylang(
            code, self.evaluator.basic_vars, self.evaluator.local_vars,
            self.evaluator.allowed_callables.values(),
            add_builtins=False,
            allow_local_var_calls=self.evaluator.allow_local_var_calls,
            abstract_function_classes=self.evaluator.abstract_function_classes,
            abstract_relation_classes=self.evaluator.abstract_relation_classes,
            require_returned_str=False
        )
        return ret_val if self.return_just_value else (ret_val, loc_vars)


SUPPORTED_STATEMENT_TYPES = (
    ast.Assign, ast.AugAssign, ast.Expr, ast.Return,
    ast.FunctionDef, ast.For, ast.If,
    ast.Break, ast.Continue,
)


class DisplayLangBreakException(Exception):
    """Raised when a `break` statement is encountered."""
    ...


class DisplayLangContinueException(Exception):
    """Raised when a `continue` statement is encountered."""
    ...


class DisplayLangProcessor:
    """
    Handles the full process of initial checks, plus parsing and evaluating of
    a string of DisplayLang.
    """

    def __init__(self, evaluator, max_len=0, max_depth=-1):
        """
        :param evaluator: a DisplayLangEvaluator instance
        :param max_len: int
            The maximum allowed length for the code.
            If 0 (the default), no max length is imposed.
        :param max_depth: int
            The maximum allowed bracket depth for the code.
            If 0, no max depth is imposed.
            If -1 (the default), we use half of ``sys.getrecursionlimit()``, i.e.
            half the maximum depth of the Python interpreter stack.
        """
        self.evaluator = evaluator
        self.max_len = max_len
        self.max_depth = max_depth

    def process(self, code, local_vars, require_returned_str=True):
        """
        Evaluate some DisplayLang, and return the generated HTML string,
        plus dictionary of newly defined symbols.

        :param code: str, or list of ast nodes
            Either a string of DisplayLang that still needs to be parsed, or
            a list of ast nodes representing statements, as results from the
            parsing process, and typically represents the `body` element of
            an ast.Module or other control structure, like ast.For or ast.If.

        :param local_vars: dict
            The initial local vars that are defined at the start of the
            evaluation. Note: will be extended by any new vars that are defined
            by the DisplayLang code being processed. Pass a copy if you don't
            want the dict to be modified.

        :param require_returned_str: boolean
            If True (the default) then the given code is required to return a
            string. If False, then it is not.

        :returns: pair (str, dict)
            The string constructed by the code, and the dictionary of all local
            vars defined at the time of the return statement. In particular, this
            will include any new vars defined in the course of the DisplayLang code
            being evaluated.

        :raises: ControlledEvaluationException
            if...
                ...the code is too long or too deep;
                ...Python AST parser reports a SyntaxError in the code;
                ...the code contains any statement type other than those listed
                    in the SUPPORTED_STATEMENT_TYPES;
                ...we encounter a Python AST node type that is not supported, i.e.
                    the code goes outside the subset of Python we support;
                ...an attempt is made to call a callable that is not allowed;
                ...an attempt is made to pass unaccepted arguments or argument
                     types to a callable;
                ...anything goes wrong during building. In particular, this
                    includes the case that the python code contains not a syntax
                    but a runtime error;
            and, if `require_returned_str` True, then if...
                ...the return value of the code is not a string;
                ...the code has no return value.
        """
        # Obtain list of statement nodes
        statement_nodes = []
        if isinstance(code, list):
            statement_nodes = code
        elif isinstance(code, str):
            check_displaylang_dims(code, max_len=self.max_len, max_depth=self.max_depth)

            try:
                node = ast.parse(code)
            except (SyntaxError, MemoryError) as e:
                # SyntaxError should correspond to a Python syntax error in the given
                # code. MemoryError should be raised if the code has excessive
                # complexity, e.g. 300 nested lists etc. We have tried to already
                # catch such cases with the call to `check_display_build_dims`, but
                # this is a second chance to try to catch it.
                msg = 'Error parsing display widget build code.\n' + str(e)
                raise ControlledEvaluationException(msg) from e

            if not isinstance(node, ast.Module):
                reject('Outer node should be a Module.')

            statement_nodes = node.body
        else:
            reject('code must be either string or list of ast nodes')

        # Check node types
        for i, stmt in enumerate(statement_nodes):
            if not isinstance(stmt, SUPPORTED_STATEMENT_TYPES):
                msg = f'Statement {i} (zero-based) is a {stmt.__class__}.'
                msg += 'Supported statement types in DisplayLang are: '
                msg += ', '.join(str(t.__class__) for t in SUPPORTED_STATEMENT_TYPES)
                reject(msg)

        self.evaluator.set_local_vars(local_vars)

        def failed_to_return_string():
            if require_returned_str:
                msg = 'DisplayLang code failed to return a string.'
                raise ControlledEvaluationException(msg)

        for node in statement_nodes:
            try:
                result = self.evaluator.visit(node)
            # Re-raise exceptions we have deliberately raised.
            except ControlledEvaluationException as ce:
                raise ce from None
            except DisplayLangBreakException as e:
                raise e from None
            except DisplayLangContinueException as e:
                raise e from None
            # After that, we need a catch-all, since the Builder will attempt
            # constructions based on the user's (restricted) Python code, which
            # could easily contain any manner of runtime Python error. E.g. if the
            # user tried to do
            #   foo = f'{1.23:d}'
            # we will try to process the format string in good faith, but it will
            # fail since format code d does not apply to float 1.23.
            # We want such exceptions to be wrapped in `ControlledEvaluationException`
            # and re-raised in this form.
            except Exception as e:
                raise ControlledEvaluationException(repr(e)) from e
            if isinstance(result, ast.Return):
                val = result.value
                if not isinstance(val, str):
                    failed_to_return_string()
                return val, local_vars

        failed_to_return_string()

        return None, local_vars


def make_displaylang_processor(basic_vars,
                        allowed_callables,
                        add_builtins=False,
                        allow_local_var_calls=False,
                        abstract_function_classes=None,
                        abstract_relation_classes=None,
                        max_len=0,
                        max_depth=-1):
    """
    Convenience function for building a DisplayLangProcessor.

    :param basic_vars: dict
        As in ``ControlledEvaluator.__init__()``.
    :param allowed_callables: list
        Pass a list of ``AllowedCallable`` instances to be allowed during
        evaluation.
    :param add_builtins: bool, default False
        If True, we do two things: (1) prepend the passed list
        ``allowed_callables`` with all the allowed built-in functions and
        methods defined in ``builtins.py``; and (2) prepend ``basic_vars`` with
        just the ``basic_callables`` defined in ``builtins.py``.
    :param allow_local_var_calls: boolean
        As in ``ControlledEvaluator.__init__()``.
    :param abstract_function_classes:
        As in ``ControlledEvaluator.__init__()``.
    :param abstract_relation_classes:
        As in ``ControlledEvaluator.__init__()``.
    :param max_len: int
        The maximum allowed length for the code.
        If 0 (the default), no max length is imposed.
    :param max_depth: int
        The maximum allowed bracket depth for the code.
        If 0, no max depth is imposed.
        If -1 (the default), we use half of ``sys.getrecursionlimit()``, i.e.
        half the maximum depth of the Python interpreter stack.

    :return: DisplayLangProcessor
    """
    if add_builtins:
        basic_vars = {
            **{ac.name:ac.callable for ac in builtin_basic_callables},
            **basic_vars
        }

    evaluator = DisplayLangEvaluator(basic_vars, {},
                                     allow_local_var_calls=allow_local_var_calls,
                                     abstract_function_classes=abstract_function_classes,
                                     abstract_relation_classes=abstract_relation_classes)

    if add_builtins:
        evaluator.add_allowed_callables(builtin_basic_callables)
        evaluator.add_allowed_callables(builtin_other_callables)
    evaluator.add_allowed_callables(allowed_callables)

    return DisplayLangProcessor(evaluator, max_len=max_len, max_depth=max_depth)


def process_displaylang(code, basic_vars, local_vars,
                        allowed_callables,
                        add_builtins=False,
                        allow_local_var_calls=False,
                        abstract_function_classes=None,
                        abstract_relation_classes=None,
                        max_len=0,
                        max_depth=-1,
                        require_returned_str=True):
    p = make_displaylang_processor(
        basic_vars, allowed_callables, add_builtins=add_builtins,
        allow_local_var_calls=allow_local_var_calls,
        abstract_function_classes=abstract_function_classes,
        abstract_relation_classes=abstract_relation_classes,
        max_len=max_len, max_depth=max_depth
    )
    return p.process(code, local_vars, require_returned_str=require_returned_str)


# A basic DisplayLangProcessor, supporting the built-in functions and methods:
basic_displaylang_processor = make_displaylang_processor(
    {}, [], add_builtins=True
)
