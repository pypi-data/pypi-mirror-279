"""Functions for handling method decorators"""
import ast
from collections import defaultdict
from collections.abc import Hashable
from types import ModuleType
from typing import Callable
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple

import libcst

from .configs import Node
from .utilities import get_function_name


class DecoratorDefaultDict(defaultdict):
    """
    Subclass of defaultdict to return length of this dictionary if provided key is missing

    Examples:
        d = DecoratorDefaultDict()
        d["key"] = "value"
        d["missing_key"]  # will return 1
    """

    def __init__(self) -> None:
        super().__init__(self.__class__)

    def __missing__(self, key: Hashable) -> int:
        return len(self)


# define here the ordering of decorated class functions
# any decorator not defined here will return the length of the dictionary
decorator_orders = DecoratorDefaultDict()
decorators = ["classmethod", "staticmethod", "property", "getter", "setter"]
for i, dec in enumerate(decorators):
    decorator_orders[dec] = i

# -------------------------------------------------------------------------
# AST functions
# -------------------------------------------------------------------------


def get_msort_group_name_ast(method: ast.FunctionDef) -> Optional[str]:
    """
    Extract the provided msort group name from the msort_group decorator
    Args:
        method: AST parsed decorator

    Returns:
        group name from the msort_group decorator
    """
    if not hasattr(method, "decorator_list"):
        return None
    decorators = method.decorator_list
    idx = [i for i, decorator in enumerate(decorators) if get_decorator_id(decorator) == "msort_group"]
    if len(idx) == 0:
        return None
    decorator = decorators[idx[0]]
    if not isinstance(decorator, ast.Call):
        return None
    if decorator.args:
        if not hasattr(decorator.args[0], "value"):
            return None
        return decorator.args[0].value
    if not hasattr(decorator.keywords[0].value, "value"):
        return None
    return decorator.keywords[0].value.value


def decorator_name_id(decorator: ast.Name) -> str:
    """
    Get the decorator type from an ast.Name decorator
    Args:
        decorator: input decorator

    Returns:
        id attribute
    """
    return decorator.id


def decorator_attribute_id(decorator: ast.Attribute) -> str:
    """
    Get the decorator type from an ast.Attribute decorator
    Args:
        decorator: input decorator

    Returns:
        attr attribute
    """
    return decorator.attr


def decorator_call_id(decorator: ast.Call) -> str:
    """
    Get the decorator type from an ast.Call decorator
    Args:
        decorator: input decorator

    Returns:
        attr attribute

    Raises:
        AttributeError: if decorator.func does not have id attribute
    """
    if hasattr(decorator.func, "id"):
        return decorator.func.id
    raise AttributeError("decorator of type ast.Call does not have func attribute with id attribute!")


# -------------------------------------------------------------------------
# CST functions
# -------------------------------------------------------------------------


def get_msort_group_name_cst(method: libcst.FunctionDef) -> Optional[str]:
    """
    Extract the provided msort group name from the msort_group decorator
    Args:
        method: CST parsed decorator

    Returns:
        group name from the msort_group decorator
    """
    decorators = method.decorators
    idx = [i for i, decorator in enumerate(decorators) if get_decorator_id_cst(decorator) == "msort_group"]
    if len(idx) == 0:
        return None
    decorator = decorators[idx[0]]
    if not hasattr(decorator.decorator, "args"):
        raise AttributeError("Could not find args attribute of msort_group decorator!")
    return decorator.decorator.args[0].value.value


def decorator_name_id_cst(decorator: libcst.Decorator) -> str:
    """
    Get the decorator type from an Name decorator
    Args:
        decorator: input decorator

    Returns:
        id attribute
    """
    if not hasattr(decorator.decorator, "value"):
        raise AttributeError("Could not find value attribute of decorator!")
    return decorator.decorator.value


def decorator_attribute_id_cst(decorator: libcst.Decorator) -> str:
    """
    Get the decorator type from an Attribute decorator
    Args:
        decorator: input decorator

    Returns:
        attr attribute
    """
    if not hasattr(decorator.decorator, "attr"):
        raise AttributeError("Could not find attr attribute of decorator!")
    return decorator.decorator.attr.value


def decorator_call_id_cst(decorator: libcst.Decorator) -> str:
    """
    Get the decorator type from an ast.Call decorator
    Args:
        decorator: input decorator

    Returns:
        attr attribute

    Raises:
        AttributeError: if decorator.func does not have id attribute
    """
    if isinstance(decorator.decorator, libcst.Call):
        if hasattr(decorator.decorator.func, "value"):
            return decorator.decorator.func.value
    raise AttributeError("libcst decorator of type libcst.Call does not have func attribute with value attribute!")


# factory to indicate what functions to call for describing different types of decorators
ast_decorator_description_factory: Dict[type, Callable] = {
    ast.Name: decorator_name_id,
    ast.Attribute: decorator_attribute_id,
    ast.Call: decorator_call_id,
}

cst_decorator_description_factory: Dict[type, Callable] = {
    libcst.Name: decorator_name_id_cst,
    libcst.Attribute: decorator_attribute_id_cst,
    libcst.Call: decorator_call_id_cst,
}


def get_msort_group_name(method: Node) -> Optional[str]:
    """
    Get the group name from a msort_group decorator
    Args:
        method: class method

    Returns:
        name assigned to msort group
    """
    if not isinstance(method, (ast.FunctionDef, libcst.FunctionDef)):
        return None
    if isinstance(method, ast.FunctionDef):
        return get_msort_group_name_ast(method)
    return get_msort_group_name_cst(method)


def get_decorator_id(decorator: ast.expr) -> str:
    """
    Get the decorator type from a method decorator parsed by ast

    This function uses decorator_description_factory to find the correct attribute given the type of ast expression.
    Args:
        decorator: input decorator expression

    Returns:
        type of decorator
    """
    func = ast_decorator_description_factory.get(type(decorator))
    if func is None:
        raise TypeError(f"Unexpected type {type(decorator)}!")
    return func(decorator)


def get_decorator_id_cst(decorator: libcst.Decorator) -> str:
    """
    Get the decorator type from a method decorator parsed by CST

    Args:
        decorator: input decorator expression

    Returns:
        type of decorator
    """
    func = cst_decorator_description_factory.get(type(decorator.decorator))
    if func is None:
        raise TypeError(f"Unexpected type {type(decorator)}!")
    return func(decorator)


def get_decorators(method: Node, sort: bool = False) -> Optional[List[str]]:
    """
    Get decorators from an ast parsed function
    Args:
        method: the ast parsed method
        sort: if True, then decorators will be sorted according to decorator_orders

    Returns:
        list of ids from decorator list attribute
    """
    if isinstance(method, ast.stmt):
        return _get_decorators_ast(method, sort=sort)
    return _get_decorators_cst(method, sort=sort)


def _get_decorators_ast(method: ast.stmt, sort: bool = False) -> Optional[List[str]]:
    """
    Get decorators from an ast parsed function
    Args:
        method: the ast parsed method
        sort: if True, then decorators will be sorted according to decorator_orders

    Returns:
        list of ids from decorator list attribute
    """
    if not isinstance(method, ast.FunctionDef) or not hasattr(method, "decorator_list"):
        return None
    decorators = [get_decorator_id(decorator) for decorator in method.decorator_list]
    if sort:
        decorators = order_decorators(decorators)
    return decorators


def _get_decorators_cst(method: libcst.CSTNode, sort: bool = False) -> Optional[List[str]]:
    """
    Get decorators from an CST parsed function
    Args:
        method: the CST parsed method
        sort: if True, then decorators will be sorted according to decorator_orders

    Returns:
        list of ids from decorator list attribute
    """
    if not isinstance(method, libcst.FunctionDef) or not hasattr(method, "decorators"):
        return None
    decorators = [get_decorator_id_cst(decorator) for decorator in method.decorators]
    if sort:
        decorators = order_decorators(decorators)
    return decorators


def has_decorator(method: Node, decorator: str) -> bool:
    """
    Determine if a parsed method has a specific decorator
    Args:
        method: the AST or CST parsed method node
        decorator: decorator to look for

    Returns:
        True if decorator in the decorators
    """
    decorators = get_decorators(method)
    if decorators is None:
        return False
    return decorator in decorators


def _get_decorator_order(decorator: str) -> Tuple[int, str]:
    """
    Get the decorator order from decorator_orders

    A tuple if returned with the name to sort decorators alphabetically if the level is equal.
    Args:
        decorator: name of decorator

    Returns:
        (level of decorator, name of decorator)
    """
    return decorator_orders[decorator], decorator


def order_decorators(decorators: List[str]) -> List[str]:
    """
    Sort a list of decorators according to the pre-defined ordering in decorator_orders
    Args:
        decorators: list of decorators found for a method

    Returns:
        sorted decorators
    """
    return sorted(decorators, key=_get_decorator_order)


class StaticMethodChecker:
    """
    A class for checking of an AST or CST parsed method could be labelled as static.

    If a method does not use "self" in the method body then the @staticmethod decorator can be assigned.
    """

    def __init__(self, parser: ModuleType) -> None:
        """
        Initialise the class

        Args:
            parser: code module with parser specific functions
        """
        self.parser = parser
        self.static_method_count: int = 0
        self.class_static_method_counts: Dict[str, int] = {}

    @staticmethod
    def _check_for_static_ast(func: ast.FunctionDef) -> bool:
        """
        Returns True if "self" in params but not used in body of the code
        Args:
            func: input class method

        Returns:
            True or False
        """
        params = [arg.arg for arg in func.args.args]
        if "self" not in params:
            return False
        code = "\n".join([ast.unparse(node) for node in func.body])
        return "self" not in code

    @staticmethod
    def _check_for_static_cst(func: libcst.FunctionDef) -> bool:
        """
        Returns True if "self" in params but not used in body of the code
        Args:
            func: input class method

        Returns:
            True or False
        """
        params = [param.name.value for param in func.params.params]
        if "self" not in params:
            return False
        code = libcst.Module([]).code_for_node(func.body)
        return "self" not in code

    @staticmethod
    def _make_static_ast(func: ast.FunctionDef) -> ast.FunctionDef:
        """
        Modify AST parsed function to include @staticmethod decorator and remove "self" from args
        Args:
            func: input class method

        Returns:
            func: decorated with @staticmethod
        """
        func.decorator_list.append(ast.Name(id="staticmethod", lineno=func.lineno - 1, col_offset=func.col_offset))
        func.args.args = [arg for arg in func.args.args if arg.arg != "self"]
        return func

    @staticmethod
    def _make_static_cst(func: libcst.FunctionDef) -> libcst.FunctionDef:
        """
        Modify CST parsed function to include @staticmethod decorator and remove "self" from args
        Args:
            func: input class method

        Returns:
            func: decorated with @staticmethod
        """
        new_decorator_tuple = tuple([libcst.Decorator(decorator=libcst.Name(value="staticmethod"))])
        func = func.with_changes(decorators=new_decorator_tuple)
        new_params = [param for param in func.params.params if param.name.value != "self"]
        func = func.with_changes(params=func.params.with_changes(params=tuple(new_params)))
        return func

    def get_static_method_count(self) -> int:
        """
        Getter for static method count
        Returns:
            number of functions converted to static
        """
        return self.static_method_count

    def staticise_classes(self, class_dict: Dict[str, List[Node]]) -> Dict[str, List[Node]]:
        """
        Iterate over each class and its list of functions, apply staticise to each function,
        and store the static method count for each class.

        Args:
            class_dict: Dictionary where keys are class names and values are lists of class components.

        Returns:
            Dictionary with class names as keys and counts of static method conversions as values.
        """
        self.class_static_method_counts = {}
        for class_name, funcs in class_dict.items():
            self.static_method_count = 0
            class_dict[class_name] = [self._staticise(func) for func in funcs]
            self.class_static_method_counts[class_name] = self.get_static_method_count()
        return class_dict

    def _check_for_static(self, func: Node) -> bool:
        """
        Returns True if the function is not labelled with staticmethod but could be static
        Args:
            func: input class method

        Returns:
            True or False
        """
        if (
            has_decorator(func, "staticmethod")
            or has_decorator(func, "abstractmethod")
            or self.parser.is_dunder_method(func)
        ):
            return False
        if isinstance(func, ast.FunctionDef):
            return self._check_for_static_ast(func)
        if isinstance(func, libcst.FunctionDef):
            return self._check_for_static_cst(func)
        return False

    def _make_static(self, func: Node) -> Node:
        """
        Modify parsed function to include @staticmethod decorator and remove "self" from args
        Args:
            func: input class method

        Returns:
            func: decorated with @staticmethod
        """
        if isinstance(func, ast.FunctionDef):
            return self._make_static_ast(func)
        if isinstance(func, libcst.FunctionDef):
            return self._make_static_cst(func)
        return func

    def _staticise(self, node: Node) -> Node:
        """
        If the class component provided is a method then check if it could be static and modify if so.
        Args:
            node: input class component

        Returns:
            func: forced to be static if applicable
        """
        if not (self.parser.is_function(node) or self.parser.is_class(node)):
            return node

        # recursive action for the class - extract methods and replace class body
        if self.parser.is_class(node):
            node_name = get_function_name(node)
            node = self.parser.update_node_body(
                node,
                self.staticise_classes(class_dict={node_name: self.parser.extract_class_components(node)})[node_name],
            )
        elif self.parser.contains_class(node):
            node = self.parser.update_node_body(
                node, [self._staticise(child) for child in self.parser.extract_class_components(node)]
            )
        else:
            pass
        if self._check_for_static(node):
            self.static_method_count += 1
            return self._make_static(node)
        return node
