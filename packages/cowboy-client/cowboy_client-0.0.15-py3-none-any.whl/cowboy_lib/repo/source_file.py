from typing import List, Optional, Tuple
from pathlib import Path
from difflib import unified_diff

from cowboy_lib.ast import Class, Function, ASTNode, NodeType
from cowboy_lib.ast import PythonAST

from logging import getLogger
from copy import deepcopy

import subprocess


logger = getLogger("test_results")
longterm_logger = getLogger("longterm")


class LintException(Exception):
    pass


class SameNodeException(Exception):
    pass


class NodeNotFound(Exception):
    pass


class SourceFile:
    def __init__(
        self,
        lines: List[str],
        path: Path,
        language: str = "python",
    ):
        self._path = path
        self._lang = language

        self.functions: List[Function] = []
        self.classes: List[Class] = []
        self.lines: List[str] = []
        # self.imports: List[str] = []

        self.update_file_state(lines)

    def clone(self) -> "SourceFile":
        return deepcopy(self)

    @property
    def path(self):
        return self._path

    def update_file_state(self, lines: List[str]):
        """
        Updates instance variables
        """
        assert isinstance(lines, list)

        # REFACTOR-AST: start here first, this is where we convert
        # AST into our code-object representation of the src code
        self.ast_parser = PythonAST("\n".join(lines))
        self.functions, self.classes = self.ast_parser.parse()
        self.lines = lines

    def __repr__(self):
        return f"{self.path}"

    def diff(self, other: "SourceFile"):
        if not isinstance(other, SourceFile):
            raise TypeError("Can only diff SourceFile instances")

        a = self.to_code().splitlines(keepends=True)
        b = other.to_code().splitlines(keepends=True)
        diff = "".join(unified_diff(a, b))

        return diff

    # this would be another easy test for modification in test_parsing
    # commit: c58ded2
    def find_class(self, class_name: str) -> Optional[Class]:
        """
        Finds a class by name
        """
        return self.find_by_nodetype(class_name, node_type=NodeType.Class)

    def find_function(self, function_name: str) -> Optional[Function]:
        """
        Finds a function by name
        """
        return self.find_by_nodetype(function_name, node_type=NodeType.Function)

    def find_by_nodetype(
        self, node_name: str, node_type: NodeType = NodeType.Function
    ) -> Optional[List[ASTNode]]:
        """
        Finds a function or class by name
        """
        assert type(node_name) == str

        all = [f for f in self.functions + self.classes if f.name == node_name]
        filtered = [f for f in all if f.type == node_type]

        if len(filtered) > 1:
            raise SameNodeException(
                "More than one node found with the same name: ", node_name
            )
        elif len(filtered) == 0:
            raise Exception(
                "No node found with the given name, did you forget to put NODETYPE param again you dumbass?: ",
                node_name,
                node_type,
            )

        return filtered[0]

    def append(self, lines: str, class_name: Optional[str] = None) -> None:
        """
        Appends lines to the test file or to an existing class
        """
        if class_name:
            node = self.find_by_nodetype(class_name, node_type=NodeType.Class)
            _, end = node.range
        else:
            end = len(self.lines) - 1

        lines = lines.split("\n")
        lines = self.lines[: end + 1] + lines + self.lines[end + 1 :]
        self.update_file_state(self.to_linted_code(lines).split("\n"))

    def delete(self, node_name: str, node_type: NodeType = NodeType.Function) -> None:
        """
        Deletes a new function or class to the file, and updates SourceFile instance accordingly without hitting file
        """

        node = self.find_by_nodetype(node_name, node_type=node_type)
        start, end = node.range

        longterm_logger.info(f"Deleting: {node.name} => {start} to {end}")

        lines = self.lines[:start] + self.lines[end + 1 :]
        self.update_file_state(self.to_linted_code(lines).split("\n"))

    # TODO: specify other code linter here
    def to_linted_code(self, lines) -> str:
        """
        Lint generated code file
        """

        self.i = 0 if getattr(self, "i", None) is None else self.i + 1

        black_cmd_str = "python -m black "
        tmp_file = f"/tmp/test{str(self.i)}.py"
        with open(tmp_file, mode="w+t", encoding="utf-8") as temp_file:
            # temp_file_name = temp_file.name
            temp_file.write("\n".join(lines))
            temp_file.flush()

            process = subprocess.Popen(
                black_cmd_str + tmp_file,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            stdout, stderr = process.communicate()
            if stderr:
                stderr = stderr.decode("utf-8")
                if "error:" in stderr:
                    raise LintException(f"Error while linting: {stderr}")

            with open(tmp_file, "r") as temp_file:
                linted_code = temp_file.read()

        return linted_code

    def map_line_to_node(
        self, start: int, end: int
    ) -> Optional[Tuple[ASTNode, ASTNode]]:
        """
        Finds the function and/or class that contains the line
        """
        for node in self.functions:
            if node.range[0] <= start and end <= node.range[1]:
                return node, node.scope
        return None, None

    def to_code(self) -> str:
        """
        Converts the sourcefile to code
        """

        return "\n".join(self.lines)

    def to_num_lines(self) -> str:
        return "\n".join([f"{i}: {line}" for i, line in enumerate(self.lines)])

    def to_llm_repr(self) -> str:
        repr_str = ""
        repr_str += "\n".join([f.__str__() for f in self.functions if not f.scope])
        repr_str += "\n"
        repr_str += "\n".join([c.__str__() for c in self.classes])
        return repr_str


class TestFile(SourceFile):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def test_nodes(self) -> List[ASTNode]:
        return [n for n in self.functions + self.classes if n.is_test]

    def test_funcs(self) -> List[Function]:
        return [func for func in self.functions if func.is_test]

    def test_classes(self) -> List[Class]:
        return [c for c in self.classes if c.is_test]

    def __repr__(self):
        return f"{self.path}"

    def new_test_funcs(self, new_file: "TestFile") -> List[Function]:
        """
        Returns a list of nodes that are in the new file but not in the current file
        """
        assert Path(self._path) == Path(new_file.path)

        return [
            f
            for f in new_file.test_funcs()
            if f.name not in [my_f.name for my_f in self.test_funcs()]
        ]
