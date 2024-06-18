from collections.abc import Iterator

from langchain_community.document_loaders import UnstructuredFileIOLoader
from langchain_google_community import GoogleDriveLoader

from loaders.common.base_loader import Document
from loaders.google_drive_loader.common.base_loader import BaseLoader
from logger.logger import set_log_level

set_log_level()


class PdfLoader(BaseLoader):
    def lazy_load(self) -> Iterator[Document]:
        loader = GoogleDriveLoader(
            credentials_path=self.credentials_path,
            token_path=self.token_path,
            folder_id=self.folder_id,
            recursive=self.recursive,
            file_types=["pdf"],
            file_loader_cls=UnstructuredFileIOLoader,
            file_loader_kwargs={"mode": "elements"},
        )

        yield from loader.lazy_load()
