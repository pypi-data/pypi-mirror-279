# -*- coding: UTF-8 -*-

'''
Module
    lookup_table.py
Copyright
    Copyright (C) 2021 - 2024 Vladimir Roncevic <elektron.ronca@gmail.com>
    codecipher is free software: you can redistribute it and/or modify it
    under the terms of the GNU General Public License as published by the
    Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    codecipher is distributed in the hope that it will be useful, but
    WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
    See the GNU General Public License for more details.
    You should have received a copy of the GNU General Public License along
    with this program. If not, see <http://www.gnu.org/licenses/>.
Info
    Defines class LookUpTable with attribute(s).
    Creates lookup table class with support for encoding/decoding.
'''

from typing import List, Dict

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2024, https://electux.github.io/codecipher'
__credits__: List[str] = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/electux/codecipher/blob/main/LICENSE'
__version__ = '1.4.6'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class LookUpTable:
    '''
        Defines class LookUpTable with attribute(s) and method(s).
        Creates lookup table class with support for encoding/decoding.

        It defines:

            :attributes:
                | ALPHA - Define alphabet for encoding/decoding.
                | NUM -  Defines numeric for encoding/decoding.
                | WHITE_SPACE - Defines white space for encoding/decoding.
                | ALPHANUM - Aggregated chars for encoding/decoding.
                | LETTER_TO_INDEX - Indexed letters for encoding/decoding.
                | INDEX_TO_LETTER - Indexed letters for encoding/decoding.
            :methods:
                | None
    '''

    ALPHA: str = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    NUM: str = '0123456789'
    WHITE_SPACE: str = ' '
    ALPHANUM: str = ''.join([ALPHA, NUM, WHITE_SPACE])
    LETTER_TO_INDEX: Dict[str, int] = dict(zip(ALPHANUM, range(len(ALPHANUM))))
    INDEX_TO_LETTER: Dict[int, str] = dict(zip(range(len(ALPHANUM)), ALPHANUM))
