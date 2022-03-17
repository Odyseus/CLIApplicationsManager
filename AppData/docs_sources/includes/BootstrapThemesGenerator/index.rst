
*****************************************
Bootstrap Themes Generator' documentation
*****************************************

.. only:: html

    A |CLI| utility to assist in the creation of Bootstrap themes.

.. include:: ../0-common/system-executable-hint.restructuredtext

|CLI| Synopsis
==============

.. only:: html

    .. docopt-docstring:: bootstrapthemesgenerator

.. only:: man

    .. custom-literalinclude:: bootstrapthemesgenerator-usage

Requirements
============

.. contextual-admonition::
    :context: warning
    :title: Dependencies

    - Python 3.5+.
    - ``Dart Sass`` `Download the appropiate release <https://github.com/sass/dart-sass/releases>`__ and `see installation instructions <https://github.com/sass/dart-sass#standalone>`__.
    - ``Node.js`` installed on the system.
    - ``psutil`` Python module.

``psutil`` module
------------------

This module is only used to programmatically terminate the HTTP server used to host the themes preview page. Without this Python module, the server can only be stopped/restarted manually.

.. include:: ./usage.restructuredtext

.. include:: ./themes-creation.restructuredtext
