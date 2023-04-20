#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Christian Heider Nielsen"
__doc__ = r"""

           Created on 26-01-2021
           """

__all__ = ["FirstArgIdentifier", "get_first_arg_name", "cprint"]

import ast
from typing import Optional, Any


def recurse_first_args(args):
    """

    :param args:
    :type args:
    :return:
    :rtype:
    """
    for a in args:
        if isinstance(a, ast.Call):
            if isinstance(a.func, ast.Attribute):
                r = f"{a.func.attr}"
            else:
                r = f"{a.func.id}"
            return f"{r}({recurse_first_args(a.args)})"
    else:
        if isinstance(args, ast.Constant):
            return args.value


class FirstArgIdentifier(ast.NodeVisitor):
    """description"""

    def __init__(
        self,
        *args,
        verbose: bool = False,
        max_num_intermediate_unnamed_elements: int = -1,  # recurse = -1
    ):
        if len(args) < 1:
            raise ValueError("Supply at least one target function")
        self.result = {arg: {} for arg in args}
        self.verbose = verbose
        # assert max_num_intermediate_unnamed_elements >= 0
        self.sequence_depth = max_num_intermediate_unnamed_elements

    def visit_Call(self, node: ast.AST) -> None:
        """
        Should work for most use cases, but no guarantee

        :param node:
        :return:
        """
        if hasattr(node.func, "id") and node.func.id in self.result:
            first_arg = node.args[0]
            if isinstance(first_arg, ast.Name):
                iter_name = first_arg.id
            elif isinstance(first_arg, ast.Call):
                if isinstance(first_arg.func, ast.Attribute):
                    # print(first_arg.func.value.value.id) # TODO: UNROLLING is possible, do some resursion
                    # print(first_arg.func.value.attr) # TODO: SAME for full qualification in scope
                    iter_name = f"{first_arg.func.attr}"
                else:
                    iter_name = f"{first_arg.func.id}"

                if self.sequence_depth < 0:
                    iter_name += f"({recurse_first_args(first_arg.args)})"

                if self.verbose:
                    args_repr = f'{", ".join([ast.dump(sub) for sub in first_arg.args])}'
                    kws_repr = f'{", ".join([ast.dump(sub) for sub in first_arg.keywords])}'
                    args_kw_repr = []
                    if len(args_repr) > 1:
                        args_kw_repr.append(args_repr)
                    if len(kws_repr) > 1:
                        args_kw_repr.append(kws_repr)
                    iter_name += f'({", ".join(args_kw_repr)})'
            elif isinstance(first_arg, (ast.List, ast.Set, ast.Tuple)):
                elts = first_arg.elts
                if self.sequence_depth > 0:
                    if self.sequence_depth < len(elts) - 2:
                        if (
                            self.sequence_depth
                        ):  # TODO: Generalise to another external function, "pick num from sequence" func
                            stride = (len(elts) // self.sequence_depth) + 1
                            between = elts[1:-2:stride]
                        else:
                            between = []
                        elts_str = [ast.dump(sub) for sub in [elts[0]] + between + [elts[-1]]]
                        iter_name = f'[{" .. ".join(elts_str)}]'
                    else:
                        iter_name = f'[{", ".join([ast.dump(sub) for sub in elts])}]'
                else:
                    iter_name = f'[{", ".join([ast.dump(sub) for sub in elts])}]'
            elif isinstance(first_arg, ast.Dict):
                kw_repr = f'{", ".join([f"{k}:{v}" for k, v in zip([ast.dump(sub) for sub in first_arg.keys], [ast.dump(sub) for sub in first_arg.values])])}'
                iter_name = f"{{{kw_repr}}}"
            else:  # No obvious name
                if self.verbose:
                    print(type(first_arg))
                    iter_name = f"{ast.dump(first_arg)}"
                else:
                    iter_name = "iterable"
            self.result[node.func.id][node.lineno] = iter_name
        self.generic_visit(node)  # visit the children


def get_first_arg_name(
    func_name: str,
    *,
    verbose=False,
    max_num_intermediate_unnamed_elements=-1,  # recurse = -1
) -> Optional[str]:
    """description"""
    import inspect
    import textwrap
    import ast

    caller_frame = inspect.currentframe().f_back.f_back
    try:
        caller_src_code_lines = inspect.getsourcelines(caller_frame)
        fai = FirstArgIdentifier(
            func_name,
            verbose=verbose,
            max_num_intermediate_unnamed_elements=max_num_intermediate_unnamed_elements,
        )
        fai.visit(ast.parse(textwrap.dedent("".join(caller_src_code_lines[0]))))
        if func_name in fai.result:
            offset = 0
            if caller_src_code_lines[1]:
                offset = caller_src_code_lines[1] - 1
            idx = caller_frame.f_lineno - offset
            if idx in fai.result[func_name]:
                return fai.result[func_name][idx]
            elif verbose:
                print(
                    f'Unexpected line number: {idx}, probably a wrong alias "{func_name}" was supplied, found {fai.result[func_name]}, in {inspect.getsourcefile(caller_frame)}'
                )
        elif verbose:
            print(f"{func_name} was not found in {fai.result}")
    except Exception as e:
        print(e)
    return


def get_first_arg_name_recurse() -> Optional[str]:
    """
    unpack chained generators to base iterator name

    :return:
    :rtype:
    """
    pass  # TODO: For e.g. description in progress_bar(range(_name_))
    raise NotImplementedError


def cprint(v: Any, writer: callable = print, deliminator: str = ":") -> None:
    """

    :param v:
    :type v:
    :param writer:
    :type writer:
    :param deliminator:
    :type deliminator:
    """
    if isinstance(v, str) and v.strip() == "":
        v = '""'
    writer(f"{get_first_arg_name('cprint')}{deliminator}", v)


if __name__ == "__main__":

    def siajd():
        """description"""
        s = ""
        cprint(s)
        cprint("")
        ass = "    "
        cprint(ass)
        cprint("  ")

    def ausdh() -> None:
        """
        :rtype: None
        """
        import inspect
        import textwrap
        import ast
        from warg import FirstArgIdentifier

        def some_func(a):
            """description"""
            caller_frame = inspect.currentframe().f_back
            # caller_src_code_snippet = inspect.getsource(caller_frame) # Only gets scope
            caller_src_code_lines = inspect.getsourcelines(caller_frame)
            caller_src_code_valid = textwrap.dedent(
                "".join(caller_src_code_lines[0])
            )  # TODO: maybe there is a nicer way?
            call_nodes = ast.parse(
                caller_src_code_valid
            )  # parse code to get nodes of abstract syntax tree of the call
            fai = FirstArgIdentifier("some_func")
            fai.visit(call_nodes)
            snippet_offset = caller_src_code_lines[1] - 1
            desc = fai.result["some_func"][caller_frame.f_lineno - snippet_offset]
            print(desc)

        this_name_is_in_another_frame = 5
        this_func_is_in_another_frame = lambda x: x
        this_generator_is_in_another_frame = range(24)

        class this_class_is_in_another_frame:
            pass

        some_func(this_name_is_in_another_frame)
        some_func(this_func_is_in_another_frame)
        some_func(this_generator_is_in_another_frame)
        # some_func([this_func_is_in_another_frame, this_func_is_in_another_frame, this_generator_is_in_another_frame,this_class_is_in_another_frame])
        some_func([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

    def ausdh2() -> None:
        """
        :rtype: None
        """
        import inspect
        import textwrap
        import ast
        from warg import FirstArgIdentifier

        def some_func(a):
            """description"""
            caller_frame = inspect.currentframe().f_back
            # caller_src_code_snippet = inspect.getsource(caller_frame) # Only gets scope
            caller_src_code_lines = inspect.getsourcelines(caller_frame)
            caller_src_code_valid = textwrap.dedent(
                "".join(caller_src_code_lines[0])
            )  # TODO: maybe there is a nicer way?
            call_nodes = ast.parse(
                caller_src_code_valid
            )  # parse code to get nodes of abstract syntax tree of the call
            fai = FirstArgIdentifier("some_func")
            fai.visit(call_nodes)
            snippet_offset = caller_src_code_lines[1] - 1
            desc = fai.result["some_func"][caller_frame.f_lineno - snippet_offset]
            print(desc)

        some_func({1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 8, 9: 9, 10: 10})

    def ausdh3() -> None:
        """
        :rtype: None
        """
        from typing import Any

        def some_func(a: Any) -> None:
            """description"""
            print(get_first_arg_name("some_func", verbose=True))

        some_func(print(2, sep="-"))

    def ausd2h3() -> None:
        """
        :rtype: None
        """
        from typing import Any
        import warg

        def some_func(a: Any) -> None:
            """description"""
            print(get_first_arg_name("some_func", verbose=True))

        some_func(warg.identity(2))

    def ausd2h3213() -> None:
        """
        :rtype: None
        """
        from typing import Any

        class Ac:
            class Bc:
                @staticmethod
                def c(d):
                    """description"""
                    pass

        def some_func(a: Any) -> None:
            """description"""
            print(get_first_arg_name("some_func", verbose=True))

        some_func(Ac.Bc.c(2))

    # ausdh()
    # ausdh2()
    # ausdh3()
    # ausd2h3()
    # ausd2h3213()
    siajd()
