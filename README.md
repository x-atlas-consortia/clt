# Command-Line Transfer

Command-Line Transfer (CLT) is a command-line interface (CLI) used to download multiple files and directories from the Globus file transfer service. The CLT initiates a transfer from a Globus endpoint to the [Globus Connect Personal](https://www.globus.org/globus-connect-personal) application. CLT provides `hubmap-clt` and `sennet-clt` command-line interfaces for HuBMAP and SenNet, respectively.

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