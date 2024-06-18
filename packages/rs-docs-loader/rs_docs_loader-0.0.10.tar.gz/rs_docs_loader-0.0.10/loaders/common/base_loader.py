from abc import ABC, abstractmethod
from collections.abc import Iterator

from langchain_core.document_loaders import BaseLoader
from langchain_core.documents import Document


class RsBaseLoader(BaseLoader, ABC):
    """
    Interface for RS Document Loaders.

    Implementations should implement the lazy-load method using generators

    loader = CustomRSLoader(
        some_param="some_param",
    )
    for doc in loader.lazy_load():
        print(doc)

    When implementing a document loader do NOT provide parameters via the lazy_load method.
    All configuration is expected to be passed through the initializer (init).
    """

    @abstractmethod
    def lazy_load(self) -> Iterator[Document]:
        """
        Used to load documents one by one lazily. Use for production code.
        Implement this method using generators to avoid loading all Documents into memory at once.
        """
