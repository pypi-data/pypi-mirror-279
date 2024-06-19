from typing import List, Optional, Tuple, NewType, Union
from dataclasses import dataclass, field
from enum import Enum

import ast


@dataclass
class Argument:
    name: str
    type: Optional[str]

    def __str__(self):
        name = self.name
        type = f"{':' + self.type if self.type else ''}"
        return name + type


class ASTNode:
    def __init__(
        self,
        name: str,
        range: Tuple[int, int],
        scope: Optional["ASTNode"],
        decorators: List["Decorator"],
        lines: List[str],
        ast_node: Optional[ast.AST],
        is_test: bool = False,
        node_type: Optional["NodeType"] = None,
    ):
        # need to turn on mypy for this shit ...
        if decorators:
            assert isinstance(decorators[0], Decorator)
        else:
            assert isinstance(decorators, list) and len(decorators) == 0

        self._name = name
        # REFACTOR-AST: create a lang specific AST node class to account for decorators?
        # ie. PyAST/GolangAST
        self.decorators = decorators
        self.range = self._set_range(range)
        self.lines = [l.rstrip() for l in lines]
        self.is_test = is_test
        self.scope = scope
        self.ast_node = ast_node
        self.node_type = self.get_node_type()

    def get_node_type(self):
        return NodeType(self.__class__.__name__)

    def is_ast(self, other_ast: ast.AST) -> bool:
        """
        Checks if self matches another ast.AST node
        """
        return self.ast_node == other_ast

    def __eq__(self, other: "ASTNode"):
        return self.name + str(self.range) == other.name + str(other.range)

    def __hash__(self):
        return sum([ord(c) for c in self.name + str(self.range)])

    def _set_range(self, range) -> Tuple[int, int]:
        start = self.decorators[0].range[0] if self.decorators else range[0]
        end = range[1]
        return (start, end)

    def set_is_test(self, is_test: bool):
        self.is_test = is_test

    def to_code(self):
        repr = ""
        for dec in self.decorators:
            repr += dec.to_code()

        # newline if we have decorators
        repr += "\n" if repr else ""
        repr += "\n".join([l.rstrip() for l in self.lines])
        return repr

    @property
    def type(self) -> "NodeType":
        return NodeType(self.__class__.__name__)

    @property
    def name(self):
        raise NotImplementedError


@dataclass
class Decorator(ASTNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Class(ASTNode):
    def __init__(self, *args, **kwargs):
        self.functions: List[Function] = kwargs.pop("functions", [])

        super().__init__(*args, **kwargs)

    def add_func(self, func: "Function"):
        self.functions.append(func)

    # def __str__(self):
    #     funcs_str = "\n".join([f"{func.__str__()}" for func in self.functions])
    #     return f"Class: {self._name} \n{funcs_str}"

    def __eq__(self, other: "Class"):
        return self._name == other._name

    # def __repr__(self):
    #     funcs_str = "\n".join([f"{func}" for func in self.functions])
    #     return f"Class: {self._name} \n{funcs_str}"

    @property
    def name(self):
        return self._name


class Function(ASTNode):
    def __init__(self, *args, **kwargs):
        # should replace this with ... a prototype that contains .name property
        # self.scope: Class = kwargs.pop("scope", [])
        self.arguments = kwargs.pop("arguments", [])

        super().__init__(*args, **kwargs)

        self.is_test = True if self._name.startswith("test") else False

    def is_meth(self):
        return bool(self.scope)

    def __str__(self):
        return f"{self._name}({', '.join([arg.__str__() for arg in self.arguments])})"

    def is_method(self):
        return self.scope is not None

    def func_name(self):
        return self._name.split(".")[-1]

    @property
    def name(self):
        scope_prefix = f"{self.scope.name}." if self.scope else ""
        return f"{scope_prefix}{self._name}"


class NodeType(Enum):
    Function = Function.__name__
    Class = Class.__name__
    Decorator = Decorator.__name__
