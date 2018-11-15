
***************************
Backup Utils' documentation
***************************

.. only:: html

    A :abbr:`CLI (Command Line Interface)` utility written in Python 3 to backup files on GNU/Linux.

.. include:: ../0-common/system-executable-hint.restructuredtext

CLI Synopsis
============

.. only:: html

    .. docopt-docstring:: backuputils

.. only:: man

    .. custom-literalinclude:: backuputils-usage

Mentions
========

Application inspired by the `backup-utils <https://gitlab.com/Oprax/backup-utils>`__ Python module.

Requirements
============

No mayor requirements are needed to run this application other than Python 3.5+.

.. contextual-admonition::
    :context: warning
    :title: Mail system requirements

    - ``keyring`` module.

``keyring`` module
------------------

This module is only used by the email system and it is used to retrieve a password stored in the system's default keyring. This application will not store nor use passwords saved in plain text.

The following command executed from a terminal will store a password:

.. code:: shell

    $ keyring set backup_secret_context backup_secret_name

Then the password is retrieved by the application email system using the ``sender_secret`` tuple specified in ``global_settings`` like so:

.. code:: python

    keyring.get_password("backup_secret_context", "backup_secret_name")

``backup_secret_context`` and ``backup_secret_name`` can have any other names that one deems to give them. As to what these names actually mean, I have no idea. What I know is that in Gnome keyring, the details tab for the generated "storage" will display the following:

::

    username: backup_secret_name
    application: python-keyring
    service: backup_secret_context

.. include:: ./usage.rst
