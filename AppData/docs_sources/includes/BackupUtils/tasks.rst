
.. _backup-utils-task-types-reference:

Task types
==========

.. warning::

    Always use the ``--dry-run`` |CLI| option to see the exact command/s that will be executed.


.. _backup-utils-tar-local-type-reference:

tar_local
---------

This task uses the ``tar`` command available on a system to create an archive with the content of all the items (files and folder) defined in a task object.

.. contextual-admonition::
    :context: info
    :title: Highlights

    - This task can backup files and folders.
    - Only local file system paths are allowed.

Data keys specific to this task type
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. note::

    All data keys are of type string and are optional unless specified otherwise.

- ``tar_compression_level`` (**Default**: -7): A value between -1 and -9. This value is used to set environment variables used by ``tar`` (XZ_OPT, GZIP_OPT or BZIP2) to set a compression level. If no compression argument is defined in ``tar_func_args``, the environment variables will not be set and ``tar_compression_level`` will not be used.
- ``tar_func_args`` (**List**) (**Default**: empty (no function arguments are passed to ``tar``)): A list of function arguments used by the ``tar`` program. Possible values for the compression arguments are **--xz**, **-J**, **--gzip**, **-z**, **--bzip2** or **-j**. Do not use *old option style*, either use short options (e.g.: ``-j``) or long options (e.g.: ``--xz``). See `GNU tar manual <https://www.gnu.org/software/tar/manual/tar.html>`__.
- ``tar_opt_args`` (**List**): See :ref:`backup-utils-tar-local-type-reference`.

.. info::

    The final command that will be executed will look similar to the following:

    .. code:: shell

        tar --create [tar_func_args] --file /path/to/destination/[destination_prefix]2018-11-22_05.42.06.846.tar[extension_depending_on_tar_func_args_passed] --files-from=/path/to/tmp/file/with/valid/generated/paths [tar_opt_args]

.. _backup-utils-rsync-type-reference:

rsync_local
-----------

This task uses the ``rsync`` command available on a system to create a mirror of each folder (``items`` key) defined in a task object.

.. contextual-admonition::
    :context: info
    :title: Highlights

    - This task can only backup folders.
    - Only local file system paths are allowed.

Data keys specific to this task type
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. note::

    All data keys are of type string and are optional unless specified otherwise.

- ``rsync_args`` (**List**): Extra arguments passed to the ``rsync`` command.

.. info::

    The final command that will be executed will look similar to the following:

    .. code:: shell

        # The --exclude arguments are dynamically added based on values defined in ignored_patterns settings.
        rsync [rsync_args] --exclude=ptrn_1 --exclude=ptrn_n /path/to/folder/to/mirror /path/to/mirror/destination

