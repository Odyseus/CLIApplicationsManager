.. Abbreviations

.. |CLI| replace:: :abbr:`CLI (Command Line Interface)`

***************************
Backup Utils' documentation
***************************

.. only:: html

    A |CLI| utility to backup files on GNU/Linux.

.. include:: ../0-common/system-executable-hint.restructuredtext

|CLI| Synopsis
==============

.. only:: html

    .. docopt-docstring:: backuputils

.. only:: man

    .. custom-literalinclude:: backuputils-usage

Mentions
========

Application inspired by the `backup-utils <https://gitlab.com/Oprax/backup-utils>`__ Python module.

.. _backup-utils-requirements-reference:

Requirements
============

No mayor requirements are needed to run this application other than Python 3.5+.

.. contextual-admonition::
    :context: info
    :title: Mail system optional requirement

    - ``keyring`` module.

``keyring`` module
------------------

This module is only used by the email system and it is used to retrieve a password stored in the system's default keyring. This module is optional because the mail system can be configured to ask for a password. This application will not store nor use passwords saved in plain text.

The following command executed from a terminal will prompt for a password that will be stored into the system's keyring:

.. code:: shell

    $ keyring set backup_secret_service_name backup_secret_user_name

Then the password is retrieved from the system's keyring by the application email system using the ``secret_service_name`` and ``secret_user_name`` keys specified in the ``settings`` property from a **settings** file or a **tasks** file like so:

.. code:: python

    keyring.get_password("backup_secret_service_name", "backup_secret_user_name")

``backup_secret_service_name`` and ``backup_secret_user_name`` can have any other names that one deems to give them. As an example, in Gnome keyring, the details tab for the generated *storage* will display the following:

::

    username: backup_secret_user_name
    application: python-keyring
    service: backup_secret_service_name

.. include:: ./usage.restructuredtext

.. include:: ./templates.restructuredtext

.. include:: ./tasks.restructuredtext
