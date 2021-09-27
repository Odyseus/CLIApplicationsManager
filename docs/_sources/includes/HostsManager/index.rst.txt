
*****************************
Hosts Manager's documentation
*****************************

.. only:: html

    A |CLI| utility written in Python 3 to manage hosts files on GNU/Linux.

.. include:: ../0-common/system-executable-hint.restructuredtext

|CLI| Synopsis
==============

.. only:: html

    .. docopt-docstring:: hostsmanager

.. only:: man

    .. custom-literalinclude:: hostsmanager-usage

Mentions
========

Application inspired and heavily based on the ``updateHostsFile.py`` Python script found on `StevenBlack's repository <https://github.com/StevenBlack/hosts>`__.

Requirements
============

No mayor requirements are needed to run this application other than Python 3.5+.

.. contextual-admonition::
    :context: info
    :title: Optional dependencies

    - ``jsonschema>3`` Python module.

``jsonschema`` module
---------------------

The ``jsonschema`` module is used to validate all data used by this |CLI| application. If not installed, the data will simply not be validated.

.. include:: ./usage.restructuredtext

.. include:: ./templates.restructuredtext
