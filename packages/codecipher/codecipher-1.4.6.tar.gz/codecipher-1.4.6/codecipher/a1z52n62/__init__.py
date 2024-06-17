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
    Defines class A1z52N62 with attribute(s) and method(s).
    Creates container class with aggregate backend API.
'''

import sys
from typing import List

try:
    from codecipher.a1z52n62.encode import A1z52N62Encode
    from codecipher.a1z52n62.decode import A1z52N62Decode
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


class A1z52N62(A1z52N62Encode, A1z52N62Decode):
    '''
        Defines class A1z52N62 with attribute(s) and method(s).
        Creates container class with aggregate backend API.

        It defines:

            :attributes:
                | None.
            :methods:
                | __init__ - Initials A1z52N62 constructor.
    '''

    def __init__(self) -> None:
        '''
            Initials A1z52N62 constructor.

            :exceptions: None
        '''
        super().__init__()
