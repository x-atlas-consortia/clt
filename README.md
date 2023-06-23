# Command-Line Transfer

Command-Line Transfer (CLT) is a command-line interface (CLI) used to download multiple files and directories from the Globus file transfer service. The CLT initiates a transfer from a Globus endpoint to the [Globus Connect Personal](https://www.globus.org/globus-connect-personal) application. CLT is a generic project used by HuBMAP and SenNet for their respective CLT distributions.

## Building and Publishing

A `clt/app.cfg` configuration file is required to build a specific distribution of the CLT. Example `app.cfg` files for HuBMAP and SenNet are
located in the `clt` directory.

See the [Python Documentation](https://packaging.python.org/en/latest/tutorials/packaging-projects/#generating-distribution-archives) for detailed instructions on building and publishing the distribution.