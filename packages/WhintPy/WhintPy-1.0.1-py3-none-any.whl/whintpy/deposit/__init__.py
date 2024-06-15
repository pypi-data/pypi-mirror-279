"""
:filename: whintpy.deposit.__init__.py
:author: Brigitte Bigi, Chiheb Bradai
:contact: contact@sppas.org
:summary: A management system for shared documents.

.. _This file is part of WhintPy.
..
    -------------------------------------------------------------------------

    ██╗    ██╗ ██╗  ██╗ ██╗ ███╗   ██╗ ████████╗ ██████╗  ██╗   ██╗
    ██║    ██║ ██║  ██║ ██║ ████╗  ██║ ╚══██╔══╝ ██╔══██╗ ╚██╗ ██╔╝
    ██║ █╗ ██║ ███████║ ██║ ██╔██╗ ██║    ██║    ██████╔╝  ╚████╔╝
    ██║███╗██║ ██╔══██║ ██║ ██║╚██╗██║    ██║    ██╔═══╝    ╚██╔╝
    ╚███╔███╔╝ ██║  ██║ ██║ ██║ ╚████║    ██║    ██║         ██║
     ╚══╝╚══╝  ╚═╝  ╚═╝ ╚═╝ ╚═╝  ╚═══╝    ╚═╝    ╚═╝         ╚═╝

            a Python library for managing shared files

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

from .document_utils import DocumentUtils
from .document import Document
from .document import ImmutableDocument
from .docsfilters import DocumentsFilters
from .documents_manager import DocumentsManager

__all__ = (
    "Document",
    "ImmutableDocument",
    "DocumentUtils",
    "DocumentsFilters",
    "DocumentsManager"
)
