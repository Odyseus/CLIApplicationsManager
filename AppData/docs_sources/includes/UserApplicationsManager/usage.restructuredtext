
Detailed usage
==============

.. contextual-admonition::
    :context: info
    :title: Highlights

    - A file named ``conf.py`` should exist inside the **UserData** folder.
    - This file should contain a property named ``applications``.
    - The ``applications`` property should contain a dictionary of named dictionaries.
    - Each named dictionary represents an application and should be uniquely named (Duh!).
    - Each application is checked for valid mandatory keys.
    - The command ``app.py manage`` is used to manage all applications, or the selected ones (``--id=<app_id>`` |CLI| option) or by type (``--type=<app_type>`` |CLI| option).

.. include:: ../0-common/cli-options.restructuredtext

Commands
--------

app.py manage
^^^^^^^^^^^^^

This command will perform different actions depending on the type of application and various conditions.

- For applications of type ``git_repo`` or ``hg_repo``:

    + If the destination folder doesn't exist, it will perform a clone of the repository.
    + If the destination folder exist, a ``pull`` from the repository will be performed.
    + If the destination folder exist and it isn't a repository, manual intervention will be required.

- For applications of type ``file``:

    + If the destination file doesn't exists, a new copy will be downloaded.
    + If the managed file comes from a Github repository's *API URL*, a file will be downloaded only if the tag names are different and/or the file hashes doesn't match.

- For applications of type ``archive``:

    + Incomplete implementation.
    + There is no check for file/folder existence. Since a downloaded archive could have various destinations and be either files or folders or both.
    + If the managed archive comes from a Github repository's *API URL*, the archive will be downloaded only if the tag names are different. Files/Folders hashes aren't checked.

Options
~~~~~~~

- ``-i <app_id>`` or ``--id=<app_id>``: The application's ID/s to manage. If not specified, all applications will be managed.
- ``-t <app_type>`` or ``--type=<app_type>``: Manage applications of this specified type. See ``type`` application key.
- ``-f`` or ``--force-update``: Force the management of all applications (or the specified ones), ignoring the frequency (and any other checks) in which they should be managed. See ``frequency`` application key.


app.py print_app_ids
^^^^^^^^^^^^^^^^^^^^

Command only used by the Bash completions script to assist in the auto-completion of the ``-i <app_id>`` or ``--id=<app_id>`` |CLI| options.

.. include:: ../0-common/generate-command.restructuredtext
