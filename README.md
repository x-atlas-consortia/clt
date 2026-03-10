# Command-Line Transfer

Command-Line Transfer (CLT) is a command-line interface (CLI) used to download multiple files and directories from the Globus file transfer service. The CLT initiates a transfer from a Globus endpoint to the [Globus Connect Personal](https://www.globus.org/globus-connect-personal) application. CLT provides `hubmap-clt` and `sennet-clt` command-line interfaces for HuBMAP and SenNet, respectively.

## Installation

### pip

Install the CLT globally using pip:
```
pip install atlas-consortia-clt
```

### pip with a virtual environment

Installing in a virtual environment keeps the CLT and its dependencies isolated from other Python projects.

**macOS/Linux:**
```
python3 -m venv clt-env
source clt-env/bin/activate
pip install atlas-consortia-clt
```

**Windows:**
```
python -m venv clt-env
clt-env\Scripts\activate
pip install atlas-consortia-clt
```

To use the CLT in the future, activate the virtual environment first:

**macOS/Linux:**
```
source clt-env/bin/activate
```

**Windows:**
```
clt-env\Scripts\activate
```

To deactivate the virtual environment, run the following command on any platform:
```
deactivate
```

### pipx

[pipx](https://pipx.pypa.io) installs the CLT in its own isolated environment and automatically exposes the `hubmap-clt` and `sennet-clt` commands on your `PATH`, without affecting other Python packages.

Install pipx if you don't have it. Check the [pipx documentation](https://pipx.pypa.io/stable/#install-pipx) for detailed installation instructions.

Then install the CLT. The CLT relies on the `globus-cli` package and must also be installed via pipx.
```
pipx install atlas-consortia-clt globus-cli
```

To upgrade:
```
pipx upgrade atlas-consortia-clt globus-cli
```

## Usage

CLT provides `hubmap-clt` and `sennet-clt` command-line interfaces. The following documentation uses `<consortium>-clt` in examples. Please replace `<consortium>` with `hubmap` or `sennet`.

Usage documentation can also be found by running the following command:
```
<consortium>-clt -h
```
### Login

A one-time login is required for any download session. For non-public data, you must log in with your HuBMAP or SenNet account. For publicly available data, you can log in with any account accepted by the login form (Google and ORCID). Log in can be initiated using the following command:

``` 
<consortium>-clt login
```

### Logout

Logout can be used to log out the current user.
```
<consortium>-clt logout
```

### Transfer

A data transfer and download can be initiated using the transfer command and a manifest file. You must be logged in to use the transfer command.
```
<consortium>-clt transfer <PATH/TO/MANIFEST/FILE> 
```
An optional destination argument can be specified. The destination is the directory on the user's computer where data will be downloaded. The directory will be created if it doesn't exist. The destination argument is relative to the user's home directory (~). For example, `--destination Desktop/<consortium>-data` corresponds to an absolute path of `~/Desktop/<consortium>-data`. The default destination directory is `~/<consortium>-downloads`.
```
<consortium>-clt transfer <PATH/TO/MANIFEST/FILE> --destination <PATH/TO/DESTINATION/DIRECTORY>
```
An optional `--from-protected-space` flag can be specified to download protected data belonging to a published protected `Dataset`. By default, the CLT will download public data only. The user must have access to the protected data in order for the transfer to be successful.
```
sennet-clt transfer <PATH/TO/MANIFEST/FILE> --from-protected-space
```

### Whoami

Whoami can be used to display the information of the currently logged in user.
``` 
<consortium>-clt whoami
```

## Additional Documentation

Additional documentation can be found at the [HuBMAP](https://docs.hubmapconsortium.org/clt) and [SenNet](https://docs.sennetconsortium.org/libraries/clt) documentation pages.


## Development

A `src/atlas_consortia_clt/common/app.cfg` configuration file is required to build the CLT. An example `app.cfg.example` file is located in the `src/atlas_consortia_clt/common` directory. Replace the values in `app.cfg.example` and rename the file to `app.cfg`.

When contributing to the CLT, run the following commands in the root directory to install the editable package.
```
python3 -m pip install --upgrade pip setuptools
python3 -m pip install -e .
```

### Building and Publishing

Install the `build` package and build the project by running the following commands in the root directory. These commands should generate a `dist` directory.
```
python3 -m pip install --upgrade build
python3 -m build
```

Install the `twine` package and upload the build files to PyPI by running the following commands. The second command will prompt for a PyPI username and password. 
```
python3 -m pip install --upgrade twine
python3 -m twine upload dist/*
```

See the [Python Documentation](https://packaging.python.org/en/latest/tutorials/packaging-projects/#generating-distribution-archives) for more detailed instructions on building and publishing.
