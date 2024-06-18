from collections.abc import Iterator

import requests

from loaders.common.base_loader import Document, RsBaseLoader
from loaders.web_loader.config import WEBFLOW_API_TOKEN, WEBFLOW_API_URL, WEBFLOW_COLLECTION_ID
from loaders.web_loader.utils.webflow_data_processor import document_generator
from logger import set_log_level

set_log_level()


class WebflowLoader(RsBaseLoader):
    """
    Retrieve data from a Webflow collection
    """

    def __init__(self) -> None:
        self.collection_id = WEBFLOW_COLLECTION_ID
        self.api_token = WEBFLOW_API_TOKEN
        self.api_url = WEBFLOW_API_URL

    def lazy_load(self) -> Iterator[Document]:
        headers = {"accept": "application/json", "authorization": f"Bearer {self.api_token}"}
        limit = 100
        offset = 0
        total = None

        while True:
            url = f"{self.api_url}/collections/{self.collection_id}/items?limit={limit}&offset={offset}"
            try:
                response = requests.get(url, headers=headers)
                response.raise_for_status()
                data = response.json()

                if total is None:
                    total = data["pagination"]["total"]

                for item in data["items"]:
                    yield document_generator(item)

                offset += limit

                if offset >= total:
                    break

            except requests.exceptions.HTTPError as http_err:
                print(f"HTTP error occurred: {http_err}")
                break
            except Exception as error:
                print(f"An unexpected error occurred: {error}")
                break
