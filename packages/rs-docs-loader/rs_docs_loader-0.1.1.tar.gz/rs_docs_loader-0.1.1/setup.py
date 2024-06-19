from pathlib import Path

from setuptools import find_packages, setup

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="rs-docs-loader",
    version="0.1.1",
    description="RS Docs Loader will help you to integrate different data sources",
    author="Rootstrap",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[
        "chroma==0.2.0",
        "chromadb==0.5.0",
        "google-api-python-client==2.129.0",
        "google-auth-httplib2==0.2.0",
        "google-auth-oauthlib==1.2.0",
        "langchain-core==0.2.0",
        "langchain-google-community==1.0.4",
        "langchain-openai==0.1.7",
        "langchain_text_splitters==0.2.0",
        "notion-client==2.2.1",
        "openai==1.31.1",
        "tiktoken==0.7.0",
        "psycopg2==2.9.9",
        "pydantic==2.7.1",
        "python-dotenv==1.0.1",
        "unstructured[pdf]==0.14.2",
    ],
)
