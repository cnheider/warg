#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Christian Heider Nielsen"
__doc__ = r"""

           Created on 26-01-2021
           """

__all__ = ["ArgIdentifier", "get_arg_names", "cprinta", "cprintz"]

import ast
from typing import Optional, Any


class ArgIdentifier(ast.NodeVisitor):
    """description"""

    def __init__(
        self,
        *args,
        verbose: bool = False,
        max_num_intermediate_unnamed_elements: int = 1,
    ):
        if len(args) < 1:
            raise ValueError("Supply at least one target function")
        self.result = {arg: {} for arg in args}
        self.verbose = verbose
        assert max_num_intermediate_unnamed_elements >= 0
        self.num_unnamed_sequence_elements = max_num_intermediate_unnamed_elements

    def visit_Call(self, node: ast.AST) -> None:
        """
        Should work for most use cases, but no guarantee

        :param node:
        :return:
        """
        if hasattr(node.func, "id") and node.func.id in self.result:
            for arg in node.args:
                if isinstance(arg, ast.Name):
                    n = arg.id
                elif isinstance(arg, ast.Call):
                    if isinstance(arg.func, ast.Attribute):
                        # print(first_arg.func.value.value.id) # TODO: UNROLLING is possible, do some resursion
                        # print(first_arg.func.value.attr) # TODO: SAME for full qualification in scope
                        n = f"{arg.func.attr}"
                    else:
                        n = f"{arg.func.id}"
                    if self.verbose:
                        args_repr = f'{", ".join([ast.dump(sub) for sub in arg.args])}'
                        kws_repr = f'{", ".join([ast.dump(sub) for sub in arg.keywords])}'
                        args_kw_repr = []
                        if len(args_repr) > 1:
                            args_kw_repr.append(args_repr)
                        if len(kws_repr) > 1:
                            args_kw_repr.append(kws_repr)
                        n += f'({", ".join(args_kw_repr)})'
                elif isinstance(arg, (ast.List, ast.Set, ast.Tuple)):
                    elts = arg.elts
                    if self.num_unnamed_sequence_elements < len(elts) - 2:
                        if (
                            self.num_unnamed_sequence_elements
                        ):  # TODO: Generalise to another external function, "pick num from sequence" func
                            stride = (len(elts) // self.num_unnamed_sequence_elements) + 1
                            between = elts[1:-2:stride]
                        else:
                            between = []
                        elts_str = [ast.dump(sub) for sub in [elts[0]] + between + [elts[-1]]]
                        n = f'[{" .. ".join(elts_str)}]'
                    else:
                        n = f'[{", ".join([ast.dump(sub) for sub in elts])}]'
                elif isinstance(arg, ast.Dict):
                    kw_repr = f'{", ".join([f"{k}:{v}" for k, v in zip([ast.dump(sub) for sub in arg.keys], [ast.dump(sub) for sub in arg.values])])}'
                    n = f"{{{kw_repr}}}"
                else:  # No obvious name
                    if self.verbose:
                        print(type(arg))
                        n = f"{ast.dump(arg)}"
                    else:
                        n = "iterable"
                if node.lineno not in self.result[node.func.id]:
                    self.result[node.func.id][node.lineno] = []
                self.result[node.func.id][node.lineno].append(n)
        self.generic_visit(node)  # visit the children


def get_arg_names(func_name: str, *, verbose=False, max_num_intermediate_unnamed_elements=1) -> Optional[str]:
    """description"""
    import inspect
    import textwrap
    import ast

    caller_frame = inspect.currentframe().f_back.f_back
    try:
        caller_src_code_lines = inspect.getsourcelines(caller_frame)
        fai = ArgIdentifier(
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


def ge_arg_names_recurse() -> Optional[str]:
    """
    unpack chained generators to base iterator name

    :return:
    :rtype:
    """
    pass  # TODO: For e.g. description in progress_bar(range(_name_,_name2_))
    raise NotImplementedError


def cprinta(*v: Any, writer: callable = print, deliminator: str = ":") -> None:
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
    writer(f"{get_arg_names('cprinta')}{deliminator}", v)


def cprintz(*v: Any, writer: callable = print) -> None:
    """

    :param v:
    :type v:
    :param writer:
    :type writer:
    """
    if isinstance(v, str) and v.strip() == "":
        v = '""'

    gen = zip(get_arg_names("cprintz"), v)
    writer(f"{list(gen)}")


if __name__ == "__main__":

    def siajd():
        """description"""
        s = ""
        aisjd = s
        sioj = 4
        cprinta(s, aisjd, sioj)
        cprinta("")
        ass = "    "
        ls = ass + s
        cprinta(ass, ls, 2)
        cprinta("  ")

        cprintz(ass, ls, 2)

    siajd()
