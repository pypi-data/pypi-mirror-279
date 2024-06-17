# -*- coding: UTF-8 -*-

'''
Module
    decode.py
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
    Defines class CaesarDecode with attribute(s) and method(s).
    Creates decode class with backend API.
'''

from dataclasses import dataclass, field
from typing import List

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2024, https://electux.github.io/codecipher'
__credits__: List[str] = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/electux/codecipher/blob/main/LICENSE'
__version__ = '1.4.6'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@dataclass
class CaesarDecode:
    '''
        Defines class CaesarDecode with attribute(s) and method(s).
        Creates decode class with backend API.

        It defines:

            :attributes:
                | _decode_data - Data decode container.
            :methods:
                | decode_data - Property methods for decode data.
                | decode - Decode data from Caesar format.
    '''

    _decode_data: str | None = field(default=None)

    @property
    def decode_data(self) -> str | None:
        '''
            Property method for getting decode data.

            :return: Decode data in str format | None
            :rtype: <str> | <NoneType>
            :exceptions: None
        '''
        return self._decode_data

    @decode_data.setter
    def decode_data(self, decode_data: str | None) -> None:
        '''
            Property method for setting decode data.

            :param decode_data: Decoded data | None
            :type decode_data: <str> | <NoneType>
            :return: None
            :exceptions: None
        '''
        if bool(decode_data):
            self._decode_data = decode_data

    def decode(self, data: str | None, shift_counter: int | None) -> None:
        '''
            Decoding data from Caesar format.

            :param data: Data which should be decoded | None
            :type data: <str> | <NoneType>
            :param shift_counter: Defining the shift count | None
            :type shift_counter: <int> | <NoneType>
            :return: None
            :exceptions: None
        '''
        if bool(data) and bool(shift_counter):
            decode_list: List[str] = []
            for element in data:
                if element.isspace() or element.isnumeric():
                    decode_list.append(element)
                    continue
                element_index: int | None = None
                new_index: int | None = None
                new_unicode: int | None = None
                new_character: str | None = None
                if element.isupper():
                    element_index = ord(element) - ord('A')
                    new_index = (element_index - shift_counter) % 26
                    new_unicode = new_index + ord('A')
                else:
                    element_index = ord(element) - ord('a')
                    new_index = (element_index - shift_counter) % 26
                    new_unicode = new_index + ord('a')
                new_character = chr(new_unicode)
                decode_list.append(new_character)
            self._decode_data = ''.join(decode_list)
