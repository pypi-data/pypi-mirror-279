# -*- coding: utf-8 -*-

from .change_pr_units import is_precipitation, change_pr_units


def change_units(cube_or_coord, new_units, new_standard_name=None):
    if is_precipitation(new_standard_name):
        change_pr_units(cube_or_coord, new_units, new_standard_name)
    else:
        cube_or_coord.convert_units(new_units)


__all__ = [
    change_units,
]
