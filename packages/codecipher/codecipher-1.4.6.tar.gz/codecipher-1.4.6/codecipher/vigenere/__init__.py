# -*- coding: UTF-8 -*-

'''
Module
    __init__.py
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
    Defines class Vigenere with attribute(s) and method(s).
    Creates container class with aggregate backend API.
'''

import sys
from typing import List

try:
    from codecipher.vigenere.encode import VigenereEncode
    from codecipher.vigenere.decode import VigenereDecode
    from codecipher.vigenere.key_generator import KeyGenerator
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


class Vigenere(VigenereEncode, VigenereDecode, KeyGenerator):
    '''
        Defines class Vigenere with attribute(s) and method(s).
        Creates container class with aggregate backend API.

        It defines:

            :attributes:
                | None.
            :methods:
                | __init__ - Initials Vigenere constructor.
    '''

    def __init__(self) -> None:
        '''
            Initials Vigenere constructor.

            :exceptions: None
        '''
        super().__init__()
