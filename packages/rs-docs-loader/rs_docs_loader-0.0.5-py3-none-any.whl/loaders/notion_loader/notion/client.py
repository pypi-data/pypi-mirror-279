from notion_client import Client

from loaders.notion_loader.config import NOTION_TOKEN


def get_notion_client() -> Client:
    return Client(auth=NOTION_TOKEN)
