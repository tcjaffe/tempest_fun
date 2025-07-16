# Fun with the Tempest Weather Station API!
This is a toy project for interacting with the Tempest Weather Station API which is documented here: https://apidocs.tempestwx.com/reference/quick-start.
This is intended entirely for fun.  I connect to my own device and use the Personal Access Token flow.

## Setup instructions
The following instructions assume you are running on MacOS.

### Prerequisites
* A fully setup and running Tempest Weather Station
* Python.  I'm currently using 3.11.12.
* pyenv.  Use this to manage your python versions.
* direnv.  Use this to manage environment variables at the directory level.
* git

### Steps
1. Clone the repository into a directory on your local machine.
2. Set the python version: `pyenv local 3.11.12`
3. Follow the steps at https://apidocs.tempestwx.com/reference/quick-start to generate a Personal Access Token.
4. Create a .envrc file in the root directory of your project and add the following text, substituting your token from the previous step for {your token}: `export TEMPEST_TOKEN={your token}`
5. `direnv allow .`
6. `python -m venv tempest_venv`
7. `source tempest_venv/bin/activate`
8. Run the code!: `python tempest_api_client.py`
