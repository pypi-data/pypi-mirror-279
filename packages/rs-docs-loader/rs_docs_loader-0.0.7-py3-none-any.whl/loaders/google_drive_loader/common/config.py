import os

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# The place where credentials is stored
CREDENTIAL_PATH = os.getenv("CREDENTIAL_PATH")
# The place where token is stored
TOKEN_PATH = os.getenv("TOKEN_PATH")
# The ID of the folder to lookup
FOLDER_ID = os.getenv("FOLDER_ID")
# Main credentials folder for Google Application
GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
