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
    Defines class VigenereEncode with attribute(s) and method(s).
    Creates encode class with backend API.
'''

import sys
from dataclasses import dataclass, field
from typing import List

try:
    from codecipher.vigenere.lookup_table import LookUpTable
except ImportError as ats_error_message:
    # Force close python ATS ##################################################
    sys.exit(f'\n{__file__}\n{ats_error_message}\n')

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2024, https://electux.github.io/codecipher'
__credits__: List[str] = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/electux/codecipher/blob/main/LICENSE'
__version__ = '1.4.6'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@dataclass
class VigenereEncode:
    '''
        Defines class VigenereEncode with attribute(s) and method(s).
        Creates encode class with backend API.

        It defines:

            :attributes:
                | _encode_data - Data encode container.
            :methods:
                | encode_data - Property methods for encode data.
                | _split_data - Splitting data for encoding.
                | encode - Encode data to Vigenere format.
    '''

    _encode_data: str | None = field(default=None)

    @property
    def encode_data(self) -> str | None:
        '''
            Property method for getting encode data.

            :return: Encoded data | None
            :rtype: <str> | <NoneType>
            :exceptions: None
        '''
        return self._encode_data

    @encode_data.setter
    def encode_data(self, encode_data_val: str | None) -> None:
        '''
            Property method for setting encode data.

            :param encode_data_val: Encode data | None
            :type encode_data_val: <str> | <NoneType>
            :return: None
            :exceptions: None
        '''
        if bool(encode_data_val):
            self._encode_data = encode_data_val

    def _split_data_encode(
        self, data_to_encode: str | None, key: str | None
    ) -> List[str]:
        '''
            Splitting data for encoding.

            :param data_to_encode: Data which should be encoded | None
            :type data_to_encode: <str> | <NoneType>
            :param key: Key for encoding | None
            :type key: <str> | <NoneType>
            :return: List with data for encoding
            :rtype: <List[str]>
            :exceptions: None
        '''
        elements: List[str] = []
        if bool(data_to_encode) and bool(key):
            for i in range(0, len(data_to_encode), len(key)):
                elements.append(data_to_encode[i: i + len(key)])
        return elements

    def encode(self, data_to_encode: str | None, key: str | None) -> None:
        '''
            Encoding data to Vigenere format.

            :param data_to_encode: Data which should be encoded | None
            :type data_to_encode: <str> | <NoneType>
            :param key: Key for encoding | None
            :type key: <str> | <NoneType>
            :return: None
            :exceptions: None
        '''
        if bool(data_to_encode) and bool(key):
            encode_list: List[str] = []
            for element in self._split_data_encode(data_to_encode, key):
                for index, letter in enumerate(element):
                    process_index = (
                        LookUpTable.LETTER_TO_INDEX[letter] +
                        LookUpTable.LETTER_TO_INDEX[key[index]]
                    ) % len(LookUpTable.ALPHANUM)
                    encode_list.append(
                        LookUpTable.INDEX_TO_LETTER[process_index]
                    )
            self._encode_data = ''.join(encode_list)
