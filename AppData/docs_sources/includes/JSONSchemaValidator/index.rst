
*************************************
JSON Schema Validator's documentation
*************************************

.. only:: html

    A |CLI| utility written in Python 3 to validate data from JSON schemas on GNU/Linux.

.. include:: ../0-common/system-executable-hint.restructuredtext

|CLI| Synopsis
==============

.. only:: html

    .. docopt-docstring:: jsonschemavalidator

.. only:: man

    .. custom-literalinclude:: jsonschemavalidator-usage

Mentions
========

This application uses the `jsonschema <https://github.com/Julian/jsonschema>`__ Python module to validate data.

Requirements
============

.. contextual-admonition::
    :context: warning
    :title: Warning

    - Python 3.5+.
    - ``jsonschema`` module.

.. include:: ./usage.restructuredtext
