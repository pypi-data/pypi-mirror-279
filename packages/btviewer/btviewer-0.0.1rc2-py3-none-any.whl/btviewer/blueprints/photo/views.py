from pathlib import Path

import flask

from .model import Photo

app: flask.Flask = flask.current_app
blueprint = flask.Blueprint('photo', __name__, url_prefix='/photos')


@blueprint.route('<path:path>.tiff')
@blueprint.route('<path:path>.tif')
def image_tiff(path: str):
    """
    /photos/<session>/<set>/<device id>/<camera id>/<timestamp>_<photo id>.tiff
    """
    photo = Photo(path + ".np")

    # TIFF image data
    return flask.send_file(photo.to_tiff(), mimetype='image/tiff', as_attachment=False)


@blueprint.route('<path:path>.png')
def image_png(path: str):
    """
    /photos/<session>/<set>/<device id>/<camera id>/<timestamp>_<photo id>.png
    """
    photo = Photo(path + ".np")

    # Return the image as a PNG file
    return flask.send_file(photo.to_png(), mimetype='image/png', as_attachment=False)


@blueprint.route('<path:path>.jpeg')
@blueprint.route('<path:path>.jpg')
def image_jpeg(path: str):
    photo = Photo(path + ".np")

    # Return the image as a PNG file
    return flask.send_file(photo.to_jpeg(), mimetype='image/jpeg', as_attachment=False)


@blueprint.route('/<path:path>.json')
def detail(path: str):
    """
    Show the photo metadata

    :param path: The path of the data file
    :return:
    """
    photo = Photo(path + '.np')
    return flask.jsonify(photo.metadata)
