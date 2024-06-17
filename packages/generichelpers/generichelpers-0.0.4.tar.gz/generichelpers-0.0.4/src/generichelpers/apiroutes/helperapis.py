"""Flask apis to perform automated operations"""

import traceback
from devs.movies_sorter import MoviesSorter
from flask import Blueprint, request, abort, jsonify

bp = Blueprint('aryajobs', __name__)


@bp.route('/moviefolders_sorter', methods=['GET'], strict_slashes=False)
def moviefolders_sorter():
    """Movies folder sorter api func
    URL = http://127.0.0.1:1501/moviefolders_sorter?base_path=/path&start_year=1950&year_interval=10
    """
    try:
        response = {}
        movie_sorter = MoviesSorter()  # call the movies sorter class
        # Access input params
        base_path = request.args.get('base_path')
        start_year = int(request.args.get('start_year'))
        year_interval = int(request.args.get('year_interval'))
        movie_sorter.sort_movie_folders(base_path, start_year, year_interval)
        response = movie_sorter.movement_status
    except Exception:
        response = {
            "message": "Failed in sorting movies in the base folder !",
            "error": traceback.format_exc()
        }
    return jsonify(response)


@bp.route('/movielist_sorter', methods=['GET'], strict_slashes=False)
def movielist_sorter():
    """Movies list sorter api func
    URL = http://127.0.0.1:1501/movielist_sorter?base_path=/path/file.txt&sort_by=imdb
    """
    try:
        response = {}
        movie_sorter = MoviesSorter()  # call the movies sorter class
        # Access input params
        base_path = request.args.get('base_path')
        sort_by = request.args.get('sort_by')
        movie_sorter.sort_movie_listing(base_path, sort_by)
        response = movie_sorter.movement_status
    except Exception:
        response = {
            "message": "Failed in sorting movies list",
            "error": traceback.format_exc()
        }
    return jsonify(response)
