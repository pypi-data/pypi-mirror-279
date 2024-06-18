from setuptools import setup, find_packages


setup(
    name='rs-docs-loader',
    version='0.0.7',
    description='RS Docs Loader will help you to integrate different data sources',
    author='Rootstrap',
    packages=find_packages(),
    install_requires=[
      "openai==1.31.1",
      "chroma==0.2.0",
      "chromadb==0.5.0",
      "tiktoken==0.7.0",
      "langchain-openai==0.1.7",
      "langchain-core==0.2.0",
      "python-dotenv==1.0.1",
      "langchain-google-community==1.0.4",
      "google-api-python-client==2.129.0",
      "google-auth-httplib2==0.2.0",
      "google-auth-oauthlib==1.2.0",
      "unstructured[pdf]==0.14.2",
      "notion-client==2.2.1",
      "pydantic==2.7.1",
      "psycopg2==2.9.9",
      "langchain_text_splitters==0.2.0"
    ]
)
