from __future__ import annotations


def get_help(config: Config) -> str:
    """Returns a help message for the command line tool."""

    return f"""
        {config.name} [-h | --help] [transfer <PATH/TO/MANIFEST/FILE> | login | logout | whoami]

        {config.consortium} Command-Line Transfer

        A utility to bulk download {config.consortium} data by specifying the directories and/or
        files in a manifest file. For detailed documentation see:
        {config.docs_url}

        Commands: One of the following commands is required:

        transfer <PATH/TO/MANIFEST/FILE>    Transfer files specified in manifest-file (see
                                            below for example) using Globus Transfer.
                                            The transferred files will be stored in the
                                            directory "{config.consortium.lower()}-download" under the user's
                                            home directory or in the directory specified using the optional 
                                            --destination argument.

        login                               Login to Globus

        logout                              Logout of Globus

        whoami                              Displays the information of the user who is
                                            currently logged in.  If no user is logged
                                            a message will be displayed prompting the user
                                            to log in.

        -h or --help                        Show this help message.

        -v or --version                     Show current installed version of {config.name}.

        -d or --destination                 Manually select a download location within the user's
                                            home directory. For example:
                                            '{config.name} transfer manifest-file -d Desktop'
                                            will download to the user's Desktop directory. The 
                                            directory will be created under the user home directory
                                            if it doesn't already exist.

        Manifest Files:
        Manifest files contain two columns: the {config.consortium} identifer and the file or directory specifier. 
        Additional information to the right of the second column, separated by a tab, can be included. An
        optional single header line starting with the column specifier "dataset_id" will be ignored.

        Example manifest files:

        654418415bed5ecb9596b17a0320a2c6 /	# retrieves all files for given dataset uuid
        {config.entity_id} /rawMicroscopy/VAN0009-LK-102-7-AF_preIMS_unregistered.czi	# retrieves czi file for dataset {config.entity_id}

        dataset_id	file_or_dir_specifier   # header line is ignored
        60ed8e03152b51d5d9c8fc04e20fa5e3 /  # retrieve all files for given dataset uuid
        {config.entity_id} /ometiffs/VAN0016-LK-202-89-IMS_PosMode_multilayer.ome.tiff  # retrieves image file for dataset {config.entity_id}
        {config.entity_id} /ometiffs/separate/  # retrieves directory of files for dataset {config.entity_id}
    """
