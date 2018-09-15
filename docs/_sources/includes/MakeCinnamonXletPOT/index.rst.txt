
**************************************
Make Cinnamon Xlet POT's documentation
**************************************

A :abbr:`CLI (Command Line Interface)` utility written in Python 3 to generate POT files for Cinnamon xlets.

Requirements
============

.. attention::

    No mayor requirements are needed to run this application other than Python 3 (Python 3.5+ to be precise).

Mentions
========

Application inspired by `the script with similar <https://github.com/linuxmint/Cinnamon/blob/master/files/usr/bin/cinnamon-xlet-makepot>`__ functions that comes with `Cinnamon Desktop Environment <https://github.com/linuxmint/Cinnamon>`__.

Differences with the original script
====================================

- Use of Python 3 instead of Python 2 on the script itself. Newer versions of the official script are already ported to Python 3.
- Possibility to scan Python files. Newer versions of the official script can also scan Python files.
- Possibility to set a custom header for the .pot file with data automatically generated and/or set through a settings file.
- Possibility to *blacklist* a set of preference keys found inside the **settings-schema.json** file so the generated .pot file doesn't need to be manually edited later.
- Possibility to pass more than one `--keyword` argument to the `xgettext`.
- Possibility to scan files outside the xlet folder.

.. include:: ./usage.rst
