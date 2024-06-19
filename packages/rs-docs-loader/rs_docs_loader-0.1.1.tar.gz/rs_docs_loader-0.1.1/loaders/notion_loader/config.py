import os

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Maximum depth at which text will be extracted from a block childs
CHILDREN_BLOCK_DEPTH = int(os.getenv("CHILDREN_BLOCK_DEPTH", default=2))

# Max request per second to the notion API
MAX_REQUESTS_PER_SECOND = 3

# Notion API token
NOTION_TOKEN = os.getenv("NOTION_TOKEN")
