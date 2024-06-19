from copy import deepcopy

from loaders.notion_loader.tests.constants import (
    BLOCK_0,
    BLOCK_1,
    BLOCK_2,
    BLOCK_3,
    BLOCK_4,
    BLOCK_11,
    BLOCK_12,
    BLOCK_21,
    BLOCK_22,
    BLOCK_31,
    BLOCK_32,
    BLOCK_121,
    BLOCK_311,
    BLOCK_312,
)


class MockNotionAPIData:
    BLOCKS = {
        # ROOT
        "0": BLOCK_0,
        # LEVEL 0 BLOCKS
        "1": BLOCK_1,
        "2": BLOCK_2,
        "3": BLOCK_3,
        "4": BLOCK_4,
        # LEVEL 1 BLOCKS
        "11": BLOCK_11,
        "12": BLOCK_12,
        "21": BLOCK_21,
        "22": BLOCK_22,
        "31": BLOCK_31,
        "32": BLOCK_32,
        # LEVEL 2 BLOCKS
        "121": BLOCK_121,
        "311": BLOCK_311,
        "312": BLOCK_312,
    }
    CHILDREN = {
        "0": [BLOCK_1, BLOCK_2, BLOCK_3, BLOCK_4],
        "1": [BLOCK_11, BLOCK_12],
        "2": [BLOCK_21, BLOCK_22],
        "3": [BLOCK_31, BLOCK_32],
        "4": [],
        "11": [],
        "12": [BLOCK_121],
        "21": [],
        "22": [],
        "31": [BLOCK_311, BLOCK_312],
        "32": [],
    }
    PAGES = {
        "0": {"url": "http://root-url.test"},
        "2": {"url": "http://child-page-1.test"},
    }

    def get_blocks(self, block_ids):
        return deepcopy([self.BLOCKS[block_id] for block_id in block_ids])

    def get_block_children(self, block_id):
        return deepcopy(self.CHILDREN[block_id])

    def get_page_data(self, page_id):
        return deepcopy(self.PAGES[page_id])


def mock_blocks_retrieve(block_id):
    api_data = MockNotionAPIData()
    return api_data.get_blocks(block_ids=[block_id])[0]


def mock_blocks_children_list(block_id):
    api_data = MockNotionAPIData()
    return {"results": api_data.get_block_children(block_id=block_id)}


def mock_pages_retrieve(page_id):
    api_data = MockNotionAPIData()
    return api_data.get_page_data(page_id)


def mock_page_url(page_id):
    api_data = MockNotionAPIData()
    return api_data.get_page_data(page_id)["url"]
