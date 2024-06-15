# -*- coding: UTF-8 -*-
"""
:filename: whintpy.deposit.document_manager.py
:author: Brigitte Bigi, Chiheb Bradai
:contact: contact@sppas.org
:summary: Management of a bunch of documents.

.. _This file is part of WhintPy: https://whintpy.sourceforge.io
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
from datetime import datetime

from ..config.typesdealer import TypesDealer
from ..config import ws

from .document import Document, ImmutableDocument
from .docsfilters import DocumentsFilters

# ---------------------------------------------------------------------------


class DocumentsManager:

    def __init__(self, folder_path: str = "."):
        """Initialize the DocumentManager.

        :example:
        >>> manager = DocumentsManager('test_folder')
        >>> manager.collect_docs()
        >>> print(manager.get_docs_sorted_by_newest())
        >>> # Assuming your_document is a document in the folder
        >>> manager.get_doc_content(your_document)
        >>> print(your_document.get_content())  # The content of the document is printed
        >>> manager.delete(your_document)
        >>> print(manager.get_docs_sorted_by_newest())  # The document is deleted

        :param folder_path: (str) The folder path to collect the documents from and write documents into
        :raises: TypeError: Invalid folder path type
        :raises: FileNotFoundError: The specified folder does not exist at the specified location

        """
        TypesDealer.check_types("DocumentManager.__init__", [(folder_path, str)])
        if os.path.exists(folder_path) is False:
            raise FileNotFoundError(f"The specified folder does not exist at the specified "
                                    f"location ({folder_path}).")
        self.__folder_path = folder_path
        self.__docs = list()

    # -----------------------------------------------------------------------

    def get_folder_path(self) -> str:
        """Return the folder path.

        :example:
        >>> doc1 = DocumentsManager('test_folder')
        >>> print(doc1.get_folder_path())  # test_folder

        :return: (str) The folder path

        """
        return self.__folder_path

    # -----------------------------------------------------------------------
    # Management of the list of documents
    # -----------------------------------------------------------------------

    def collect_docs(self) -> None:
        """Collect all documents from the folder path.

        :example:
        >>> manager = DocumentsManager('test_folder')
        >>> manager.collect_docs()
        >>> print([doc for doc in manager])

        :raises: FileNotFoundError: The specified folder does not exist at the specified location
        :raises: FileNotFoundError: No documents found in the folder

        """
        if os.path.exists(self.__folder_path) is False:
            raise FileNotFoundError(f"The specified folder does not exist at the specified "
                                    f"location ({self.__folder_path}).")

        for entry in os.scandir(self.__folder_path):
            if entry.is_dir() is True:
                folder_name = entry.name
                parts = folder_name.split(ws.FOLDER_NAME_SEPARATOR)
                if len(parts) >= 4:
                    document = Document(parts[0], date=datetime.strptime(parts[1], "%Y-%m-%d"), filetype=parts[2],
                                        filename=parts[3], folder_path=self.__folder_path)
                    self.__docs.append(document)

    # -----------------------------------------------------------------------

    def clear_docs(self):
        """Clear the list of documents.

        :example:
        >>> manager = DocumentsManager('test_folder')
        >>> manager.collect_docs()
        >>> manager.clear_docs()
        >>> print([doc for doc in manager])
        []

        """
        self.__docs.clear()

    # -----------------------------------------------------------------------

    def add(self, author: str, filename: str, **kwargs) -> ImmutableDocument:
        """Create and add a document to the list of documents.

        :example:
        >>> doc1 = DocumentsManager('test_folder')
        >>> doc1.collect_docs()
        >>> # Assuming your_document is a document
        >>> doc1.add_doc(your_document)
        >>> print(doc1.is_in_docs(your_document))
        True

        :param author: (str) The document author
        :param filename: (str) The document filename
        :param kwargs: (dict) The keyword arguments to create the Document()
        :raises: TypeError: Cant create the document
        :raises: ValueError: Cant create the document
        :return: (ImmutableDocument) The created document

        """
        doc = Document(author, filename, **kwargs)
        self.__docs.append(doc)
        return ImmutableDocument(author, filename, **kwargs)

    # -----------------------------------------------------------------------

    def add_doc(self, doc: Document | ImmutableDocument) -> None:
        """Add a document to the list of documents.

        :example:
        >>> doc1 = DocumentsManager('test_folder')
        >>> doc1.collect_docs()
        >>> # Assuming your_document is a document
        >>> doc1.add_doc(your_document)
        >>> print(doc1.is_in_docs(your_document)) # True

        :param doc: (Document) The document to add
        :raises: TypeError: Invalid document type

        """
        TypesDealer.check_types("DocumentManager.add_doc", [(doc, (Document, ImmutableDocument))])
        if isinstance(doc, ImmutableDocument) is True:
            doc = Document(doc.author, doc.filename, content=doc.content, date=doc.date, filetype=doc.filetype,
                           description=doc.description, folder_path=doc.folder_path)
        self.__docs.append(doc)

    # -----------------------------------------------------------------------

    def add_docs(self, docs: list) -> None:
        """Add a list of documents into the actual list of documents.

        Do not add anything if any element in the list is incorrect.

        :example:
        >>> manager = DocumentsManager('test_folder')
        >>> manager.collect_docs()
        >>> # Assuming doc1 and doc2 are Document() instances
        >>> manager.add_docs([doc1, doc2])
        >>> manager.is_in_docs(doc1))
        True

        :param docs: (list) The list of documents to add
        :raises: TypeError: Invalid document type

        """
        TypesDealer.check_types("DocumentManager.add_docs", [(docs, (list, tuple))])
        # Check all docs before adding -- allows to not add anything if at least one is invalid
        for doc in docs:
            TypesDealer.check_types("DocumentManager.add_doc",
                                    [(doc, (Document, ImmutableDocument))])

        # Add each given document
        for doc in docs:
            if isinstance(doc, ImmutableDocument) is True:
                doc = Document(doc.author, doc.filename, content=doc.content, date=doc.date, filetype=doc.filetype,
                               description=doc.description, folder_path=doc.folder_path)
            self.add_doc(doc)

    # -----------------------------------------------------------------------

    def get_docs_sorted_by_newest(self) -> list:
        """Get documents sorted by date from the most recent to the oldest.

        Return the list of ImmutableDocument() instances sorted
        from the most recent to the oldest.

        :example:
        >>> doc1 = DocumentsManager('test_folder')
        >>> doc1.collect_docs()
        >>> sorted_docs = doc1.get_docs_sorted_by_newest()
        >>> for doc in sorted_docs:
        >>>     print(doc)
        >>> # The documents are printed from the most recent to the oldest

        :return: (list) The list of sorted documents

        """
        sorted_docs = sorted(self.__docs, key=lambda doc: doc.get_date(), reverse=True)
        return [doc.to_immutable() for doc in sorted_docs]

    # -----------------------------------------------------------------------

    def get_docs_sorted_by_oldest(self) -> list:
        """Get documents sorted by date from the oldest to the most recent.

        Return the list of ImmutableDocument() instances sorted
        from the oldest to the most recent.

        :example:
        >>> doc1 = DocumentsManager('test_folder')
        >>> doc1.collect_docs()
        >>> sorted_docs = doc1.get_docs_sorted_by_oldest()
        >>> # The documents are printed from the oldest to the most recent
        >>> for doc in sorted_docs:
        >>>     print(doc)

        :return: (list) The list of sorted documents

        """
        sorted_docs = sorted(self.__docs, key=lambda doc: doc.get_date())
        return [doc.to_immutable() for doc in sorted_docs]

    # -----------------------------------------------------------------------

    def get_docs_sorted_by_most_viewed(self) -> list:
        """Get documents sorted by the number of views.

        Return the list of ImmutableDocument() instances sorted
        from the most viewed to the least viewed.

        :example:
        >>> doc1 = DocumentsManager('test_folder')
        >>> doc1.collect_docs()
        >>> sorted_docs = doc1.get_docs_by_most_viewed()
        >>> # The documents are printed from the most viewed to the least viewed
        >>> for doc in sorted_docs:
        >>>     print(doc)

        :return: (list) The sorted list of documents

        """
        sorted_docs = sorted(self.__docs, key=lambda doc: doc.get_downloads(), reverse=True)
        return [doc.to_immutable() for doc in sorted_docs]

    # -----------------------------------------------------------------------

    def get_docs_sorted_by_least_viewed(self) -> list:
        """Get documents reversely sorted by the number of views.

        Return the list of ImmutableDocument() instances sorted
        from the least viewed to the most viewed.

        :example:
        >>> doc1 = DocumentsManager('test_folder')
        >>> doc1.collect_docs()
        >>> sorted_docs = doc1.get_docs_by_least_viewed()
        >>> for doc in sorted_docs:
        >>>     print(doc)

        :return: (list) The list of sorted documents

        """
        sorted_docs = sorted(self.__docs, key=lambda doc: doc.get_downloads())
        return [doc.to_immutable() for doc in sorted_docs]

    # -----------------------------------------------------------------------

    def filter(self, filters, match_all=False) -> list:
        """Return the list of documents matching the given filters.

        Each filter is a tuple (filter function name, comparator name, [value1, value2, ...]).
        Applicable filter functions are "filename", "filetype", "author" and "date".

        :example:
        >>> manager = DocumentsManager('test_folder')
        >>> manager.collect_docs()
        >>> # Get all documents of Brigitte Bigi
        >>> manager.filter(("author", "iexact", ["Brigitte Bigi"]))
        >>> # Get all PDF or TXT documents of Brigitte Bigi
        >>> _docs = manager.filter(("author", "iexact", ["Brigitte Bigi"]), ("filetype", "iexact", ["pdf", "txt"]), match_all=True)
        >>> # Get all PDF or TXT documents of Brigitte Bigi or John Doe
        >>> _docs = manager.filter(("author", "iexact", ["Brigitte Bigi", "John Doe"]), ("filetype", "iexact", ["pdf", "txt"]), match_all=True)

        :param filters: (list of tuple) List of filters to be applied on the documents.
        :param match_all: (bool) If True, returned documents must match all the given criteria
        :raises: ValueError: If a malformed filter.
        :raises: ValueError: If no value is provided in a filter.
        :return: (list) The list of documents matching the given criteria

        """
        doc_filter = DocumentsFilters(self.__docs)
        filtered_sets = list()
        cast_filters = self.__cast_filters(filters)

        # Apply each filter and append the result in a list of file's sets
        for f in cast_filters:
            # Apply the filter on the 1st value
            value = f[2][0]
            logging.info(" >>> filter.{:s}({:s}={!s:s})".format(f[0], f[1], value))
            files_set = getattr(doc_filter, f[0])(**{f[1]: value})
            #   - getattr() returns the value of the named attributed of object:
            #     it returns f.date if called with getattr(f, "date")
            #   - func(**{'x': '3'}) is equivalent to func(x='3')

            # Apply the filter on the next values
            for i in range(1, len(f[2])):
                value = doc_filter.cast_data(f[0], f[2][i])
                logging.info(" >>>    | filter.{:s}({:s}={!s:s})".format(f[0], f[1], value))
                files_set = files_set | getattr(doc_filter, f[0])(**{f[1]: value})

            filtered_sets.append(files_set)

        # None of the documents is matching
        if len(filtered_sets) == 0:
            return list()

        # At least one document is matching
        files_set = doc_filter.merge_data(filtered_sets, match_all)
        # Return the documents, sorted by date -- newest first
        return sorted(files_set, key=lambda doc: doc.date)

    # -----------------------------------------------------------------------
    # Operate on a specific document
    # -----------------------------------------------------------------------

    def invalidate_doc(self, document: Document | ImmutableDocument) -> None:
        """Delete a document of the disk and remove it of the managed ones.

        :example:
        >>> doc1 = DocumentsManager('test_folder')
        >>> doc1.collect_docs()
        >>> # Assuming your_document is a document in the folder
        >>> doc1.invalidate_doc(your_document)

        :param document: (Document | ImmutableDocument) The document to invalidate
        :raises: ValueError: The document was not found
        :raises: AttributeError: No documents found. Please run collect_docs() first
        :raises: TypeError: Invalid document type

        """
        if len(self.__docs) == 0:
            raise AttributeError("DocumentManager.invalidate_doc exception: No documents found."
                                 " Please run collect_docs() first")
        TypesDealer.check_types("DocumentManager.invalidate_doc", [(document, (Document, ImmutableDocument))])

        # Compare the document given in parameter with his file_path or by the document itself
        doc = self.__find_doc(document)

        if doc is not None:
            if doc.folder_path is None or doc.folder_path == "":
                doc.set_folder_path(self.__folder_path)
            doc.delete_file()
            self.__docs.remove(doc)
            return

        raise ValueError(f"DocumentManager.invalidate_doc exception: Document {document.get_filename()} not found.")

    # -----------------------------------------------------------------------

    def set_description(self, document: Document | ImmutableDocument, description: str):
        """Set and save a description for a document.

        :example:
        >>> doc1 = DocumentsManager('test_folder')
        >>> doc1.collect_docs()
        >>> doc1.set_description(your_document, "This is a description")

        :param document: (Document | ImmutableDocument) The document
        :param description: (str) The description to set
        :raises: FileNotFoundError: The file was not found
        :raises: AttributeError: No documents found. Please run collect_docs() first
        :raises: TypeError: Invalid document type

        """
        if len(self.__docs) == 0:
            raise AttributeError("DocumentManager.set_description exception: No documents found. "
                                 "collect_docs() should be called first.")
        TypesDealer.check_types("DocumentManager.delete", [(document, (Document, ImmutableDocument))])

        doc = self.__find_doc(document)

        if doc is not None:
            if doc.folder_path is None or doc.folder_path == "":
                doc.set_folder_path(self.__folder_path)
            doc.set_description(description)
            doc.save_description()
        else:
            raise ValueError(f"DocumentManager.set_description exception: Document {document.filename} not found.")

    # -----------------------------------------------------------------------

    def increment_doc_downloads(self, document: Document | ImmutableDocument):
        """Increment the number of downloads of a document.

        :example:
        >>> doc1 = DocumentsManager('test_folder')
        >>> doc1.collect_docs()
        >>> doc1.increment_doc_downloads(your_document)

        :param document: (Document | ImmutableDocument) The document
        :raises: FileNotFoundError: The file was not found
        :raises: AttributeError: No documents found. Please run collect_docs() first
        :raises: TypeError: Invalid document type

        """
        if len(self.__docs) == 0:
            raise AttributeError("DocumentManager.increment_doc_downloads exception: No documents found. "
                                 "collect_docs() should be called first.")
        TypesDealer.check_types("DocumentManager.increment_doc_downloads", [(document, (Document, ImmutableDocument))])

        doc = self.__find_doc(document)

        if doc is not None:
            if doc.folder_path is None or doc.folder_path == "":
                doc.set_folder_path(self.__folder_path)
            doc.increment_downloads()
        else:
            raise ValueError(f"DocumentManager.increment_doc_downloads exception: "
                             f"Document {document.filename} not found.")

    # -----------------------------------------------------------------------

    def save_doc(self, document: Document | ImmutableDocument, folder_path: str = ""):
        """Save a document

        :example:
        >>> doc1 = DocumentsManager('test_folder')
        >>> doc1.collect_docs()
        >>> # You can save the document in a different folder
        >>> doc1.save_doc(your_document, 'new_folder')
        >>> # Or in the folder with the DocumentsManager was initialized
        >>> doc1.save_doc(your_document)

        :param document: (Document | ImmutableDocument) The document
        :param folder_path: (str) The folder path to save the document
        :raises: TypeError: Invalid document type or folder path type

        """
        TypesDealer.check_types("DocumentManager.save_doc",
                                [(document, (Document, ImmutableDocument)), (folder_path, str)])

        if isinstance(document, ImmutableDocument) is True:
            document = Document(
                document.author, document.filename, content=document.content,
                date=document.date, filetype=document.filetype,
                description=document.description, folder_path=folder_path)

        document.save_file(folder_path if folder_path != "" else self.__folder_path)

    # -----------------------------------------------------------------------

    def get_doc_content(self, doc: Document | ImmutableDocument) -> str | bytes | None:
        """Get the content of a document.

        :example:
        >>> doc1 = DocumentsManager('test_folder')
        >>> doc1.collect_docs()
        >>> # Assuming your_document is a document in the folder
        >>> doc1.get_doc_content(your_document)
        >>> print(your_document.get_content())

        :param doc: (Document) The document
        :raises: FileNotFoundError: The file was not found
        :raises: AttributeError: No documents found. Please run collect_docs() first
        :raises: TypeError: Invalid document type
        :return: (str|bytes|None) The content of the document

        """
        if len(self.__docs) == 0:
            raise AttributeError("DocumentManager.get_content exception: No documents found. "
                                 "collect_docs() should be called first.")
        TypesDealer.check_types("DocumentManager.get_content", [(doc, Document)])
        file_path = doc.get_file_path()
        if file_path is None:
            raise FileNotFoundError("DocumentManager.get_content exception: File path cannot be None.")
        if os.path.exists(file_path) is False:
            raise FileNotFoundError(f"DocumentManager.get_content exception: File {file_path} not found.")

        doc = self.__find_doc(doc)
        if doc.folder_path is None or doc.folder_path == "":
            doc.set_folder_path(self.__folder_path)
        if doc is not None:
            with open(file_path, 'r') as file:
                content = file.read()
            doc.set_content(content)
            return doc.get_content()
        return None

    # -----------------------------------------------------------------------------------------------------------------

    def get_doc_description(self, document: Document | ImmutableDocument) -> str | None:
        """Get the description of a document.

        :example:
        >>> doc1 = DocumentsManager('test_folder')
        >>> doc1.collect_docs()
        >>> # Assuming your_document is a document in the folder
        >>> doc1.get_doc_description(your_document)
        >>> print(your_document.get_description())

        :param document: (Document | ImmutableDocument) The document
        :raises: FileNotFoundError: The file was not found
        :raises: AttributeError: No documents found. Please run collect_docs() first
        :raises: TypeError: Invalid document type
        :return: (str|None) The description of the document

        """
        if len(self.__docs) == 0:
            raise AttributeError("DocumentManager.get_description exception: No documents found. "
                                 "collect_docs() should be called first.")
        TypesDealer.check_types("DocumentManager.get_description", [(document, (Document, ImmutableDocument))])

        doc = self.__find_doc(document)

        if doc is not None:
            if doc.folder_path is None or doc.folder_path == "":
                doc.set_folder_path(self.__folder_path)
            return doc.get_description()

        raise ValueError(f"DocumentManager.get_description exception: Document {document.filename} not found.")

    # -----------------------------------------------------------------------
    # Private
    # -----------------------------------------------------------------------

    def __cast_filters(self, filters: list) -> list:
        """Return the value-typed of given filters.

        :param filters: (list of tuple) List of filters to be applied on the documents.
        :raises: ValueError: If a malformed filter.
        :raises: ValueError: If an invalid field is provided in a filter.
        :return: (list of tuple) List of filters to be applied on the documents with typed values.

        """
        cast_filters = list()
        doc_filter = DocumentsFilters(self.__docs)

        # Apply each filter and append the result in a list of file's sets
        for f in filters:
            if isinstance(f, (list, tuple)) and len(f) == 3:
                if None in f or any(len(f[i]) == 0 for i in range(len(f))):
                    raise ValueError("Invalid field defined for filter {:s}".format(str(f)))
                casted_values = list()
                for value in f[2]:
                    casted_values.append(doc_filter.cast_data(f[0], value))

                cast_filters.append((f[0], f[1], casted_values))
            else:
                raise ValueError("Filter must have 3 arguments: function, comparator, value."
                                 "Got {:d} instead.".format(len(f)))

        return cast_filters

    # -----------------------------------------------------------------------

    def __find_doc(self, document: Document | ImmutableDocument) -> Document | None:
        """Search for a document in the list of stored documents.

         Find the instance of Document which is matching the given document
         in the list of stored docs.i If it finds a matching document, it
         returns the document instance; otherwise, it returns None.

        :param document: (Document | ImmutableDocument) The document to find
        :return: (Document | None) The document found or None if not found or invalid

        """
        # Two docs are equal if same author, filename, filetype and date.
        # See Document.__eq__ for details.
        return next((doc for doc in self.__docs if doc == document), None)

    # -----------------------------------------------------------------------
    # Overloads
    # -----------------------------------------------------------------------

    def __len__(self):
        return len(self.__docs)

    # -----------------------------------------------------------------------

    def __iter__(self):
        for doc in self.__docs:
            yield doc.to_immutable()

    # -----------------------------------------------------------------------

    def __contains__(self, document):
        # do not un-necessarily browse through the documents
        if isinstance(document, (Document, ImmutableDocument)) is False:
            return False
        # compare given document to each of ours with '=='.
        # allows to return true if all(author, filename, date, filetype) are equals
        for doc in self.__docs:
            if doc == document:
                return True
        return False
