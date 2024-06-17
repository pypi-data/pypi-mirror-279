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
    Defines class AlephTawBetShinDecode with attribute(s) and method(s).
    Creates decode class with backend API.
'''

from dataclasses import dataclass, field
from base64 import b64decode
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
class B64Decode:
    '''
        Defines class AlephTawBetShinDecode with attribute(s) and method(s).
        Creates decode class with backend API.

        It defines:

            :attributes:
                | _decode_data - Data decode container.
            :methods:
                | decode_data - Property methods for decode data.
                | decode - Decode data from AlephTawBetShin format.
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

            :param decode_data: Decoded data
            :type decode_data: <str> | <NoneType>
            :return: None
            :exceptions: None
        '''
        if bool(decode_data):
            self._decode_data = decode_data

    def decode(self, data: str | None) -> None:
        '''
            Decoding data from AlephTawBetShin format.

            :param data: Data which should be decoded | None
            :type data: <str> | <NoneType>
            :return: None
            :exceptions: None
        '''
        if bool(data):
            self._decode_data = b64decode(data).decode()
