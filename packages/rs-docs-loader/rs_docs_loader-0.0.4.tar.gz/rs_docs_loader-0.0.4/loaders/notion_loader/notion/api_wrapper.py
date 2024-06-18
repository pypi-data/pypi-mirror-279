from typing import Any

from loaders.notion_loader.notion.client import get_notion_client


def get_block_data(block_id: str) -> dict[str, Any]:
    """
    Wrapper method that retrieves the content of a single block
    corresponding to the provided `block_id`.
    """
    notion = get_notion_client()
    return notion.blocks.retrieve(block_id=block_id)


def get_children_blocks(block_id: str) -> dict[str, Any]:
    """
    Wrapper method that retrieves the child blocks of the block
    corresponding to the provided `block_id`.
    """
    notion = get_notion_client()
    return notion.blocks.children.list(block_id=block_id)


def get_page_url(page_id: str) -> str:
    """
    Wrapper method that gets the URL of a Notion page
    from a page ID.
    """
    notion = get_notion_client()
    return notion.pages.retrieve(page_id=page_id).get("url")


def get_database_pages(database_id: str) -> dict[str, Any]:
    """
    Wrapper method that gets the list of pages of a Notion database
    from a database ID.
    """
    notion = get_notion_client()
    return notion.databases.query(database_id=database_id)
