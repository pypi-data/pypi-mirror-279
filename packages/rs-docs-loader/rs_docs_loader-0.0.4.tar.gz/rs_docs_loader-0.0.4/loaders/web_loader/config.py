import os

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Webflow API token
WEBFLOW_API_TOKEN = os.getenv("WEBFLOW_API_TOKEN")

# ID of the Webflow collection from which data will be fetched
WEBFLOW_COLLECTION_ID = os.getenv("WEBFLOW_COLLECTION_ID")

# Base URL of the Webflow API
WEBFLOW_API_URL = os.getenv("WEBFLOW_API_URL")

# Base URL of the blog
BLOG_URL = os.getenv("BLOG_URL")
