import sys
from collections.abc import Iterator

from loaders.common.base_loader import Document, RsBaseLoader
from loaders.notion_loader.notion.page import get_notion_tree_documents, get_single_page_document
from logger import set_log_level

set_log_level()


class NotionLoader(RsBaseLoader):
    """
    Retrieve all text content from pages in Notion
    """

    def __init__(self, page_id: str, tree_load: bool) -> None:
        self.page_id = page_id
        self.tree_load = tree_load

    def lazy_load(self) -> Iterator[Document]:
        if self.tree_load:
            yield from get_notion_tree_documents(page_id)
        else:
            yield get_single_page_document(page_id)
        return super().lazy_load()


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python notion_documents_loader.py <tree|single> <page_id>")
        sys.exit(1)
    tree_load = sys.argv[1] == "tree"
    page_id = sys.argv[2]
    loader = NotionLoader(page_id=page_id, tree_load=tree_load)
    result = loader.load()
    print(result)
