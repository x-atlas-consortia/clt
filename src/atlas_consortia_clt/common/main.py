import argparse
import collections
import os.path
import re
import requests
import subprocess
import sys
import tempfile

from atlas_consortia_clt import __version__
from atlas_consortia_clt.common.config import Config


# This handles the argument parsing for the command line interface. Business logic is relegated to the individual
# functions corresponding to each subcommand
def launch_command(config: Config):
    # Configure the top level Parser
    parser = argparse.ArgumentParser(prog=config.name, description=f"{config.consortium} Command Line Transfer", usage=config.help_txt)
    subparsers = parser.add_subparsers()

    # Create Subparsers to give subcommands
    parser_transfer = subparsers.add_parser("transfer", prog=f"{config.name}-transfer", usage=config.help_txt, help=None)
    parser_transfer.add_argument("manifest_file_path", type=str)
    parser_transfer.add_argument("-d", "--destination", default=f"{config.consortium.lower()}-downloads", type=str)

    parser_login = subparsers.add_parser("login", usage=config.help_txt, help=None, prog=f"{config.name}-login")

    parser_whoami = subparsers.add_parser("whoami", usage=config.help_txt, help=None, prog=f"{config.name}-whoami")

    parser_logout = subparsers.add_parser("logout", usage=config.help_txt, help=None, prog=f"{config.name}-logout")

    # Assign subparsers to their respective functions
    parser_transfer.set_defaults(func=transfer, config=config)
    parser_login.set_defaults(func=login)
    parser_whoami.set_defaults(func=whoami)
    parser_logout.set_defaults(func=logout)

    # Parse the arguments and call appropriate functions
    if len(sys.argv) == 1 or "-h" in sys.argv or "--help" in sys.argv:
        print("usage: ", end="")
        print(config.help_txt)
        sys.exit(0)
    if "-v" in sys.argv or "--version" in sys.argv:
        print(f"version: {__version__}")
        sys.exit(0)
    args = parser.parse_args()
    args.func(args, config)


# This is the primary function of the clt. Accepts a single mandatory argument which is the path/name of a
# manifest file. A transfer is initiated from the uuid's and paths located within the file. Also accepts an optional
# arguments --destination or -d which chooses a specific download location
def transfer(args, config: Config):
    # Verify existence of the manifest file
    file_name = args.manifest_file_path
    if not os.path.exists(file_name):
        print(f"The file {file_name} cannot be found. You may need to include the path to the file. Example: \n"
              f"Documents/manifest.txt \n")
        sys.exit(1)

    # Obtain the local-id of the endpoint
    local_id_process = subprocess.Popen(["globus", "endpoint", "local-id"], stdout=subprocess.PIPE)
    local_id = local_id_process.communicate()[0].decode("utf-8")
    if local_id_process.returncode != 0:
        print(local_id)
        sys.exit(1)

    # Verify that the endpoint is connected
    endpoint_show_process = subprocess.Popen(["globus", "endpoint", "show", local_id], stdout=subprocess.PIPE)
    endpoint_show = endpoint_show_process.communicate()[0].decode("utf-8")
    if endpoint_show_process.returncode != 0:
        print(endpoint_show)
        sys.exit(1)
    endpoint_connected = False
    for line in endpoint_show.splitlines():
        if line.startswith("GCP Connected"):
            colon_index = line.find(":") + 1
            substring = line[colon_index:].strip()
            if substring == "True":
                endpoint_connected = True
    if endpoint_connected is False:
        print(f"The endpoint {local_id} \nis not active. Please consult the Globus Connect documentation  \n"
              f"to start the local endpoint. Once the endpoint is connected, try again")
        sys.exit(1)

    # Open the manifest file and verify the contents
    f = open(file_name, "r")

    # A list of the ID's is necessary to send to the ingest webservice.
    id_list = set()
    # entity id: [specific path, specific path, ...]
    manifest_lists = collections.defaultdict(list)
    for x in f:
        if x.startswith("dataset_id") is False:
            if x != "" and x != "\n":
                pattern = "^(\\S+)[ \t]+([^\t\n]+)"
                matches = re.search(pattern, x)
                if matches is None:
                    print(f"There was a problem with one of the entries in {file_name}. Please review {file_name} and "
                          f"for any formatting errors")
                    sys.exit(1)
                id_list.add(matches.group(1).strip('"'))
                manifest_lists[matches.group(1).strip('"')].append(matches.group(2).strip('"'))
    if len(id_list) == 0:
        print(f"File {file_name} contained nothing or only blank lines. \n"
              f"Each line on the manifest must be the id for the dataset/upload, followed by its path and \n"
              f"separated with a space. Example: {config.entity_id} /expr.h5ad")
        sys.exit(1)
    # send the list of uuid's to the ingest webservice to retrieve the endpoint uuid and relative path.
    r = requests.post(f"{config.ingest_url}/entities/file-system-rel-path", json=list(id_list))
    path_json = r.json()
    if r.status_code != 200:
        print(f"There were problems with {len(path_json)} dataset id's in {file_name}:\n")
        for each in path_json:
            print(f"{each['id']}: {each['message']} \n")
        sys.exit(1)

    globus_endpoints = collections.defaultdict(list)
    for item in path_json:
        entity_id = item["id"]
        manifest_items = [{**item, "specific_path": m} for m in manifest_lists[entity_id]]
        globus_endpoints[item["globus_endpoint_uuid"]].extend(manifest_items)

    at_least_one_success = []
    for globus_endpoint_uuid in list(globus_endpoints.keys()):
        endpoint_items = globus_endpoints[globus_endpoint_uuid]
        is_successful = batch_transfer(endpoint_items, globus_endpoint_uuid, local_id, args, config)
        if is_successful:
            at_least_one_success.append(globus_endpoint_uuid)
    if len(at_least_one_success) > 0:
        destination = args.destination.replace("\\", os.sep)
        destination = destination.replace("/", os.sep)
        print(f"Globus transfer successfully initiated. Files to be downloaded to <Home-Folder>/{destination} where "
              f"Home-Folder is the default download\ndirectory designated by Globus Connect Personal. "
              f"For instructions on how to view the current GCP download directory, visit:\n"
              f"{config.docs_url}. \n\nDownloading from endpoint(s): ")
        for endpoint in at_least_one_success:
            print(f"\t{endpoint}")
        print("\nThe status of the transfer(s) may be found at https://app.globus.org/activity. For more information,"
              " please consult the documentation")


# Construct the file used for the globus batch tranfer. Each source endpoint id needs a separate globus transfer.
# This also allows each one to have a unique task id which is relayed back to the user. A temporary file is created
# and lines from the incoming manifest file are transformed into how they are needed by globus
def batch_transfer(endpoint_list, globus_endpoint_uuid, local_id, args, config: Config):
    temp = tempfile.NamedTemporaryFile(mode="w+t", delete=False)
    entity_id_name = config.entity_id_name
    for each in endpoint_list:
        is_directory = False
        destination = args.destination.replace("\\", "/")
        # We use "/" rather than os.sep because the file system for globus always uses "/"
        if each["specific_path"] == "/":
            full_path = each["rel_path"] + "/"
        else:
            full_path = each["rel_path"].replace("\\", "/") + "/" + each["specific_path"].lstrip("/")
        if os.path.basename(full_path) == "":
            is_directory = True
        if is_directory is False:
            line = f'"{full_path}" "~/{destination}/{each[entity_id_name]}-{each["uuid"]}/{os.path.basename(full_path)}" \n'
        else:
            if each["specific_path"] != "/":
                slash_index = full_path.rstrip('/').rfind("/")
                local_dir = full_path[slash_index:].rstrip().rstrip("/")
            else:
                local_dir = "/"
            line = f'"{full_path}" "~/{destination}/{each[entity_id_name]}-{each["uuid"]}/{local_dir.lstrip("/")}" --recursive \n'
        line = line.replace("\\", "/")
        temp.write(line)
    temp.seek(0)
    globus_transfer_process = subprocess.Popen(["globus", "transfer", globus_endpoint_uuid, local_id, "--batch",
                                                temp.name], stdout=subprocess.PIPE)
    globus_transfer = globus_transfer_process.communicate()[0].decode("utf-8")
    temp.close()
    os.unlink(temp.name)
    if globus_transfer_process.returncode != 0:
        print(f"Transfer failure for endpoint with ID {globus_endpoint_uuid}")
        print(globus_transfer)
        return False
    print(globus_transfer)
    return True


# Makes the command "globus whoami". If the user is logged in, their identity will be printed. If they are not
# Logged in, they will be prompted to use the command "login"
def whoami(args, config: Config):
    whoami_process = subprocess.Popen(["globus", "whoami"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    whoami_show = whoami_process.communicate()[0].decode("utf-8")
    if whoami_process.returncode == 0:
        print(whoami_show)
    else:
        print(f"You are not logged in. Login with '{config.name} login'")


# Forces a login to globus through the default web browser
def login(args, config: Config):
    # Check if the user is logged in
    whoami_process = subprocess.Popen(["globus", "whoami"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    whoami_show = whoami_process.communicate()[0].decode("utf-8").strip()
    if whoami_process.returncode == 0:
        print(f"You are already logged in as {whoami_show}. Logout with '{config.name} logout'")
        return

    print(f"You are running '{config.name} login', which should automatically open a browser window for you to login.\n")
    login_process = subprocess.Popen(["globus", "login", "--force"], stdout=subprocess.PIPE)
    login_process.wait()
    print(f"You have successfully logged in to the {config.consortium} Command-Line Transfer! You can check your primary identity "
          f"with {config.name} whoami.\nLogout of the {config.consortium} Command-Line Transfer with '{config.name} logout'")
    login_process.communicate()[0].decode('utf-8')


# Logs the user out of globus
def logout(args, config: Config):
    # Check if the user is logged in
    whoami_process = subprocess.Popen(["globus", "whoami"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    whoami_process.communicate()[0].decode("utf-8").strip()
    if whoami_process.returncode != 0:
        print(f"You are not logged in. Login with '{config.name} login'")
        return

    # Prompt the user to confirm that they want to logout
    user_input = None
    while user_input is None or user_input.lower() not in ["y", "n", ""]:
        user_input = input("Are you sure you want to logout? [y/N]: ")

    if user_input.lower() != "y":
        print("Logout cancelled.")
        return

    # Logout of globus
    logout_process = subprocess.Popen(["globus", "logout", "--yes"], stdout=subprocess.PIPE)
    logout_process.wait()
    print(f"\nYou are now successfully logged out of the {config.consortium} Command-Line Transfer.")
