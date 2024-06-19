from unittest.mock import patch

import httpx
from notion_client import APIResponseError

from loaders.notion_loader.notion.database import get_db_page_title, pages_links_from_db
from loaders.notion_loader.tests.constants import MOCK_DATABASE_PAGES


class TestDatabaseFunctions:
    @patch("loaders.notion_loader.notion.database.get_database_pages", return_value=MOCK_DATABASE_PAGES)
    def test_pages_links_from_db(self, mocked_db):
        """
        Function called with a valid database block,
        returns a list of tuples with page titles and IDs
        """
        db_block = {"id": "valid_id"}
        result = pages_links_from_db(db_block)
        mocked_results = MOCK_DATABASE_PAGES["results"]
        assert len(result) == len(mocked_results)
        assert result[0][0] == ""
        assert result[0][1] == mocked_results[0]["id"]
        assert result[1][0] == mocked_results[1]["properties"]["prop2"]["title"][0]["plain_text"]
        assert result[1][1] == mocked_results[1]["id"]
        assert result[2][0] == mocked_results[2]["properties"]["prop2"]["title"][0]["plain_text"]
        assert result[2][1] == mocked_results[2]["id"]

    @patch("loaders.notion_loader.notion.database.get_database_pages", return_value={"results": []})
    def test_pages_links_from_db_empty(self, mocked_empty):
        db_block = {"id": "valid_id"}
        result = pages_links_from_db(db_block)
        assert result == []

    @patch(
        "loaders.notion_loader.notion.database.get_database_pages",
        side_effect=APIResponseError(httpx.Response(500), "Error", 500),
    )
    def test_pages_links_from_db_error(self, mocked_error):
        db_block = {"id": "valid_id"}
        result = pages_links_from_db(db_block)
        assert result == []

    def test_get_db_page_title(self):
        """
        Should return the title of a Notion database page representation
        """
        mocked_results = MOCK_DATABASE_PAGES["results"]
        db_page = mocked_results[1]
        assert get_db_page_title(db_page) == "Test text"
