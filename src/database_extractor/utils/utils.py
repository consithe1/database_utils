import itertools
import os
import re
import sys


import database_extractor.utils.constants as constants


def dict_factory(cursor, row):
    fields = [column[0] for column in cursor.description]
    return {key: value for key, value in zip(fields, row)}


all_chars = (chr(i) for i in range(sys.maxunicode))
categories = {'Cc', 'Cf', 'Cs', 'Co', 'Cn'}
control_chars = ''.join(map(chr, itertools.chain(range(0x00, 0x20), range(0x7f, 0xa0))))
control_char_re = re.compile('[%s]' % re.escape(control_chars))


def remove_control_chars(s):
    return control_char_re.sub('', s)


def winapi_path(dos_path):
    """
    Function to add the windows path extension to allow longer paths
    :param dos_path: the base path
    :return: a string of a path
    """
    path = os.path.abspath(dos_path)
    if path.startswith(u"\\\\"):
        return u"\\\\?\\UNC\\" + path[2:]
    return u"\\\\?\\" + path


def convert_multidimensional_to_single_dimensional(values: any, elem_key: str = "") -> dict[str, any]:
    # a 1-dimension row
    one_dimension_row: dict[str, any] = {}

    if isinstance(values, dict):
        for key_elem, elem in values.items():
            sub_key = f"{elem_key} {constants.SEP_KEY_CHAR} {key_elem}" if elem_key else f"{key_elem}"
            one_dimension_row |= convert_multidimensional_to_single_dimensional(values=elem, elem_key=sub_key)
    elif isinstance(values, list) or isinstance(values, tuple):
        for index_elem, elem in enumerate(values):
            sub_key = f"{elem_key} {constants.SEP_KEY_CHAR} {index_elem}" if elem_key else f"{index_elem}"
            one_dimension_row |= convert_multidimensional_to_single_dimensional(values=elem, elem_key=sub_key)
    else:
        one_dimension_row |= {elem_key: values}

    return one_dimension_row
