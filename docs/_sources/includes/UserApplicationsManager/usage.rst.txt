
Detailed usage
==============

Usage Synopsis
--------------

- A file named ``conf.py`` should exist inside the **UserData** folder.
- This file should contain a property named ``applications``.
- The ``applications`` property should contain a dictionary of named dictionaries.
- Each named dictionary represents an application and should be uniquely named (Duh!).
- Each application is checked for valid mandatory keys.
- The command ``app.py manage`` is used to manage all applications, or the selected ones or by ``type``.

.. include:: ../0-common/cli-options.restructuredtext
- ``-i <app_id>`` or ``--id=<app_id>``: The application's ID/s to manage. If not specified, all applications will be managed.
- ``-t <app_type>`` or ``--type=<app_type>``: Manage applications of this specified type. See ``type`` application key.
- ``-f`` or ``--force-update``: Force the management of all applications (or the specified ones), ignoring the frequency (and any other checks) in which they should be managed. See ``frequency`` application key.

Commands
--------

app.py manage
^^^^^^^^^^^^^

This command will perform different actions depending on the type of application and various conditions. All application types are

- ``git_repo`` or ``hg_repo``:

    + If the destination folder doesn't exists, it will perform a clone of the repository.
    + If the destination folder exists, a ``pull`` from the repository will be performed.
    + If the destination folder exists and it isn't a repository, manual intervention will be required.

- ``file``:

    + If the destination file doesn't exists, a new copy will be downloaded.
    + If the managed file comes from a Github repository's *API URL*, a file will be downloaded only if the tag names are different and/or the file hashes doesn't match.

- ``archive``:

    + Incomplete implementation.
    + There is no check for file/folder existence. Since a downloaded archive could have various destinations and be either files or folders or both.
    + If the managed archive comes from a Github repository's *API URL*, the archive will be downloaded only if the tag names are different. Files/Folders hashes aren't checked.

app.py print_app_ids
^^^^^^^^^^^^^^^^^^^^

Print on screen all applications IDs as defined in the ``conf.py`` file. This command is used by the Bash completions script to assist in the auto-completion of the ``-i`` and ``--id=`` options.

.. include:: ../0-common/generate-command.restructuredtext

Example configuration file
--------------------------

.. literalinclude:: ../../../../UserData/UserApplicationsManager/AppData/data/templates/conf.py
    :language: python

Application keys
----------------

- **name** (String|Mandatory): The name of an application.
- **type** (String|Mandatory): The application type that will decide how to handle downloaded application files.

    + ``git_repo`` or ``hg_repo``: The application is a Git or Mercurial repository.
    + ``file``: The application is a single file.
    + ``archive``: The application is an archive that needs to be unpacked.

- **url** (String|Mandatory): The URL where to download the application.
- **destination** (String|Mandatory): The final destination for an application.

    + ``git_repo`` or ``hg_repo``: The **destination** should always be a path to a folder.
    + ``file``: The **destination** should always be a path to a file.
    + ``archive``: The **destination** is not needed/used so it isn't mandatory for this type of application. See **unzip_targets** key.

- **frequency** (String|Optional): Frequency in which an application should be downloaded. If not specified, it defaults to ``w`` (weekly).

    + ``d`` (daily): An application is downloaded every time that it is managed.
    + ``w`` (weekly): An application is downloaded only if at least 6 days have passed since the last download.
    + ``m`` (monthly): An application is downloaded only if at least 28 days have passed since the last download.

- **github_api_asset_data** (Dictionary|Optional): This key must contain *matching data* and must be used only when an application **url** key points to a Github repository's *API URL*. The Github repository's *API URL* is used to download a JSON file with data about a repository release. The **name** key of each element of the array/list called **assets** of the downloaded JSON file is scanned for different matches to locate the URL of the asset that one actually wants to download. This key is only used by applications of **type** ``file`` or ``archive``. And needless to say that this key is mandatory when an application **url** key points to a Github repository's *API URL*. Otherwise, there wouldn't be a way to pinpoint the exact asset that needs to be downloaded.

    + ``asset_name_contains``: Self explanatory.
    + ``asset_name_starts``: Self explanatory.
    + ``asset_name_ends``: Self explanatory.

- **unzip_prog** (String|Mandatory): The name of the command used to unpack an archive. Key only used by applications of **type** ``archive``. As of now, only the ``tar`` command is implemented.
- **unzip_args** (String|Mandatory): Arguments passed to the command defined in **unzip_prog**. Key only used by applications of **type** ``archive``.
- **unzip_targets** (List|Mandatory): A list of tuples. At index zero of each tuple should be defined the path to a file/folder inside a downloaded archive. At index one should be defined the path to the folder where the target should be extracted. Key only used by applications of **type** ``archive``.
- **post_extraction_actions** (Dictionary|Optional): A list of actions to perform after an archive is extracted.

    + ``symlinks``: A list of tuples. At index zero, the path to a file/folder. At index one, the path to the generated symbolic link.
    + ``set_exec``: A list of file paths to set as executable.
