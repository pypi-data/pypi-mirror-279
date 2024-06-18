from typing import Any

from notion_client import APIResponseError

from loaders.notion_loader.notion.api_wrapper import get_database_pages
from logger import logger


def pages_links_from_db(db_block: dict[str, Any]) -> list[tuple[str, str]]:
    """
    From a db block, obtain a list of (title, id) tuples of its child pages
    TO DO: Handle paginated databases
    """
    try:
        db_pages = get_database_pages(db_block.get("id"))["results"]
    except APIResponseError as error:
        logger.error(error)
        return []
    page_links = list(map(lambda db_page: (get_db_page_title(db_page), db_page.get("id")), db_pages))
    return page_links


def get_db_page_title(db_page: dict[str, Any]) -> str:
    """
    Extracts the title from a Notion database page representation
    Iter over all the page properties and extract the plain text value
    of the title property
    """
    page_title = ""
    for prop in db_page["properties"].values():
        if prop.get("type") == "title":
            page_title = prop["title"][0]["plain_text"] if prop["title"] else ""
            break
    return page_title
