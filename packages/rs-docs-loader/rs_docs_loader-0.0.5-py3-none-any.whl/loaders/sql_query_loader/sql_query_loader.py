from __future__ import annotations

import re
from collections.abc import Iterator

from langchain_text_splitters import RecursiveCharacterTextSplitter

from loaders.common.base_loader import Document, RsBaseLoader


class SqlQueryLoader(RsBaseLoader):
    """A custom document loader that retrieves documents from a SQL database."""

    def __init__(self, connection, sql_query: str, params: tuple = ()) -> None:
        """
        Initializes the loader with a connection and an SQL query.

        Args:
            connection: The connection object.
            sql_query: The SQL query to retrieve documents.
            params: Optional tuple of parameters to use in the query.
        """
        self.connection = connection
        self.sql_query = sql_query.strip()  # Store the SQL query as a stripped string
        self.params = params

        self.validate_query()

    def validate_query(self) -> None:
        """Validates the SQL query to ensure it meets security requirements."""
        self.__validate_select_only()
        self.__validate_no_prohibited_commands()
        self.__validate_limit_clause()

    def __validate_select_only(self) -> None:
        """Ensures the query starts with a SELECT statement."""
        if not self.sql_query.upper().startswith("SELECT"):
            raise ValueError("Only SELECT queries are allowed.")

    def __validate_no_prohibited_commands(self) -> None:
        """Checks for potentially dangerous SQL commands."""
        prohibited_commands = ["INSERT", "UPDATE", "DELETE", "DROP", "ALTER", "CREATE"]
        for command in prohibited_commands:
            if re.search(rf"\b{command}\b", self.sql_query, re.IGNORECASE):
                raise ValueError(f"Prohibited SQL command found: {command}")

    def __validate_limit_clause(self) -> None:
        """Ensures the query contains a LIMIT clause properly formatted and placed at the end."""
        if "LIMIT" not in self.sql_query.upper():
            raise ValueError("Query must include a LIMIT clause.")
        if not re.search(r"LIMIT\s+\d+\s*;?$", self.sql_query, re.IGNORECASE):
            raise ValueError("The LIMIT clause must be properly formatted and placed at the end of the query.")

    def lazy_load(self) -> Iterator[Document]:  # type: ignore
        """A lazy loader that retrieves documents from the database one by one.

        Yields:
            Documents retrieved from the database.
        """
        cursor = self.connection.cursor()
        cursor.execute(self.sql_query, self.params)
        for row in cursor.fetchall():  # Fetch all rows and iterate over them
            # Join fields with a semicolon
            page_content = "; ".join(str(field) for field in row)
            yield Document(
                page_content=page_content,
                metadata={"source": "sql_database"},
            )
        cursor.close()

    def text_splitter(self):
        """Splits the documents into smaller chunks using a text splitter."""
        docs = list(self.lazy_load())

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=4000, chunk_overlap=0, separators=[" ", ",", "\n"])

        return text_splitter.split_documents(docs)
