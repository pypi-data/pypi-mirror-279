import time
from collections.abc import Iterator
from typing import Any

from notion_client import APIResponseError

from loaders.common.base_loader import Document
from loaders.notion_loader.config import MAX_REQUESTS_PER_SECOND
from loaders.notion_loader.notion.api_wrapper import get_block_data, get_children_blocks, get_page_url
from loaders.notion_loader.notion.blocks import flatten_children_blocks, text_from_page_data
from loaders.notion_loader.notion.database import pages_links_from_db
from logger import logger


def get_notion_tree_documents(page_root_id: str) -> Iterator[Document]:
    """
    Retrieves the content of the notion page corresponding to `page_root_id`
    as well as for all pages that have the `root_id` page as an ancestor.
    Returns the content of the pages as a list of `Document` instances.
    """

    request_count = 0

    try:
        page_title = get_page_title(page_root_id)
    except APIResponseError as error:
        logger.error(error)
        return []

    pages = [(page_title, page_root_id)]

    retrieved_ids = set()
    docs = []

    page_titles = {}
    parents = {}

    while pages:
        page_title, page_id = pages.pop(0)

        if page_id in retrieved_ids:
            continue

        try:
            # Extract all page content
            request_count += 1
            page_url, text, linked_pages = get_page_content(page_id, page_title)

            # Build page path
            page_path = build_page_path(page_id, page_title, parents, page_titles)

            # Update data structures
            page_titles[page_id] = page_title
            for child_page in linked_pages:
                parents[child_page[1]] = page_id

            # Save document
            metadata = {
                "id": page_id,
                "url": page_url,
                "author": page_path,  # TODO: Change author for new field for path
            }
            document = generate_document(text=text, metadata=metadata)

            docs.append(document)
            pages.extend(linked_pages)
            retrieved_ids.add(page_id)
            yield document

        except APIResponseError as error:
            logger.error(error)

        # Wait 1 second every N requests to avoid exceeding Notion's request limit
        if request_count % MAX_REQUESTS_PER_SECOND == 0:
            time.sleep(1)

    return docs


def get_single_page_document(page_id: str) -> Document:
    """
    Get a document with data of a single page from Notion, given a page ID.
    Raises APIResponseError if there is an error retrieving the page data.
    """
    page_title = get_page_title(page_id)
    page_url, text, _ = get_page_content(page_id, page_title)
    metadata = {
        "id": page_id,
        "url": page_url,
    }
    page_document = generate_document(text=text, metadata=metadata)
    return page_document


def get_page_title(page_id) -> str:
    """
    Get the title of a page given its page ID.
    Raises APIResponseError if there is an error retrieving the page data.
    """
    page_data = get_block_data(block_id=page_id)
    child_page_data = page_data.get("child_page")
    page_title = child_page_data.get("title")
    return page_title


def get_page_content(page_id: str, page_title: str) -> tuple[str, str, list[tuple[str, str]]]:
    """
    Get the url, text and linked pages from a Notion page given a page ID and title
    The page text contains all the text of the page blocks and their child blocks.
    """
    blocks = get_page_blocks(page_id=page_id)
    page_url = get_page_url(page_id=page_id)
    blocks = flatten_children_blocks(blocks=blocks, children_block_depth=2)
    linked_pages = extract_notion_child_pages(blocks=blocks)
    text = f"<h2>{page_title}</h2>\n\n{text_from_page_data(blocks=blocks)}"
    return page_url, text, linked_pages


def build_page_path(page_id: str, page_title: str, parents: dict[str, str], page_titles: dict[str, str]) -> str:
    """
    Builds the page path, which is a string representing the hierarchy of parent pages, for a given page in Notion.
    - The page path is built by concatenating the parent page titles with the current page title, separated by " / ".

    Parameters:
    - page_id: The ID of the page for which to build the path.
    - page_title: The title of the page.
    - parents: A dictionary mapping child page IDs to their parent page IDs.
    - page_titles: A dictionary mapping page IDs to their titles.
    """
    page_path = ""

    while parents.get(page_id) is not None:
        page_path = page_titles.get(parents.get(page_id)) + " / " + page_path
        page_id = parents.get(page_id)

    page_path += page_title
    return page_path


def extract_notion_child_pages(blocks: list[dict[str:Any]]) -> list[tuple[str, str]]:
    """
    Given a list of blocks corresponding to the content of a Notion page,
    it extracts all ids corresponding to a child page and returns
    a list of tuples of the form: (Title of child page, Child page id)
    """
    pages = []
    for block in blocks:
        if block.get("type") == "child_page":
            link_tuple = (block.get("child_page").get("title"), block.get("id"))
            pages.append(link_tuple)
        elif block.get("type") == "child_database":
            db_pages = pages_links_from_db(block)
            pages.extend(db_pages)
    return pages


def get_page_blocks(page_id: str) -> dict[str, Any]:
    """
    Wrapper method that retrieves the blocks of the Notion page
    corresponding to the provided `page_id`.
    """

    response = get_children_blocks(page_id)
    blocks = response["results"]

    return blocks


def generate_document(text: str, metadata: dict[str, Any] = None) -> Document:
    """
    Takes a text and an id that belong to a Notion page, then
    constructs and returns a Document instance with this information.
    """
    return Document(page_content=text, metadata=metadata)
