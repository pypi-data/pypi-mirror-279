from cowboy_lib.utils import generate_id
from cowboy_lib.repo.repository import PatchFile

from pydantic import BaseModel, Field, ConfigDict, root_validator
from typing import List, Optional, Any, Tuple, Dict

from pathlib import Path
from enum import Enum

from dataclasses import dataclass, field


class TaskStatus(Enum):
    PENDING = "PENDING"
    STARTED = "STARTED"
    COMPLETE = "COMPLETE"
    FAILED = "FAILED"


class TaskResult(BaseModel):
    coverage: Optional[Dict] = None
    failed: Optional[Dict] = None
    exception: Optional[str] = None

    @root_validator
    def check_coverage_or_exception(cls, values):
        coverage, failed, exception = (
            values.get("coverage"),
            values.get("failed"),
            values.get("exception"),
        )
        if exception and (coverage or failed):
            raise ValueError(
                "If 'exception' is specified, 'coverage' and 'failed' must not be specified."
            )
        if not exception and not (coverage or failed):
            raise ValueError(
                "Either 'coverage' and 'failed' or 'exception' must be specified."
            )
        return values


class Task(BaseModel):
    """
    Task datatype
    """

    config = ConfigDict(arbitrary_types_allowed=True)

    repo_name: str
    task_id: str = Field(default_factory=lambda: generate_id())
    result: Optional[TaskResult] = Field(default=None)
    status: str = Field(default=TaskStatus.PENDING.value)
    task_args: Optional[Any]


@dataclass
class FunctionArg:
    name: str
    is_meth: bool


# REFACTOR-RUNNER: assume that all unit testing frameworks will support
# including and excluding tests
@dataclass
class RunTestTaskArgs:
    patch_file: PatchFile = field(default=None)
    exclude_tests: List[Tuple[FunctionArg, str]] = field(default_factory=list)
    include_tests: List[str] = field(default_factory=list)

    @classmethod
    def from_data(
        cls,
        patch_file: PatchFile = None,
        exclude_tests: List[Tuple[FunctionArg, str]] = [],
        include_tests: List[str] = [],
    ):
        """
        Used by server
        """
        partial = cls(patch_file, exclude_tests, include_tests)

        # if partial.patch_file:
        #     partial.patch_file.path = str(partial.patch_file["path"])
        if partial.exclude_tests:
            partial.exclude_tests = [
                (
                    FunctionArg(
                        name=func.name,
                        is_meth=func.is_meth(),
                    ),
                    str(path),
                )
                for func, path in partial.exclude_tests
            ]

        return partial

    @classmethod
    def from_json(
        cls,
        patch_file: Dict = {},
        exclude_tests: List[Tuple[Dict, str]] = [],
        include_tests: List[str] = [],
    ):
        """
        Used by client
        """
        partial = cls(patch_file, exclude_tests, include_tests)

        if partial.patch_file:
            partial.patch_file = PatchFile(
                path=Path(partial.patch_file["path"]),
                patch=partial.patch_file["patch"],
            )
        if partial.exclude_tests:
            partial.exclude_tests = [
                (
                    FunctionArg(
                        name=func["name"],
                        is_meth=func["is_meth"],
                    ),
                    Path(path),
                )
                for func, path in partial.exclude_tests
            ]

        return partial


class RunTestTaskServer(Task):
    task_args: Optional[RunTestTaskArgs]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.task_args = RunTestTaskArgs.from_data(
            patch_file=kwargs["patch_file"],
            include_tests=kwargs["include_tests"],
            exclude_tests=kwargs["exclude_tests"],
        )


class RunTestTaskClient(Task):
    task_args: Optional[RunTestTaskArgs]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.task_args = RunTestTaskArgs.from_json(
            patch_file=kwargs["patch_file"],
            include_tests=kwargs["include_tests"],
            exclude_tests=kwargs["exclude_tests"],
        )
