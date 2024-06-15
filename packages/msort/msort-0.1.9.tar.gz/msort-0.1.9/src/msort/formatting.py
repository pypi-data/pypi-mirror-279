"""Reformat class method definitions"""
import ast
import logging
from types import ModuleType
from typing import Dict
from typing import List
from typing import Optional

from .configs import format_msort_response
from .configs import ordered_methods_type
from .decorators import has_decorator
from .decorators import StaticMethodChecker
from .diff import SyntaxTreeDiffGenerator
from .method_describers import describe_method
from .method_describers import MethodDescriber
from .utilities import create_path
from .utilities import extract_text_from_file
from .utilities import get_function_name


def order_class_functions(
    methods: List[ast.stmt],
    method_describer: MethodDescriber,
    parser: ModuleType,
    parent: Optional[ast.stmt] = None,
    use_property_groups: bool = False,
) -> ordered_methods_type:
    """
    Sort a list of method definitions by the method type and alphabetically by method name
    Args:
        methods: list of method definitions
        method_describer: instance of MethodDescriber for classifying methods of classes
        parser: module containing functions for the code parser e.g. AST or CST
        parent: the node from which the methods where extracted
        use_property_groups: If True, then methods related to a property such as getter, setter, deleter will be
                            grouped together

    Returns:
        sorted_methods: method definitions sorted by method type
    """
    if parent is None or parser.is_class(parent):
        sorted_methods: List[ast.stmt] = sorted(methods, key=lambda m: describe_method(m, method_describer))
    else:
        sorted_methods = methods
    if use_property_groups:
        # find index of properties
        prop_idx = [i for i, method in enumerate(sorted_methods) if has_decorator(method, "property")]
        original_order = sorted_methods.copy()
        # iterate over properties and find methods with the same name
        for prop in prop_idx:
            updated_prop = sorted_methods.index(original_order[prop])
            attr_name = get_function_name(sorted_methods[updated_prop])
            # sort by property, getter, setter, deleter
            funcs = sorted(
                [method for method in sorted_methods if get_function_name(method) == attr_name],
                key=lambda m: describe_method(m, method_describer),
            )
            sorted_methods = [m for m in sorted_methods if m not in funcs]
            sorted_methods = sorted_methods[:updated_prop] + funcs + sorted_methods[updated_prop:]

    formatted_sorted_methods: ordered_methods_type = [
        {m: order_class_functions(parser.extract_class_components(m), method_describer, parser, m)}
        if parser.is_class(m) or parser.contains_class(m)
        else m
        for m in sorted_methods
    ]
    return formatted_sorted_methods


def format_msort(
    parser: ModuleType,
    file_path: str,
    method_describer: MethodDescriber,
    output_py: Optional[str] = None,
    auto_static: bool = False,
    use_property_groups: bool = False,
) -> format_msort_response:
    """
    Main function for running msort
    Args:
        parser: Module containing functions for specified code parser
        file_path: path to source code (.py) file
        method_describer: instance of MethodDescriber for extracting class method info
        output_py: where to write out formatted code (.py) file
        auto_static: If True, then static methods without the @staticmethod decorator will be marked as static
        use_property_groups: If True, then methods related to a property such as getter, setter, deleter will be
                            grouped together

    Returns:
        {
            "code" : indicates whether file has changed or not
            "diff": string indicating changes introduced by msort
        }
    """

    python_code = extract_text_from_file(file_path)
    parsed_code = parser.parse_code(code=python_code, file_path=file_path)
    classes = parser.find_classes(parsed_code)
    functions = {name: parser.extract_class_components(cls["node"]) for name, cls in classes.items()}

    if auto_static:
        static_checker = StaticMethodChecker(parser=parser)
        functions = static_checker.staticise_classes(functions)
        for class_name, n_changes in static_checker.class_static_method_counts.items():
            if n_changes > 0:
                logging.info("msort converted %s methods from %s to static!", n_changes, class_name)

    sorted_functions: Dict[str, ordered_methods_type] = {
        cls: order_class_functions(methods, method_describer, parser, use_property_groups=use_property_groups)
        for cls, methods in functions.items()
    }

    if all(functions[cname] == sorted_functions[cname] for cname in functions.keys()):
        logging.info("No changes made!")
        return format_msort_response(code=0, diff="")
    # update the classes dictionary with new class body
    classes = {name: parser.update_node(cls, sorted_functions[name]) for name, cls in classes.items()}
    # update parsed code with sorted classes
    parsed_code = parser.update_module(parsed_code, classes)

    new_code = parser.nodes_to_code(tree=parsed_code, source_code=python_code)

    diff_gen = SyntaxTreeDiffGenerator()
    diff_list = []
    for cls_name in functions:
        diff = diff_gen.diff(functions[cls_name], sorted_functions[cls_name])
        diff = f"**************\n ***** {file_path} *****\n**************\n" + f"\n ----- {cls_name} ----- \n" + diff
        diff_list.append(diff)
    compiled_diff = "/n/n".join(diff_list)

    if output_py is not None:
        create_path(output_py)
        with open(output_py, "w", encoding="utf-8") as f:
            f.writelines(new_code)
    return format_msort_response(code=1, diff=compiled_diff)
