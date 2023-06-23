def get_help(name: str, author: str, ex_entity_id: str, help_url: str):
    """Returns a help message for the command line tool."""

    return f"""
        {name} [-h | --help] [transfer manifest-file | login | logout | whoami]

        {author} Command Line Transfer

        A utility to bulk download {author} data by specifying the directories and/or
        files in a manifest file. For detailed documentation see:
        {help_url}

        Commands: One of the following commands is required:

        transfer manifest-file   Transfer files specified in manifest-file (see
                                 below for example) using Globus Transfer.
                                 The transfered files will be stored in the
                                 directory "{author.lower()}-download" under the user's
                                 home directory.

        login                    Login to Globus

        logout                   Logout of Globus

        whoami                   Displays the information of the user who is
                                 currently logged in.  If no user is logged
                                 a message will be displayed prompting the user
                                 to log in.

        -h or --help             Show this help message.

        -v or --version          Show current installed version of {name}.

        -d or --destination      Manually select a download location within the user's
                                 home directory. For example:
                                 '{name} transfer manifest-file -d Desktop'
                                 will download to the user's Desktop directory. The 
                                 directory will be created under the user home directory
                                 if it doesn't already exist.

        Manifest Files:
        Manifest files contain two columns: the {author} identifer and the file or directory specifier. 
        Additional information to the right of the second column, separated by a tab, can be included. An
        optional single header line starting with the column specifier "dataset_id" will be ignored.

        Example manifest files:

        654418415bed5ecb9596b17a0320a2c6 /	# retrieves all files for given dataset uuid
        {ex_entity_id} /rawMicroscopy/VAN0009-LK-102-7-AF_preIMS_unregistered.czi	# retrieves czi file for dataset {ex_entity_id}

        dataset_id	file_or_dir_specifier   # header line is ignored
        60ed8e03152b51d5d9c8fc04e20fa5e3 /  # retrieve all files for given dataset uuid
        {ex_entity_id} /ometiffs/VAN0016-LK-202-89-IMS_PosMode_multilayer.ome.tiff  # retrives image file for dataset {ex_entity_id}
        {ex_entity_id} /ometiffs/separate/  # retrieves directory of mages files for dataset {ex_entity_id}
    """