from pathlib import Path

import flask

from .models import Session

app: flask.Flask = flask.current_app

blueprint = flask.Blueprint('session', __name__, url_prefix='/sessions')


@blueprint.route('/_all_cameras')
def list_all_cameras():
    """
    DEVELOPMENT ONLY - THIS WILL BE REMOVED

    List all data subdirectories
    """

    root_directory = Path(app.config['ROOT_DIRECTORY'])
    # Get camera data subdirectories (nested four deep)
    camera_directories = (path for path in root_directory.glob("*/*/*/*") if path.is_dir())
    # Convert paths to strings
    camera_directories = tuple(str(path.relative_to(root_directory).as_posix()) for path in camera_directories)
    return flask.jsonify(camera_directories)


@blueprint.route("/")
def list_():
    """
    This an API endpoint to list all sessions.
    It lists all available session folders in the root directory.

    btviewer ~/my_data/<session>
    where the root directory is ~/my_data/

    :returns: JSON list of session identifiers
    [
        "my_session_1",
        "my_session_2",
        "my_session_3"
    ]
    """
    sessions = tuple((str(session) for session in Session.iter_sessions()))

    # Return JSON response to browser
    return flask.jsonify(sessions)


@blueprint.route("/<path:relative_path>")
def list_path(relative_path: str):
    """
    List directory contents of _any_ data subdirectory

    <root_directory>/<session>/<set>/<device id>/<camera id>/<timestamp>_<photo id>.np
    """

    root_directory = Session.root_directory()
    relative_path = Path(relative_path)
    path: Path = root_directory.joinpath(relative_path)

    # Are we in a camera directory that contains photos?
    # (i.e. Are we at least four subdirectories deep in the file structure?)
    if len(relative_path.parents) >= 4:
        # Get photo files
        file_paths = path.glob("*.np")
        file_names = tuple(str(path.relative_to(root_directory).as_posix()) for path in file_paths)
        return flask.jsonify(file_names)

    else:
        # Get subdirectory names
        subdir_paths = (path for path in path.iterdir() if path.is_dir())
        subdir_names = tuple(str(path.relative_to(root_directory).as_posix()) for path in subdir_paths)
        return flask.jsonify(subdir_names)
