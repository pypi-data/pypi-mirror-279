from abc import ABC, abstractmethod
from cowboy_lib.api.runner.shared import RunTestTaskArgs
from cowboy_lib.coverage import CoverageResult

from typing import Tuple, List, Any


class TestSuiteError(Exception):
    """
    Stderr from the subprocess that runs the lang/framework unit test suite
    """

    def __init__(self, stderr: str):
        super().__init__(stderr)
        self.stderr = stderr

    # Not actually used for some reason
    def __str__(self):
        return "TestSuit Error: " + self.stderr


class Runner(ABC):
    """
    Runs the lang/framework specific unit test
    """

    @abstractmethod
    def run_testsuite(self, args: RunTestTaskArgs) -> Tuple[CoverageResult, str, str]:
        """
        Runs the lang/framework specific unit test suite
        """
        raise NotImplementedError

    def _construct_cmd(
        self,
        repo_path,
        selected_args_str: str = "",
        deselected_args_str: str = "",
    ):
        """
        Constructs the cmd for running the test via subprocess
        """
        raise NotImplementedError

    def _get_include_tests_arg_str(self, include_tests: List[str] = []):
        """
        Constructs the arg string for selecting specific tests
        """
        raise NotImplementedError

    def _get_exclude_tests_arg_str(self, exclude_tests: List[Any]):
        """
        Constructs the arg string for excluding specific tests
        """
        raise NotImplementedError
