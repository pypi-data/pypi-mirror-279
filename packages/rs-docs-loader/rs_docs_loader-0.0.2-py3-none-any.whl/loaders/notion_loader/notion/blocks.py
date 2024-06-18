import time
from typing import Any

from notion_client import APIResponseError

from loaders.notion_loader.config import MAX_REQUESTS_PER_SECOND
from loaders.notion_loader.notion.api_wrapper import get_children_blocks
from logger import logger


def flatten_children_blocks(blocks: list[dict[str, Any]], children_block_depth: int) -> list[dict[str, Any]]:
    """
    Given a list of blocks, returns a new list of blocks containing
    the same blocks that were in the original list plus all its child blocks.
    This process is done until reaching children blocks at the depth indicated
    by the parameter `children_block_depth`.
    Child blocks are placed right after their parent.
    """

    if children_block_depth < 1:
        raise ValueError("Depth must be non negative.")

    result = blocks

    for i in range(children_block_depth):
        result = _flatten_children_blocks_one_level_depth(result)

    return result


def _flatten_children_blocks_one_level_depth(blocks: list[dict[str, Any]]) -> list[dict[str, Any]]:
    request_count = 0

    result = []

    for block in blocks:
        result.append(block)

        if block["has_children"] and block.get("type") != "child_page":
            try:
                request_count += 1
                children = get_children_blocks(block["id"])["results"]
                result.extend(children)

                # Change the value of flag to not retrieve children in next iterations
                block["has_children"] = False

            except APIResponseError as error:
                logger.error(error)

            # Wait 1 second every N requests to avoid exceeding Notion's request limit
            if request_count % MAX_REQUESTS_PER_SECOND == 0:
                time.sleep(1)

    return result


def text_from_page_data(blocks: dict[str, Any]) -> str:
    """
    Parses Notion blocks and transforms them into plain text.
    """

    result = ""
    for block in blocks:
        result += text_from_block(block) + "\n"

    return result


def text_from_block(block: dict[str, Any]) -> str:
    """
    Extracts text from a block and returns it.
    If the block has no text it returns an empty string.
    """
    block_type = block["type"]
    rich_text_key = "rich_text"
    cells_key = "cells"
    is_rich_text_block = rich_text_key in block[block_type]
    if is_rich_text_block:
        rich_text = block[block_type][rich_text_key]
        return extract_text_from_text_block(rich_text)
    elif cells_key in block[block_type]:
        cells_block = block[block_type][cells_key]
        return extract_text_from_cells(cells_block)
    return ""


def extract_text_from_cells(cells_block: list[list[dict[str, Any]]]) -> str:
    cells_list_content = list(map(extract_text_from_text_block, cells_block))
    return " ".join(cells_list_content)


def extract_text_from_text_block(text_block: list[dict[str, Any]]) -> str:
    list_content = [rt.get("plain_text", "").strip() for rt in text_block]
    return " ".join(list_content)
