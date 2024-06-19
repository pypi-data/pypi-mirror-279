from cowboy.http import APIClient
from cowboy.db.core import Database


db = Database()
api = APIClient(db)


def api_build_tm_mapping(repo_name, mode, files, tms):
    """
    Builds the test module to source file mapping for each selected
    test module
    """
    api.long_post(
        "/tm/build-mapping",
        {
            "repo_name": repo_name,
            "mode": mode,
            "tms": tms,
            "files": files,
            "overwrite": False,
        },
    )
