from unittest.mock import patch

from loaders.common.base_loader import Document
from loaders.notion_loader.notion.page import (
    build_page_path,
    extract_notion_child_pages,
    generate_document,
    get_notion_tree_documents,
    get_page_content,
    get_single_page_document,
)
from loaders.notion_loader.tests.mocks import mock_blocks_children_list, mock_blocks_retrieve, mock_page_url


class TestPageFunctions:
    @patch("loaders.notion_loader.notion.page.get_page_url", wraps=mock_page_url)
    @patch("loaders.notion_loader.notion.page.get_children_blocks", wraps=mock_blocks_children_list)
    @patch("loaders.notion_loader.notion.blocks.get_children_blocks", wraps=mock_blocks_children_list)
    @patch("loaders.notion_loader.notion.page.get_block_data", wraps=mock_blocks_retrieve)
    def test_get_notion_tree_documents(self, mocked_blocks, mocked_childred, mocked_children2, mocked_url):
        results = list(get_notion_tree_documents(page_root_id="0"))

        # There is one document for the root page and one for the only child page
        assert len(results) == 2

        root_page_doc, child_page_doc = results

        assert isinstance(root_page_doc, Document)
        assert root_page_doc.metadata["id"] == "0"
        assert root_page_doc.page_content == (
            "<h2>TEST ROOT PAGE</h2>\n"
            "\n"
            "Block 1\n"
            "Child 1 of block 1\n"
            "Child 2 of block 1\n"
            "Child 1 of block 12\n"
            "\n"
            "Block 3\n"
            "Child 1 of block 3\n"
            "Child 1 of block 3\n"
            "Child 1 of block 3\n"
            "Child 2 of block 3\n"
            "Block 4\n"
        )
        assert root_page_doc.metadata["url"] == "http://root-url.test"

        assert isinstance(child_page_doc, Document)
        assert child_page_doc.metadata["id"] == "2"
        assert child_page_doc.page_content == (
            "<h2>Child page 1</h2>\n" "\n" "Child 1 of block 2\n" "Child 2 of block 2\n"
        )
        assert child_page_doc.metadata["url"] == "http://child-page-1.test"

    @patch("loaders.notion_loader.notion.page.get_page_title", return_value="Page Title")
    @patch("loaders.notion_loader.notion.page.get_page_content", return_value=("page_url", "Page content", ""))
    def test_get_single_page_document(self, mock_content, mock_title):
        valid_page_id = "valid_page_id"
        expected_page_id = valid_page_id
        expected_text = "Page content"
        expected_url = "page_url"
        result = get_single_page_document(valid_page_id)

        assert isinstance(result, Document)
        assert result.metadata["id"] == expected_page_id
        assert result.page_content == expected_text
        assert result.metadata["url"] == expected_url

    @patch("loaders.notion_loader.notion.page.get_page_blocks")
    @patch("loaders.notion_loader.notion.page.get_page_url", return_value="page_url")
    @patch("loaders.notion_loader.notion.page.flatten_children_blocks")
    @patch("loaders.notion_loader.notion.page.extract_notion_child_pages", return_value=[("Child Page 1", "child1")])
    @patch("loaders.notion_loader.notion.page.text_from_page_data", return_value="Page text")
    def test_get_page_content(self, mock_page_data, mock_childs, mock_flatten, mock_url, mock_blocks):
        result = get_page_content("page_id", "Page Title")
        assert result == (
            "page_url",
            "<h2>Page Title</h2>\n\nPage text",
            [("Child Page 1", "child1")],
        )

    def test_build_page_path(self):
        page_id = "page_id"
        page_title = "Page Title"
        parents = {"parent_page_id": "grandparent_page_id", "page_id": "parent_page_id"}
        page_titles = {
            "parent_page_id": "Parent Page",
            "grandparent_page_id": "Grand parent Page",
        }
        result = build_page_path(page_id, page_title, parents, page_titles)
        assert result == "Grand parent Page / Parent Page / Page Title"

        parents = {}
        page_titles = {}
        result = build_page_path(page_id, page_title, parents, page_titles)
        assert result == "Page Title"

    def test_extract_notion_child_pages(self):
        block_1 = {
            "type": "text_block",
            "text_block": {"rich_text": [{"plain_text": "Block 1"}]},
        }
        block_2 = {
            "id": "2",
            "type": "child_page",
            "child_page": {"title": "Child page 1"},
        }
        block_3 = {
            "type": "text_block",
            "text_block": {"rich_text": [{"plain_text": "Block 3"}]},
        }
        block_4 = {
            "id": "4",
            "type": "child_page",
            "child_page": {"title": "Child page 2"},
        }

        page_data = [block_1, block_2, block_3, block_4]

        expected_child_pages = [("Child page 1", "2"), ("Child page 2", "4")]

        child_pages = extract_notion_child_pages(page_data)

        assert child_pages == expected_child_pages

    def test_generate_document(self):
        test_url = "https://testurl.test"
        text = "Example text"
        id = "1234"

        document = generate_document(text=text, metadata={"id": id, "url": test_url})

        expected_document = Document(
            page_content=text,
            metadata={"id": id, "url": test_url},
        )

        assert document == expected_document
