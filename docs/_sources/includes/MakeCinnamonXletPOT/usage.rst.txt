
Detailed usage
==============

Differences with the original script
====================================

- Use of Python 3 instead of Python 2 on the script itself. Newer versions of the official script are already ported to Python 3.
- Possibility to scan Python files. Newer versions of the official script can also scan Python files.
- Possibility to set a custom header for the .pot file with data automatically generated and/or set through a settings file.
- Possibility to *blacklist* a set of preference keys found inside the **settings-schema.json** file so the generated .pot file doesn't need to be manually edited later.
- Possibility to pass more than one `--keyword` argument to the `xgettext`.
- Possibility to scan files outside the xlet folder.

.. include:: ../0-common/cli-options.restructuredtext

Commands
--------

.. include:: ../0-common/generate-command.restructuredtext
