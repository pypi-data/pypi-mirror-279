# -*- coding: UTF-8 -*-
"""
:filename: whintpy.deposit.document.py
:author: Chiheb Bradai, Brigitte Bigi
:contact: contact@sppas.org
:summary: Represents a file that will be uploaded to a server.

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

from __future__ import annotations
import logging
import os
import shutil
import datetime

from ..config import ws
from ..config import TypesDealer

from .document_utils import DocumentUtils

# ---------------------------------------------------------------------------


class ImmutableDocument:
    """Ensure that instances become immutable after their creation.

    This is achieved by using _is_frozen attribute to True after the instance
    is created, preventing further modifications to its attributes.

    :example:
    >>> doc = ImmutableDocument(
    >>>           author="Alice",
    >>>           filename="Doc1.txt",
    >>>           content="a cool content",
    >>>           date=datetime.date(2024, 1, 1),
    >>>           filetype="txt")
    >>> print(doc.author)
    "Alice"
    >>> doc.author = "Bob"  # Raises AttributeError
    >>> del doc.author  # Raises AttributeError

    """

    def __init__(self, author: str,
                 filename: str,
                 content: str | bytes | None = None,
                 date: datetime.date | datetime.datetime | None = None,
                 filetype: str | None = None,
                 description: str | None = None,
                 folder_path: str | None = None,
                 downloads: int = 0):
        # Temporarily allow setting attributes
        self._is_frozen = False
        self.author = DocumentUtils.format_author(author)
        self.content = content
        self.date = date
        self.description = description
        self.folder_path = folder_path

        self.filename = DocumentUtils.format_filename(filename)
        self.filetype = DocumentUtils.get_filetype(filename) if (DocumentUtils.get_filetype(filename)
                                                                   != '') else DocumentUtils.format_filetype(filetype)
        self.file_path = os.path.join(folder_path, TypesDealer.serialize_data((author, date, filetype, filename)
                                                                              , "_"), (filename + "." + filetype)) \
            if (folder_path is not None) else None
        self.downloads = downloads
        self.folder_name = TypesDealer.clear_whitespace(
            TypesDealer.remove_diacritics_and_non_ascii(
                DocumentUtils.get_folder_name(self.author, self.filename, self.date, self.filetype)))
        # Freeze the instance
        self._is_frozen = True

    # -----------------------------------------------------------------------

    def __setattr__(self, key, value):
        """Override to prevent any attribute setter."""
        if getattr(self, "_is_frozen", False):
            raise AttributeError(f"{self.__class__.__name__} object is immutable")
        super().__setattr__(key, value)

    def __delattr__(self, key):
        """Override to prevent any attribute deletion."""
        if getattr(self, "_is_frozen", False):
            raise AttributeError(f"{self.__class__.__name__} object is immutable")
        super().__delattr__(key)

    def __str__(self):
        return f"ImmutableDocument({self.author}, {self.filename}, {self.date}, {self.filetype})"

    def __repr__(self):
        return (f"ImmutableDocument(author={self.author}, filename={self.filename}, date={self.date}, "
                f"filetype={self.filetype})")


# ---------------------------------------------------------------------------


class Document:
    """Represent a file that will be uploaded to a server.

    It is designed to handle file operations such as saving, deleting,
    and maintaining metadata associated with the file. Logging should
    be enabled to get some messages.

    Features:

    - Manage file operations including saving and deleting.
    - Store and retrieve metadata such as author, filename, date, and file type.

    :example:
    >>> # Create a new Document instance with all information
    >>> doc = Document("Alice", "Doc1.txt", content="a cool content",
    >>>                date=datetime(2024, 1, 1), filetype="txt")
    >>> # Save the document to a specified folder
    >>> doc.save_file("very_cool_folder")
    >>> # Delete the document from the specified folder
    >>> doc.delete_file("very_cool_folder")

  """

    def __init__(self, author: str,
                 filename: str,
                 content: str | bytes = None,
                 date: datetime.date | datetime.datetime | None = None,
                 filetype: str | None = None,
                 description: str | None = None,
                 folder_path: str | None = None):
        """Initialize the document with the provided parameters.

        When the document is created, it is saved in a folder with the following format:
        author_date_filetype_filename

        :Example:
        >>> # Create a document without the extension in the filename:
        >>> doc = Document("Alice", "Doc1", "Your_content", date=datetime.datetime(2023, 1, 1), filetype="txt")
        >>> # Create a document with the extension in the filename:
        >>> doc2 = Document("Alice", "Doc1.txt", "Your_content", date=datetime.date(2023, 1, 1))
        >>> # Create a document without a date and filetype:
        >>> doc1 = Document("Alice", "Doc1", "Your_content")
        >>> # save the document in a folder:
        >>> doc1.save_file("A_Cool_Folder")
        >>> # delete the document from the folder:
        >>> doc1.delete_file("A_Cool_Folder")

        :param filename: (str) The name of the file (can be provided with the extension or without it)
        :param author: (str) The author of the file
        :param content: (str) The content of the file (optional)
        :param date: (datetime|date) The date of the file (optional) (default: today)
        :param filetype: (str) The extension of the file (optional) (default: the extension extracted from the filename)
        :param description: (str) The description of the file (optional)
        :param folder_path: (str) The folder path where the file is stored (used for already stored files) (optional)

        :raises: ValueError: if the filename is too short
        :raises: TypeError: if the parameters are not in the correct format

        """
        # Check if the filename is at least 4 characters long
        if len(filename) < ws.MIN_FILE_NAME_LENGTH:
            raise ValueError("Document.__init__: filename must be at least 4 characters long.")
        if len(author) < 1 or len(filename) < 1:
            raise ValueError("Document.__init__: author and filename must be at least 1 character long.")
        # Check if the parameters are in the correct format and type
        TypesDealer.check_types("Document.__init__", [(author, str), (filename, str), (description, (str, type(None)))])
        if filetype is not None:
            TypesDealer.check_types("Document.__init__", [(filetype, str)])
        if content is not None:
            TypesDealer.check_types("Document.__init__", [(content, (str, bytes))])
        if date is not None:
            TypesDealer.check_types("Document.__init__", [(date, (datetime.datetime, datetime.date))])
        if folder_path is not None:
            TypesDealer.check_types("Document.__init__", [(folder_path, str)])

        # Format required fields
        self.__author = DocumentUtils.format_author(author)
        self.__date = DocumentUtils.format_date(date)

        # Format optional fields
        self.__filename = DocumentUtils.format_filename(filename)
        self.__filetype = DocumentUtils.get_filetype(filename) if (DocumentUtils.get_filetype(filename)
                                                                   != '') else DocumentUtils.format_filetype(filetype)

        self.__full_name = (TypesDealer.clear_string(self.__filename, ws.INVALID_CHARS_FOR_FILES) + "." +
                            self.__filetype)
        self.__content = content or None
        self.__folder_path = folder_path or None
        self.__description = description if description is not None else self.get_description()
        self.__downloads = self.get_downloads() or None
        # The path to the file
        self.__file_path = os.path.join(folder_path, self.get_folder_name(), self.__full_name) \
            if (folder_path is not None) else None

    # -----------------------------------------------------------------------
    # Getters & Setters
    # -----------------------------------------------------------------------

    def to_immutable(self) -> ImmutableDocument:
        """Return an immutable copy of the document.

        Creates and returns an immutable copy of the current Document instance.
        This ensures that the returned document cannot be modified, preserving
        its state at the time of the method call.

        """
        return ImmutableDocument(
            author=self.__author,
            filename=self.__filename,
            content=self.__content,
            date=self.__date,
            filetype=self.__filetype,
            description=self.__description,
            folder_path=self.__folder_path,
            downloads=self.__downloads
        )

    # -----------------------------------------------------------------------

    def get_author(self) -> str:
        """Return the author of the document."""
        return self.__author

    author = property(get_author, None)

    # -----------------------------------------------------------------------

    def get_filename(self) -> str:
        """Return the filename of the document, without its path."""
        return self.__filename

    filename = property(get_filename, None)

    # -----------------------------------------------------------------------

    def get_filetype(self) -> str:
        """Return the filetype of the document.

        The filetype is the extension in lower-case and without the dot.

        """
        return self.__filetype if self.__filetype is not None else ""

    filetype = property(get_filetype, None)

    # -----------------------------------------------------------------------

    def get_date(self) -> datetime.datetime | datetime.date | None:
        """Return the date associated to the document."""
        return self.__date if self.__date is not None else None

    date = property(get_date, None)

    # -----------------------------------------------------------------------

    def get_file_path(self) -> str:
        """Get the path to the document."""
        return self.__file_path if self.__file_path is not None else ""

    file_path = property(get_file_path, None)

    # -----------------------------------------------------------------------

    def get_description(self) -> str | None:
        """Return the description of the document, or a default value if the path isn't set.

        If folder_path is None, this method might return a default description or notify the user that the document needs to be saved first.

        :return: The description of the document or None if undefined

        """
        # Handle the case where no folder path is provided
        if self.__folder_path is not None:

            # Proceed if a folder path is provided
            description_file_path = os.path.join(self.__folder_path, self.get_folder_name(), "description.txt")
            if os.path.exists(description_file_path) is True:
                with open(description_file_path, "r", encoding="utf-8") as file:
                    return file.read().strip()
        return ""

    description = property(get_description, None)

    # -----------------------------------------------------------------------

    def get_folder_name(self) -> str:
        """Return the name of the folder in which the document is stored."""
        return TypesDealer.clear_whitespace(
            TypesDealer.remove_diacritics_and_non_ascii(
                DocumentUtils.get_folder_name(self.__author, self.__filename, self.__date, self.__filetype)))

    folder_name = property(get_folder_name, None)

    # -----------------------------------------------------------------------

    def get_folder_path(self) -> str:
        """Return the folder path of the document.

        :return: (str) The folder path of the document

        """
        return self.__folder_path if self.__folder_path is not None else ""

    folder_path = property(get_folder_path, None)

    # -----------------------------------------------------------------------

    def get_downloads(self) -> int:
        """Return the number of times the document was downloaded or 0.

        :return: (int) The number of downloads or -1 if error

        """
        # Handle the case where no folder path is provided
        if self.__folder_path is not None:
            download_filename = os.path.join(self.__folder_path, self.get_folder_name(), ws.DOWNLOADS_FILENAME)
            if os.path.exists(download_filename) is True:
                with open(download_filename, "r") as file:
                    try:
                        return int(file.read().strip())
                    except ValueError as e:
                        logging.error(f"Failed to read the number of downloads from the file: {e}")
            else:
                logging.warning(f"The file {ws.DOWNLOADS_FILENAME} does not exist in path: "
                                f" {os.path.join(self.__folder_path, self.get_folder_name())}")
        else:
            logging.warning("Document must be saved before its description can be accessed.")
            return -1
        return 0

    downloads = property(get_downloads, None)

    # -----------------------------------------------------------------------

    def get_content(self) -> str | bytes | None:
        """Return the content of the document.

        :return: (str|bytes|None) The content of the document

        """
        return self.__content

    # -----------------------------------------------------------------------

    def set_content(self, content: str | bytes):
        """Set the content of the document.

        :param content: (str) The content of the document

        """
        TypesDealer.check_types("Document.set_content", [(content, (str, bytes))])
        self.__content = content

    # -----------------------------------------------------------------------

    def set_description(self, description: str | None):
        """Set the description of the document and delete the existing one.

        :param description: (str) The description of the document

        """
        self.__description = ""
        TypesDealer.check_types("Document.set_description", [(description, (str, type(None)))])
        self.__description = description

    # -----------------------------------------------------------------------

    def set_folder_path(self, folder_path: str):
        """Set the folder path of the document.

        :param folder_path: (str) The folder path of the document

        """
        TypesDealer.check_types("Document.set_folder_path", [(folder_path, str)])
        if os.path.exists(folder_path):
            self.__folder_path = folder_path
        else:
            raise FileNotFoundError(f"Document.set_folder_path: folder path {folder_path} does not exist.")

    # -----------------------------------------------------------------------
    # Workers
    # -----------------------------------------------------------------------

    @staticmethod
    def create_document_by_folder_name(folder_name: list, folder_path: str = None) -> ImmutableDocument:
        """Return a Document() instance created from the given folder name.

        :param folder_name: (list) Name of a folder
        :param folder_path: (str) The path of the folder
        :raises: TypeError: An invalid given parameter
        :return: (Document) A Document instance created from the given folder name

        """
        TypesDealer.check_types("Document.get_document_by_folder_name", [(folder_name, list),
                                                                         (folder_path, (str, type(None)))])
        if len(folder_name) < 4:
            raise TypeError("Expected a name with 4 fields. Got {:d} instead.".format(len(folder_name)))
        return ImmutableDocument(
            folder_name[0],
            folder_name[3],
            date=DocumentUtils.str_to_date(folder_name[1]),
            filetype=folder_name[2],
            folder_path=folder_path)

    # -----------------------------------------------------------------------

    def save_file(self, path_name: str = "") -> bool:
        """Write the document to the disk into a folder of the given path.

        Create the folder - if any, and save the file content.

        :param path_name: (str) The path where the document has to be stored
        :raises: TypeError: invalid given folder
        :raises: OSError: path does not exist
        :raises: Exception: something went wrong while trying to save the file
        :raises: FileNotFoundError: the specified folder does not exist at the specified location
        :return: (bool) True if the document was saved, False otherwise

        """
        # Check if there is content to save.
        if self.__content is None:
            logging.error("Document.save_file: No content to save.")
            return False
        # Validate the type of path_name.
        TypesDealer.check_types("Document.save_file", [(path_name, str)])
        # Ensure the path exists.
        if not os.path.exists(path_name):
            raise OSError(f"Path {path_name} does not exist.")
        # Create the directory if it does not exist.
        dst_dir = os.path.join(path_name, self.get_folder_name())
        os.makedirs(dst_dir, exist_ok=True)
        # Prepare the file path.
        file_name = TypesDealer.remove_diacritics_and_non_ascii(TypesDealer.clear_whitespace(self.__full_name))
        file_path = os.path.join(dst_dir, file_name)

        # Determine the appropriate mode to open the file.
        write_mode = 'wb' if isinstance(self.__content, bytes) else 'w'

        # Write the content to the file.
        try:
            with open(file_path, write_mode) as file:
                file.write(self.__content)
        except Exception as e:
            logging.error(f"Failed to write to file: {e}")
            return False

        # Optionally log success and save additional information.
        if os.path.exists(file_path):
            self.__file_path = file_path
            self.__folder_path = path_name
            self.__save_metadata(dst_dir)
            logging.info(f"File {file_path} saved.")
            return True

        return False

    # -----------------------------------------------------------------------

    def __save_metadata(self, dst_dir: str = ""):
        """Save metadata like download count and description.

        :param path_name: (str) The path where the document has to be stored
        :return: (bool) True if the metadata was saved, False otherwise"""
        with open(os.path.join(dst_dir, ws.DOWNLOADS_FILENAME), "w") as file:
            file.write("0")
        if self.__description:
            with open(os.path.join(dst_dir, ws.DESCRIPTION_FILENAME), "w") as file:
                file.write(self.__description)

    # -----------------------------------------------------------------------
    def delete_file(self) -> bool:
        """Delete the document from the disk.

        :raises: TypeError: invalid given path
        :raises: OSError: path does not exist
        :raises: Exception: something went wrong while trying to delete the directory
        :raises: FileNotFoundError: the specified folder does not exist at the specified location
        :return: (bool) True if the document was deleted, False otherwise

        """
        if self.__folder_path is None:
            raise FileNotFoundError("Document.delete_file: folder path must be provided.")
        # Check if the folder is a string
        if os.path.exists(self.folder_path) is False:
            raise OSError(f"Path {self.__folder_path} does not exists.")

        directory_path = os.path.join(self.folder_path, DocumentUtils.get_folder_name(self.__author, self.__filename,
                                                                               self.__date, self.__filetype))
        # Check if the directory exists
        try:
            shutil.rmtree(directory_path)
            logging.info(f"Directory {directory_path} deleted.")
            return True
        # If the directory does not exist, raise an error
        except Exception as e:
            logging.error(f"Directory {directory_path} not deleted: {e}")
            return False

    # -----------------------------------------------------------------------

    def increment_downloads(self) -> int:
        """Increment the number of downloads of the document.

        :raises: FileNotFoundError: the specified folder does not exist at the specified location
        :return: (int) Incremented number of downloads, -1 otherwise

        """
        if self.__folder_path is None:
            raise FileNotFoundError("Document.increment_downloads: folder path must be provided.")

        # Check if the directory exists
        nb = -1
        try:
            downloads = os.path.join(self.folder_path, self.folder_name, ws.DOWNLOADS_FILENAME)
            with open(downloads, "r") as file:
                nb = int(file.read()) + 1
            with open(downloads, "w") as file:
                file.write(str(nb))

        except Exception as e:
            # If the directory/file does not exist, logging the error
            logging.error(f"Number of downloads of the document {self.get_filename()} "
                          f"not incremented: {e}")

        return nb

    # -----------------------------------------------------------------------

    def save_description(self) -> None:
        """Save the description of the document.

        :Example:
        >>> doc = Document("Alice", "Doc1", "Your_content", date=datetime.datetime(2023, 1, 1), filetype="txt")
        >>> doc.save_file("A_Cool_Folder")
        >>> doc.set_description("This is a description")
        >>> doc.save_description()

        :raises: ValueError: if the description is not provided
        :raises: FileNotFoundError: the specified folder does not exist at the specified location
        :raises: Exception: something went wrong while trying to save the description

        """
        if self.__description is None or self.__description == "":
            raise ValueError("Document.save_description: description must be provided.")
        if self.__folder_path is None:
            raise FileNotFoundError("Document.save_description: folder path must be provided.")

        directory_path = os.path.join(self.__folder_path, self.get_folder_name())

        # Check if the directory exists
        if os.path.exists(directory_path) is False:
            raise FileNotFoundError(f"The directory {directory_path} does not exist.")
        try:
            destination = os.path.join(directory_path, ws.DESCRIPTION_FILENAME)
            with open(destination, "w") as file:
                file.write(self.__description)
        except Exception as e:
            raise Exception(f"Description of the document {self.get_filename()} not saved: {e}")

    # -----------------------------------------------------------------------
    # Overloads
    # -----------------------------------------------------------------------

    def __str__(self):
        return f"Document({self.get_author()}, {self.filename}, {self.date}, {self.__filetype})"

    def __repr__(self):
        return (f"Document(author={self.get_author()}, filename={self.filename}, date={self.date}, "
                f"filetype={self.__filetype})")

    def __eq__(self, other):
        """Check equality of two documents.

        Checks if two Document instances are equal by comparing their author,
        filename, filetype, and date.

        :param other: (Document) The document to be compared
        :return: (bool) True if the two documents are equal, False otherwise

        """
        if self is other:
            return True
        if isinstance(other, (Document, ImmutableDocument)) is True:
            return (self.__author == other.author and
                    self.__filename == other.filename and
                    DocumentUtils.date_to_str(self.__date) == DocumentUtils.date_to_str(other.date) and
                    self.__filetype == other.filetype)

        return False
