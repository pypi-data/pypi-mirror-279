from cowboy_lib.utils import gen_random_name
from cowboy_lib.repo.diff import CommitDiff

import os
import tempfile
import hashlib
from pathlib import Path
from logging import getLogger
from git import Repo, GitCommandError
from dataclasses import dataclass
import shutil
import random
from typing import List, Union, Tuple

logger = getLogger("test_results")


class NoRemoteException(Exception):
    pass


class NoMainBranch(Exception):
    pass


def del_file(func, path, exc_info):
    """
    Error handler for ``shutil.rmtree``.

    If the error is due to an access error (read only file)
    it attempts to add write permission and then retries.

    If the error is for another reason it re-raises the error.

    Usage : ``shutil.rmtree(path, onerror=onerror)``
    """
    import stat

    # Is the error an access error?
    if not os.access(path, os.W_OK):
        os.chmod(path, stat.S_IWUSR)
        func(path)
    else:
        raise


class GitRepo:
    """
    Used to manage git operations on a git repo
    """

    def __init__(self, repo_path: Path, remote: str = "origin", main: str = "main"):
        if not repo_path.exists():
            # test suite may be renamed or deleted
            raise Exception("GitRepo does not exist: ", repo_path)

        # used for reversing patches
        self.patched_files = {}
        self.repo_folder = repo_path
        self.repo = Repo(repo_path)
        self.head = self.repo.head

        # checks if main branch and remote exists
        if not self.branch_exists(main):
            raise NoMainBranch(main)
        self.main = main
        try:
            self.origin = self.repo.remotes.__getattr__(remote)
        except AttributeError:
            raise NoRemoteException(remote)

        self.username = self.origin.url.split("/")[-2]
        self.repo_name = self.origin.url.split("/")[-1]

        self.branch_prefix = "cowboy_"

    @classmethod
    def clone_repo(cls, clone_dst: Path, url: str) -> Path:
        """
        Creates a clone of the repo locally
        """
        if not os.path.exists(clone_dst):
            os.makedirs(clone_dst)  # Ensure the destination folder exists

        Repo.clone_from(url, clone_dst)
        return cls(clone_dst)

    @classmethod
    def delete_repo(cls, repo_dst: Path):
        """
        Deletes a repo from the db and all its cloned folders
        """
        import platform

        if not repo_dst.exists():
            return

        if platform.system() == "Windows":
            shutil.rmtree(repo_dst, onerror=del_file)
        else:
            shutil.rmtree(repo_dst)

    def commit_exists(self, commit_sha: str) -> bool:
        """
        Checks if a commit exists in the repo
        """
        try:
            self.repo.commit(commit_sha)
            return True
        except Exception:
            return False

    def get_curr_commit(self):
        """
        Returns the current commit sha
        """
        return self.head.commit.hexsha

    def reset_to_commit(self, commit_sha, parent=None):
        """
        Resets the index of the repository to a specific commit.
        """
        self.repo.git.reset("--hard", commit_sha)
        return f"Successfully reset to commit {commit_sha}"

    def get_prev_commit(self, commit_sha):
        """
        Returns the previous commit of a given commit sha
        """
        return self.repo.commit(commit_sha).parents[0]

    def apply_patch(self, patch: str) -> None:
        """
        Applies a patch from a .diff file to a single file in the repository
        """
        with tempfile.NamedTemporaryFile(mode="wb", delete=False) as patch_file:
            patch_file.write(patch.encode("utf-8") + b"\n")
            patch_file.flush()

        patch_hash = hashlib.md5(patch.encode("utf-8")).hexdigest()
        self.repo.git.apply(patch_file.name, whitespace="nowarn")
        self.patched_files[patch_hash] = patch_file.name

    def reverse_patch(self, patch: str) -> None:
        """
        Reverses a patch from a .diff
        """
        patch_hash = hashlib.md5(patch.encode()).hexdigest()
        patch_file = self.patched_files[patch_hash]

        self.repo.git.apply(patch_file, reverse=True)
        self.patched_files.pop(patch_hash)

    def branch_exists(self, branch: str):
        """
        Checks if a branch exists in the repo
        """
        if branch in [str(br) for br in self.repo.heads]:
            return True

        return False

    def clean_branches(self, branch_prefix: str):
        """
        Deletes all branches with a specific prefix
        """
        removed = []
        for branch in self.repo.branches:
            if branch.name.startswith(branch_prefix):
                removed.append(branch.name)
                self.repo.delete_head(branch)

        return removed

    def diff_remote(self) -> Tuple[List[str], List[str]]:
        """
        Diffs the remote with our local repo
        """
        try:
            # Open the repository
            self.repo.remotes.origin.fetch()
            local_commit = self.repo.head.commit.hexsha
            remote_commit = self.repo.remotes.origin.refs.__getattr__(
                self.main
            ).commit.hexsha

            # Check if there is an update
            if local_commit == remote_commit:
                print("No updates available.")
            else:
                print("Updates found!")
                # Pull the latest changes
                # repo.remotes.origin.pull()

                # Get the new HEAD commit after pull
                # new_commit = repo.head.commit.hexsha

                # Get the diff between the old commit and the new HEAD
                diff = self.repo.git.diff(local_commit, remote_commit)
                commit_diff = CommitDiff(diff)

                return commit_diff
        except Exception as e:
            print(f"An error occurred: {e}")
            return [], []

    def checkout_and_push(
        self,
        name: str,
        commit_message: str,
        files_to_commit: list,
    ):
        """
        Checks out a new branch, commits changes, and pushes to the remote. Returns the
        URL for the merge request of our new branch against main

        Args:
        - name: The "suggested" name
        - commit_message: The commit message to use.
        - files_to_commit: List of file paths (relative to the repo root) to commit.

        Returns:
        - None
        """
        branch_name = name
        if self.branch_exists(name):
            branch_name = self.branch_prefix + name + "_" + gen_random_name()

        # Check out a new branch
        new_branch = self.repo.create_head(branch_name)
        new_branch.checkout()

        # Add and commit changes
        self.repo.index.add(files_to_commit)
        self.repo.index.commit(commit_message)

        print("Pushing to remote: ", self.origin)
        self.origin.push(refspec=f"{branch_name}:{branch_name}")
        origin_url = self.origin.url.replace(".git", "")

        # url for branch merge request
        return f"{origin_url}/compare/{self.main}...{self.username}:{self.repo_name}:{branch_name}?expand=1"


class PatchApplyExcepion(Exception):
    pass


class IncompatibleCommit(Exception):
    pass


# TODO: add __str__ and then use str() in method
@dataclass
class PatchFile:
    path: Path
    patch: str


class PatchFileContext:
    """
    Context manager for applying and reversing patches
    """

    def __init__(
        self, repo: GitRepo, patch: Union[str, PatchFile], revert: bool = True
    ):

        self.repo = repo
        self.patch = patch
        # assume all cases repo and patch are both specified, or neither are
        self.head_commit = self.repo.head.commit if self.patch else None
        self.failed_id = random.randint(0, 1000000)
        # for debugging
        self.revert = revert

    # def _write_broken_patch(self):
    #     with open(
    #         f"log/failed_patches/patch_{self.failed_id}.diff", "w+", encoding="utf-8"
    #     ) as f:
    #         f.write(self.patch)

    def __enter__(self):
        if not self.patch:
            return

        try:
            if isinstance(self.patch, PatchFile):
                with open(self.patch.path, "w", encoding="utf-8") as f:
                    f.write(self.patch.patch)
            elif isinstance(self.patch, str):
                self.repo.apply_patch(self.patch)

        except GitCommandError as e:
            # self._write_broken_patch()
            raise PatchApplyExcepion(e)

    def __exit__(self, exc_type, exc_value, traceback):
        if not self.patch:
            return

        try:
            if isinstance(self.patch, PatchFile) and self.revert:
                self.repo.reset_to_commit(self.head_commit)
            elif isinstance(self.patch, str) and self.revert:
                self.repo.reverse_patch(self.patch)

        except GitCommandError as e:
            logger.info(f"Error reversing patch")
            raise PatchApplyExcepion(e)


class RepoCommitContext:
    """
    Resets the repository to a specific commit
    """

    def __init__(self, repo: GitRepo, fd_reset: bool = False, revert: bool = True):
        self.repo = repo
        self.revert = revert
        self.fd_reset = fd_reset

    def __enter__(self):
        """
        Saves the current commit hash when entering the context.
        """
        self.original_commit = self.repo.head.commit.hexsha
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Restores the repository to the original commit when exiting the context.
        """
        if exc_type is not None:
            print(f"An exception occurred: {exc_type.__name__}: {exc_value}")
            # Optionally, log the traceback here

        if self.fd_reset:
            self._add_files()

        if self.original_commit and self.revert:
            self.repo.reset_to_commit(self.original_commit)

        # reset the patched files in GitRepo
        self.repo.patched_files = {}

    def _add_files(self):
        """
        Adds all files in repo so that they are tracked by git and can be resetted
        when the context is exited
        """
        self.repo.repo.git.add(".")
        print(self.repo.repo.git.status())

    def reset_to_commit(self, commit_sha: str, parent=None):
        """
        Resets the index of the repository to a specific commit.
        """
        return self.repo.reset_to_commit(commit_sha, parent)
