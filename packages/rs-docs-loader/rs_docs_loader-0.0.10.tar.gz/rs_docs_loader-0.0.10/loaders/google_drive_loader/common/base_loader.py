from abc import abstractmethod
from collections.abc import Iterator

from loaders.common.base_loader import Document, RsBaseLoader
# from loaders.google_drive_loader.common.config import CREDENTIAL_PATH, FOLDER_ID, TOKEN_PATH


class BaseLoader(RsBaseLoader):
    def __init__(self, credentials_path, token_path, folder_id, recursive):
        self.credentials_path = credentials_path
        self.token_path = token_path
        self.folder_id = folder_id
        self.recursive = recursive

    @abstractmethod
    def lazy_load(self) -> Iterator[Document]:
        """
        Used to load documents one by one lazily. Use for production code.
        Implement this method using generators to avoid loading all Documents into memory at once.
        """
