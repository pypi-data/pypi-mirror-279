"""Script for sorting movies folders/files into year-wise folders"""
# -*- coding: utf-8 -*-
# @author Ratnadip Adhikari

from __future__ import absolute_import
from typing import Union, List
import os
import sys
import re
import shutil
from datetime import datetime
from utils.fileopsutils import FileopsHandler
from utils.dtypesutils import DtypesOpsHandler
import logging
LOGGER = logging.getLogger(__name__)


class MoviesSorter():
    """Class for sorting movies folders/files into year-wise folders"""
    def __init__(self):
        pass  # initialized class with empty constructor

    def _form_sorting_folders(self, start_year: int, year_interval: int):
        """Form the list of year-wise sorting folders"""
        current_year = datetime.now().year
        years_list = [str(yr) for yr in range(start_year, current_year+1, year_interval)]
        if current_year % year_interval:
            years_list.append(str(current_year))
        len_range = range(len(years_list))
        sorting_folders = ["-".join(years_list[i:i+2]) for i in len_range if i+1 in len_range]
        return sorting_folders

    def _find_bracket_indices(self, text_str: str):
        """Find indices of all valid bracket pairs in a str"""
        bracket_pairs = {'(': ')', '{': '}', '[': ']'}
        bracket_stack, bracepair_ids = [], []
        for idx, char in enumerate(text_str):
            if char in bracket_pairs.keys():
                bracket_stack.append((char, idx))
            elif char in bracket_pairs.values():
                if bracket_stack and char == bracket_pairs[bracket_stack[-1][0]]:
                    bracepair_ids.append((bracket_stack.pop()[1], idx))
        return bracepair_ids

    def _find_movie_year(self, name_str: str):
        """Find the movie year from its name. The year must be inside the last bracket pair
        For e.g. -- "Black Swan[2010]", "Boys Don't Cry [1999]"
        """
        bracepair_ids = self._find_bracket_indices(name_str)
        lastbraces_ids = bracepair_ids[-1] if bracepair_ids else None
        movie_year = name_str[lastbraces_ids[0]+1: lastbraces_ids[1]] if lastbraces_ids else None
        try:
            return int(movie_year)
        except Exception:
            return

    def _sort_movie_groups(self, movie_groups: dict, sort_by='year'):
        """Sort list of movies in `movie_groups` by `sort_by` param"""
        sorted_groups = {}
        sort_idx = 1 if sort_by == 'year' else 2
        for _key, _movies in movie_groups.items():
            _key = re.sub(r'^\n\n+', '', _key)
            movies_with_yrimdb = [DtypesOpsHandler.flatten_iterable((s, re.split(r'\s+', re.sub(
                r'[^0-9\.]', ' ', s))[1:-2])) for s in _movies]
            movies_with_yrimdb = [(s[0], eval(s[1]), eval(s[2])) for s in movies_with_yrimdb]
            movies_with_yrimdb = sorted(movies_with_yrimdb, key=lambda x: x[sort_idx], reverse=True)  # sort the list
            sorted_groups[_key] = [s[0] + '\n\n' if s[0][-1] != '\n' else s[0] for s in movies_with_yrimdb]
        return sorted_groups

    def _create_formatted_movies_str(self, movie_groups: dict):
        """Create formatted movie str from list of movies in `movie_groups`"""
        format_movies_str = ""
        for _key, _movies in movie_groups.items():
            tot_movies = len(_movies)
            format_movies_str += _key if isinstance(_key, str) else ""
            item_nos = [f'{i}. ' for i in range(1, 1 + tot_movies)]
            format_movies_str += "".join([x + y for x, y in zip(item_nos, _movies)])
        return format_movies_str

    def _find_folder_for_movie(self, sorting_folders: List[str], movie_year: Union[int, None]):
        """Find the specific sorting folder for a given movie year"""
        if not (sorting_folders and movie_year):
            return ''
        for id, f in enumerate(sorting_folders):
            try:
                st_yr, end_yr = f.split('-')
                if int(st_yr) <= movie_year < int(end_yr):
                    return f
            except Exception:
                return ''

    def sort_movie_folders(self, base_folder: str, start_year: int, year_interval: int):
        """Sort individual movies to respective folders"""
        base_items = os.listdir(base_folder)
        sorting_folders = self._form_sorting_folders(start_year, year_interval)
        if not (sorting_folders and base_items):
            return
        [os.makedirs(os.path.join(base_folder, f), exist_ok=True) for f in sorting_folders]
        movieyrs_dict = {f: self._find_folder_for_movie(sorting_folders, self._find_movie_year(f)) for f in base_items}
        movement_status = {"moved": [], "not_moved": []}  # dict to track movement success of movie folders
        for movie_name, sort_folder in movieyrs_dict.items():
            try:
                shutil.move(os.path.join(base_folder, movie_name), os.path.join(base_folder, sort_folder))
                movement_status["moved"].append(movie_name)
            except Exception:
                movement_status["not_moved"].append(movie_name)
        # Finally remove the empty folders from 'sorting_folders', which are left adter the sorting process
        for f in sorting_folders:
            try:
                os.rmdir(os.path.join(base_folder, f))
            except Exception:
                pass
        self.movement_status = movement_status

    def sort_movie_listing(self, listing_path: str, sort_by='year'):
        """Sort list of movies, saved as a text file. Sorting to be done by 'year' or 'imdb'."""
        movement_status, sorted_movies_str = "", ""
        _dir, _filename = os.path.dirname(listing_path), os.path.splitext(os.path.basename(listing_path))[0]
        movies_listing, movie_groups, group_name = FileopsHandler.import_file(listing_path), {}, ""
        movie_names = re.split(r'\d+\.\s', movies_listing)  # split on numberings -- "1.", "2." etc.
        movie_names = DtypesOpsHandler.flatten_iterable(
            [[s + '[IMDB]' if not i and 'IMDB' in _str else s for i, s in enumerate(
                _str.split('[IMDB]', 1))] for _str in movie_names])  # split on '[IMDB]'
        movie_names = [x + y if bool(re.fullmatch(r'\n+', y)) else x for x, y in zip(movie_names[:-1], movie_names[1:])]
        movie_names = [s for s in movie_names if s and not bool(re.fullmatch(r'\n+', s))]
        # Group the movies category-wise
        for idx, _name in enumerate(movie_names):
            if any(_char.isdigit() for _char in _name):
                movie_groups.update({group_name: [_name]}) if not movie_groups.get(
                    group_name) else movie_groups[group_name].append(_name)
            else:
                group_name = _name
        movie_groups = self._sort_movie_groups(movie_groups, sort_by)  # Sort 'movie_groups' based on 'sort_by' param
        sorted_movies_str = self._create_formatted_movies_str(movie_groups)  # final formatted movies
        movement_status = FileopsHandler.save_files(sorted_movies_str, _dir, f'{_filename}_sorted', '.txt')
        if movement_status:
            tot_movies = sum([len(v) for k, v in movie_groups.items()])
            movement_status = "Total {} movie names sorted and saved successfully !".format(tot_movies)
        self.movement_status = movement_status


if __name__ == '__main__':
    print('python version:', sys.version)
    print('cwd:', os.getcwd())
