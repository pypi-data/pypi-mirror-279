from abc import abstractmethod
from collections.abc import Iterator

from loaders.common.base_loader import Document, RsBaseLoader
from loaders.google_drive_loader.common.config import CREDENTIAL_PATH, FOLDER_ID, TOKEN_PATH
from logger.logger import set_log_level

set_log_level()


class BaseLoader(RsBaseLoader):
    def __init__(self, recursive):
        self.credentials_path = CREDENTIAL_PATH
        self.token_path = TOKEN_PATH
        self.folder_id = FOLDER_ID
        self.recursive = recursive

    @abstractmethod
    def lazy_load(self) -> Iterator[Document]:
        """
        Used to load documents one by one lazily. Use for production code.
        Implement this method using generators to avoid loading all Documents into memory at once.
        """
