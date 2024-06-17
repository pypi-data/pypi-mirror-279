# -*- coding: UTF-8 -*-

'''
Module
    encode.py
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
    Defines class A1z52N62Encode with attribute(s) and method(s).
    Creates encode class with backend API.
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
class A1z52N62Encode:
    '''
        Defines class A1z52N62Encode with attribute(s) and method(s).
        Creates encode class with backend API.

        It defines:

            :attributes:
                | _encode_data - Data encode container.
            :methods:
                | encode_data - Property methods for encode data.
                | encode - Encode data to A1z52N62 format.
    '''

    _encode_data: str | None = field(default=None)

    @property
    def encode_data(self) -> str | None:
        '''
            Property method for getting encode data.

            :return: Encoded data
            :rtype: <str> | <NoneType>
            :exceptions: None
        '''
        return self._encode_data

    @encode_data.setter
    def encode_data(self, encode_data: str | None) -> None:
        '''
            Property method for setting encode data.

            :param encode_data: Encode data | None
            :type encode_data: <str> | <NoneType>
            :return: None
            :exceptions: None
        '''
        if bool(encode_data):
            self._encode_data = encode_data

    def encode(self, data: str | None) -> None:
        '''
            Encoding data to A1z52N62 format.

            :param data: Data which should be encoded | None
            :type data: <str> | <NoneType>
            :return: None
            :exceptions: None
        '''
        if bool(data):
            encode_list: List[str] = []
            for element in data:
                if element.isalpha():
                    if element.isupper():
                        encode_list.append(str(ord(element) - 64))
                    else:
                        encode_list.append(str(ord(element) - 96 + 27))
                else:
                    if element.isnumeric():
                        encode_list.append(str(int(element) + 53))
                    else:
                        encode_list.append(element)
            self._encode_data = ' - '.join(encode_list)
