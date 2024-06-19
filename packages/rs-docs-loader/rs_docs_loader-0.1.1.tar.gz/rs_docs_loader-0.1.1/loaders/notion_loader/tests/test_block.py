from copy import deepcopy
from unittest.mock import patch

from loaders.notion_loader.notion.blocks import (
    _flatten_children_blocks_one_level_depth,
    extract_text_from_cells,
    extract_text_from_text_block,
    flatten_children_blocks,
    text_from_block,
    text_from_page_data,
)
from loaders.notion_loader.tests.constants import BLOCK_WITH_CELLS, BLOCK_WITH_RICH_TEXT, BLOCK_WITH_TEXT_RESULT
from loaders.notion_loader.tests.mocks import MockNotionAPIData, mock_blocks_children_list


class TestBlockFunctions:
    @patch("loaders.notion_loader.notion.blocks.get_children_blocks", wraps=mock_blocks_children_list)
    def test__flatten_children_blocks_one_level_depth(self, mocked_children):
        data = MockNotionAPIData()

        (
            block_1,  # Has children
            block_2,  # Has children but is a child page
            block_3,  # Has children
            block_4,  # Has no children
        ) = data.get_blocks(["1", "2", "3", "4"])

        page_data = [block_1, block_2, block_3, block_4]

        expected_result = [
            block_1,
            *data.get_blocks(["11", "12"]),
            block_2,
            block_3,
            *data.get_blocks(["31", "32"]),
            block_4,
        ]

        flattened_blocks = _flatten_children_blocks_one_level_depth(page_data)

        assert flattened_blocks == expected_result

    @patch("loaders.notion_loader.notion.blocks.get_children_blocks", wraps=mock_blocks_children_list)
    def test_flatten_children_blocks_with_one_level_of_depth(self, mocked_children):
        data = MockNotionAPIData()

        (
            block_1,  # Has children
            block_2,  # Has children but is a child page
            block_3,  # Has children
            block_4,  # Has no children
        ) = data.get_blocks(["1", "2", "3", "4"])

        page_data_1 = [block_1, block_2, block_3, block_4]
        page_data_2 = deepcopy(page_data_1)

        # Children with ids 121, 311 and 312 are not retrieved
        flatten_one_level_private = _flatten_children_blocks_one_level_depth(page_data_1)
        flatten_one_level_public = flatten_children_blocks(page_data_2, children_block_depth=1)

        assert flatten_one_level_private == flatten_one_level_public

    @patch("loaders.notion_loader.notion.blocks.get_children_blocks", wraps=mock_blocks_children_list)
    def test_flatten_children_blocks_with_two_levels_of_depth(self, mocked_children):
        data = MockNotionAPIData()

        (
            block_1,  # Has children
            block_2,  # Has children but is a child page
            block_3,  # Has children
            block_4,  # Has no children
        ) = data.get_blocks(["1", "2", "3", "4"])

        page_data = [block_1, block_2, block_3, block_4]

        expected_result = [
            block_1,
            data.get_blocks(["11"])[0],
            data.get_blocks(["12"])[0],
            *data.get_blocks(["121"]),
            block_2,
            block_3,
            data.get_blocks(["31"])[0],
            *data.get_blocks(["311", "312"]),
            data.get_blocks(["32"])[0],
            block_4,
        ]

        # Update values to reflect changes after calling flatten function
        expected_result[2].update(has_children=False)
        expected_result[6].update(has_children=False)
        flattened_blocks = flatten_children_blocks(page_data, children_block_depth=2)

        assert flattened_blocks == expected_result

    def test_text_from_page_data(self):
        block_1 = {
            "type": "text_block",
            "text_block": {
                "rich_text": [
                    {"plain_text": "Block"},
                    {"plain_text": "number 1"},
                ],
            },
        }
        block_2 = {
            "type": "text_block",
            "text_block": {},
        }
        block_3 = {
            "type": "text_block",
            "text_block": {
                "rich_text": [
                    {"plain_text": "Block"},
                    {"plain_text": "number 3"},
                ],
            },
        }
        block_4 = {
            "type": "text_block",
            "text_block": {},
        }

        block_5 = {
            "type": "table_row",
            "table_row": {
                "cells": [
                    [
                        {"plain_text": "Block number 5"},
                    ]
                ]
            },
        }

        page_data = [block_1, block_2, block_3, block_4, block_5]
        expected_text = "Block number 1\n\nBlock number 3\n\nBlock number 5\n"

        assert text_from_page_data(page_data) == expected_text

    def test_text_from_block_empty_text(self):
        block_with_no_text = {"type": "non_text_block", "non_text_block": {}}
        assert text_from_block(block_with_no_text) == ""

    def test_text_from_block_rich_text(self):
        assert text_from_block(BLOCK_WITH_RICH_TEXT) == BLOCK_WITH_TEXT_RESULT

    def test_text_from_block_cells(self):
        assert text_from_block(BLOCK_WITH_CELLS) == BLOCK_WITH_TEXT_RESULT

    def test_extract_test_from_cells(self):
        assert extract_text_from_cells(BLOCK_WITH_CELLS["table_row"]["cells"]) == BLOCK_WITH_TEXT_RESULT

    def test_extract_text_from_text_block(self):
        text_block_rich_text = BLOCK_WITH_RICH_TEXT["text_block"]["rich_text"]
        assert extract_text_from_text_block(text_block_rich_text) == BLOCK_WITH_TEXT_RESULT

        text_block_cells = BLOCK_WITH_CELLS["table_row"]["cells"][0]
        assert extract_text_from_text_block(text_block_cells) == BLOCK_WITH_TEXT_RESULT
