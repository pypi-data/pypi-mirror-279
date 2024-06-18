# rs-docs-loaders
Python project designed to provide different document loaders from external sources like notion, Google Drive, etc.

## Setup environment
For a proper use of python, we should create a virtual environment (venv) to isolate the project packages from the global python configuration, to create this venv run:
* `python -m venv path/to/venv`

Then you need to activate this new venv, so for that run:
* `source path/to/venv/bin/activate`

Please take a look to this little guide about how to create and activate a [venv](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/#create-and-use-virtual-environments)

## Install dependencies
To install the project dependencies run `pip install -r requirements.txt`. This will install all the requirements for the project and all loaders requirements.

If you are a `dev`, you may want to install some dev dependencies to be able to use for example `black`, `isort`, `flake8`, etc. To install the dev dependencies run `pip install -r dev_requirements.txt`. This will install the same things as `requirements.txt`(step before) plus dev tools.

### Requirements structure
```
rs-docs-loaders/
|-- common/
|-- loaders/
|   |-- first_loader/
|   |   |-- tests/
|   |   |-- other_folder/
|   |   |-- first_loader.py
|   |   |-- requirements.txt
|   |   |-- README.md
|   |-- second_loader/
|   |   |-- tests/
|   |   |-- other_folder/
|   |   |-- second_loader.py
|   |   |-- requirements.txt
|   |   |-- README.md
|   |-- loaders_requirements.txt
|-- base_requirements.txt
|-- dev_requirements.txt
|-- requirements.txt
```

`requirements.txt` --> invoke `base_requirements.txt` and `loaders/loders_requirements.txt`

`base_requirements.txt` --> has all the dependencies for the base project.

`loaders/loaders_requirements.txt` --> has all the dependencies for the loaders.

`loaders/[loader-name]/requirements.txt` --> has all the dependencies for an specific loader.

`dev_requirements.txt` --> invoke `requirements.txt` + devs tools

### Install specific loader dependencies
To install a specific loader dependencies, you will need to install the base requirements for the proyect and then the loader specific requirements, so you can do something like: `pip install -r base_requirements.txt` and then `pip install -r loaders/[loader-name]/requirements.txt`

### Add a new loader
To add a new loader, you just need to create a new folder inside `loaders/` and must create a `requirements.txt` for this loader. Then you will need to update the `loaders/loaders_requirements.txt` to invoke the requirements for the new loader.

So in the `loaders/loaders_requirements.txt` you will need to add a new line: `-r [loader-name]/requirements.txt`. This will make that the new loaders requirements were installed when you install the `requirements.txt` placed in the root folder, making it dependencies available for CI, and basic project configuration.
