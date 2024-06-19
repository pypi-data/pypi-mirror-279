from dataclasses import dataclass

from typing import List, Optional, TYPE_CHECKING, Tuple
from pathlib import Path

from cowboy_lib.ast.code import ASTNode


@dataclass
class TargetCode:
    """
    A chunk of code that is covered by the lines in a TestModule
    """

    range: Tuple[int, int]
    lines: List[str]
    filepath: Path
    func_scope: Optional[ASTNode]
    class_scope: Optional[ASTNode]

    def base_path(self) -> Path:
        """
        Returns the base path relative to the repo directory
        """
        return Path(*self.filepath.parts[2:])

    def __post_init__(self):
        if not isinstance(self.filepath, Path):
            self.filepath = Path(self.filepath)

    def __eq__(self, other: "TargetCode"):
        return self.filepath == other.filepath and self.range == other.range

    def __hash__(self):
        return hash((self.filepath, self.range))

    def to_lines(self):
        repr = ""
        for i, line in zip(range(self.range[0], self.range[1] + 1), self.lines):
            repr += f"{i}. {line}\n"

        return repr
