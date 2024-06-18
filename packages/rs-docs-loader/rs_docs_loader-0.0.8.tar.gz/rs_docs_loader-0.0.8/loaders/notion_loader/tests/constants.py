# ROOT PAGE
BLOCK_0 = {
    "id": "0",
    "type": "child_page",
    "child_page": {"title": "TEST ROOT PAGE"},
    "has_children": True,
}
# LEVEL 0 BLOCKS
BLOCK_1 = {  # Has children
    "id": "1",
    "type": "test_block",
    "test_block": {"rich_text": [{"plain_text": "Block 1"}]},
    "has_children": True,
}
BLOCK_2 = {  # Has children but is a child page
    "id": "2",
    "type": "child_page",
    "child_page": {"title": "Child page 1"},
    "has_children": True,
}
BLOCK_3 = {  # Has children
    "id": "3",
    "type": "test_block",
    "test_block": {"rich_text": [{"plain_text": "Block 3"}]},
    "has_children": True,
}
BLOCK_4 = {  # Has no children
    "id": "4",
    "type": "test_block",
    "test_block": {"rich_text": [{"plain_text": "Block 4"}]},
    "has_children": False,
}

# LEVEL 1 BLOCKS
BLOCK_11 = {
    "id": "11",
    "type": "text_block",
    "text_block": {"rich_text": [{"plain_text": "Child 1 of block 1"}]},
    "has_children": False,
}
BLOCK_12 = {
    "id": "12",
    "type": "text_block",
    "text_block": {"rich_text": [{"plain_text": "Child 2 of block 1"}]},
    "has_children": True,
}
BLOCK_21 = {
    "id": "21",
    "type": "text_block",
    "text_block": {"rich_text": [{"plain_text": "Child 1 of block 2"}]},
    "has_children": False,
}
BLOCK_22 = {
    "id": "22",
    "type": "text_block",
    "text_block": {"rich_text": [{"plain_text": "Child 2 of block 2"}]},
    "has_children": False,
}
BLOCK_31 = {
    "id": "31",
    "type": "text_block",
    "text_block": {"rich_text": [{"plain_text": "Child 1 of block 3"}]},
    "has_children": True,
}
BLOCK_32 = {
    "id": "32",
    "type": "table_row",
    "table_row": {"cells": [[{"plain_text": "Child 2 of block 3"}]]},
    "has_children": False,
}

# LEVEL 2 BLOCKS
BLOCK_121 = {
    "id": "121",
    "type": "text_block",
    "text_block": {"rich_text": [{"plain_text": "Child 1 of block 12"}]},
    "has_children": True,
}
BLOCK_311 = {
    "id": "311",
    "type": "text_block",
    "text_block": {"rich_text": [{"plain_text": "Child 1 of block 3"}]},
    "has_children": True,
}
BLOCK_312 = {
    "id": "312",
    "type": "table_row",
    "table_row": {"cells": [[{"plain_text": "Child 1 of block 3"}]]},
    "has_children": True,
}

# SINGLE TEXT AND CELLS BLOCKS
BLOCK_WITH_RICH_TEXT = {
    "type": "text_block",
    "text_block": {
        "rich_text": [
            {"plain_text": "Test"},
            {"plain_text": "text"},
            {"plain_text": "for"},
            {"plain_text": "block"},
        ]
    },
}
BLOCK_WITH_CELLS = {
    "type": "table_row",
    "table_row": {
        "cells": [
            [
                {"plain_text": "Test"},
                {"plain_text": "text"},
                {"plain_text": "for"},
                {"plain_text": "block"},
            ]
        ]
    },
}

BLOCK_WITH_TEXT_RESULT = "Test text for block"

MOCK_DATABASE_PAGES = {
    "results": [
        {
            "id": "an-id",
            "properties": {
                "prop1": {"type": "other_type", "multi_select": []},
                "prop2": {"id": "title", "type": "title", "title": []},
            },
        },
        {
            "id": "another-id",
            "properties": {
                "prop1": {"type": "multi_select", "multi_select": "something"},
                "prop2": {"type": "title", "title": [{"plain_text": "Test text"}]},
            },
        },
        {"id": "third-id", "properties": {"prop2": {"type": "title", "title": [{"plain_text": "Test text 2"}]}}},
    ]
}
