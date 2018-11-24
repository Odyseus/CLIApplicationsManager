
Detailed usage
==============

.. warning::

    Always use the ``--dry-run`` |CLI| option to see the exact command/s that will be executed.

.. contextual-admonition::
    :context: info
    :title: Highlights

    - Backup tasks are read from configuration files located in **UserData/tasks/*.py**.
    - Global settings are read from configuration files located in **UserData/settings/*.py**.
    - Each tasks file can have defined their own settings and contain one or more backup tasks of any type.

.. include:: ../0-common/cli-options.restructuredtext

Commands
--------

app.py backup
^^^^^^^^^^^^^

The main command to perform backup tasks.

Options
~~~~~~~

- ``-t <name>`` or ``--task=<name>``: File name of the file containing the backup tasks. Should be the name of a file stored in **UserData/tasks/<name>.py**. Extension omitted.
- ``-g <name>`` or ``--global=<name>``: File name of the file containing the global settings that all the backup tasks will use. Should be the name of a file stored in **UserData/settings/<name>.py**. Extension omitted.
- ``-d`` or ``--dry-run``: Do not perform file system changes. Only display messages informing of the actions that will be performed or commands that will be executed.

    .. warning::

        Some file system changes will be performed (e.g. temporary files creation).


app.py print_tasks
^^^^^^^^^^^^^^^^^^

Command only used by the Bash completions script to assist in the auto-completion of the ``-t <name>`` or ``--task=<name>`` |CLI| options.

app.py print_settings
^^^^^^^^^^^^^^^^^^^^^

Command only used by the Bash completions script to assist in the auto-completion of the ``-g <name>`` or ``--global=<name>`` |CLI| options.

.. include:: ../0-common/generate-command.restructuredtext

