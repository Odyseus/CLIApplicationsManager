
Detailed Usage
==============

.. include:: ../0-common/cli-options.restructuredtext
- ``-a`` or ``--app=<name>``:  Specify one or more application names to work with. If this option isn't specified on the commands that make use of it, the command will work with all available applications.

Commands
--------

app.py app_repos
^^^^^^^^^^^^^^^^

Perform tasks on the applications repositories managed by this application. See ``repo`` command for sub-commands.

app.py bump_app_version
^^^^^^^^^^^^^^^^^^^^^^^

Bump all applications or only the specified applications versions. See ``--app`` option.

app.py gen_base_app
^^^^^^^^^^^^^^^^^^^

Generate a new base (*empty*) application from a template.

app.py gen_docs
^^^^^^^^^^^^^^^

Generate documentation page.

Options
~~~~~~~

- ``-f`` or ``--force-clean-build``: Clear doctree cache and destination folder when building the documentation.
- ``-u`` or ``--update-inventories``: Update inventory files from their on-line resources when building the documentation. Inventory files will be updated automatically if they don't already exist.

app.py gen_docs_no_api
^^^^^^^^^^^^^^^^^^^^^^

Same as ``gen_docs`` command, but without extracting Python modules docstrings. Same options apply.

app.py gen_readmes
^^^^^^^^^^^^^^^^^^

Generate README files for all managed applications, including the applications manager.

app.py gen_sys_exec_all
^^^^^^^^^^^^^^^^^^^^^^^

Create an executable for all managed applications on the system PATH to be able to run them from anywhere. For creating an executable for an individual application, each one of the applications has a system executable generation mechanism.

app.py gen_sys_exec_self
^^^^^^^^^^^^^^^^^^^^^^^^

Create an executable for this application on the system PATH to be able to run it from anywhere.

app.py install_deps
^^^^^^^^^^^^^^^^^^^

Install the dependencies for all managed applications of just for the specified ones. See ``--app`` option.

app.py repo
^^^^^^^^^^^

Perform tasks on this application repository.

Sub-commands
~~~~~~~~~~~~

- ``submodules``: Manage repository's sub-modules.

    + ``init``: Initialize sub-modules.
    + ``update``: Update sub-modules.

- ``subtrees``: Manage repository's sub-trees.

    + ``init``: Initialize sub-trees.
    + ``update``: Update sub-trees.

app.py run_cmd_on_app
^^^^^^^^^^^^^^^^^^^^^

Run a command on all managed applications or only on the specified ones. See ``--parallel`` and ``--command`` options.

Options
~~~~~~~

- ``-c <command>`` or ``--command=<command>``: Command to execute inside a managed application folder.
- ``-p`` or ``--parallel``: Run command in parallel instead of after finishing each command execution.
