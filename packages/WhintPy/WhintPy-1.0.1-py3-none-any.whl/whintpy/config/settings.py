# -*- coding: UTF-8 -*-
"""
:filename: whintpy.config.settings.py
:author: Brigitte Bigi
:contact: contact@sppas.org
:summary: Settings for managing documents in a deposit and their accesses

.. _This file is part of WhintPy.
..
    -------------------------------------------------------------------------

    Copyright (C) 2024 Brigitte Bigi
    Laboratoire Parole et Langage, Aix-en-Provence, France

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.

    This banner notice must not be removed.

    -------------------------------------------------------------------------

"""


class WhintPySettings:
    """Initialize configuration settings for the WhintPy library.

    It sets default values for folder and file naming conventions, including
    separators, minimum lengths, and invalid characters.

    """

    def __init__(self):
        """Initialize the settings for WhintPy library.

        """
        self.__dict__ = dict(
            # Separator used to separate the parts of a document folder name
            FOLDER_NAME_SEPARATOR='_',

            # Minimum length of a file name
            MIN_FILE_NAME_LENGTH=4,

            # Invalid characters for folder names
            INVALID_CHARS_FOR_FOLDERS="/\\._$@#%&*()[]{}<>:;,?\"'`!^+=|~",

            # Invalid characters for file names
            INVALID_CHARS_FOR_FILES="/\\_$@#%&*()[]{}<>:;,?\"'`!^+=|~",

            # Default filenames
            DOWNLOADS_FILENAME="downloads.txt",
            DESCRIPTION_FILENAME="description.txt"

        )
        self._is_frozen = True

    # -----------------------------------------------------------------------

    def freeze(self):
        super().__setattr__('_is_frozen', True)

    # -----------------------------------------------------------------------

    def unfreeze(self):
        super().__setattr__('_is_frozen', False)

    # -----------------------------------------------------------------------

    def __setattr__(self, key, value):
        """Override to prevent any attribute setter."""
        if getattr(self, "_is_frozen", False):
            raise AttributeError(f"{self.__class__.__name__} object is immutable")
        super().__setattr__(key, value)

    # -----------------------------------------------------------------------

    def __delattr__(self, key):
        """Override to prevent any attribute deletion."""
        raise AttributeError(f"{self.__class__.__name__} object does not allow attribute deletion")

    # -----------------------------------------------------------------------

    def __enter__(self):
        """Override to allow the use of 'with'."""
        return self

    # -----------------------------------------------------------------------

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    # -----------------------------------------------------------------------

    def __iter__(self):
        """Browse through the class attributes."""
        for item in self.__dict__.keys():
            yield item
