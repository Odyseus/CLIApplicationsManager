
*************************
General development notes
*************************

- :ref:`docopt-usage-notes-reference`
- :ref:`application-generation-reference`
- :ref:`docs-generation-reference`
- :ref:`sys-exec-generation-reference`
- :ref:`installing-dependencies-reference`

.. attention::

    All commands described in this page should be executed from the root folder of the main application (at the same level as the **AppData** folder).


.. _docopt-usage-notes-reference:

docopt module usage notes
=========================

The `docopt Python module <https://github.com/docopt/docopt>`__ is used as command line arguments parser for all |CLI| applications.

The ``docopt_doc`` variable defined in each **cli.py** file for each application is used to store/define the doc string that will be passed to ``docopt`` as the **doc** argument. This was done because, if I use a doc string that complies with Sphinx/RST, ``docopt`` will not parse it correctly. If I use a doc string that complies with ``docopt``, Sphinx doesn't SHUT UP about incorrect indentations and the likes. So, I store the *``docopt`` document* in a variable. This will SHUT UP Sphinx because it *cannot see* the doc string. The variable then is explicitly passed to ``docopt`` as the **doc** argument. Moving the on!!!

docopt warnings/workarounds/known issues
----------------------------------------

.. attention::
    Do not ever start a line with a hyphen (minus sign) inside ``docopt_doc``, except when specifying options. ``docopt`` parses all lines starting with a hyphen as options without exceptions.

.. attention::
    When an option is specified more than once inside the *Usage* section of ``docopt_doc``, it might generate duplicated items.

    .. code:: python

        # Workaround `docopt issue <https://github.com/docopt/docopt/issues/134>`__:
        # Not perfect, but good enough for some of my particular usage cases.
        deduplicated_options = list(set(args["--option"]))

.. tip::
    Fixed arguments order.

    .. code:: python

        order_reference = [
            "First",
            "Second",
            "Third",
            "Fourth"
        ]
        # Sort the arguments so one doesn't have to worry about the order in which they are passed.
        # Source: https://stackoverflow.com/a/12814719.
        unordered_arguments = args["<arguments>"]
        # ["Fourth", "First", "Third", "Second"]
        unordered_arguments.sort(key=lambda x: order_reference.index(x))
        # ["First", "Second", "Third", "Fourth"]

        # Notes:
        # - unordered_arguments can have missing items.
        # - unordered_arguments cannot have items that aren't present in order_reference.




.. _application-generation-reference:

New application generation
==========================

A new *skeleton* application can be created to facilitate the addition of new applications.

- Command: ``app.py gen_base_app``

.. _docs-generation-reference:

Documentation generation
========================

This documentation is a "unified" documentation for all Python applications. The build documentation process needs Sphinx 1.6.5+ to be installed on the system.

- Command: ``app.py gen_docs``


Documentation basic guidelines
------------------------------

To avoid headaches, follow these basic guidelines.

ReStructuredText section headers
--------------------------------

- **\#**: With overline, for parts.
- **\***: With overline, for chapters.
- **\=**: For sections.
- **\-**: For subsections.
- **\^**: For subsubsections.
- **\"**: For paragraphs.

.. _sys-exec-generation-reference:

System executable generation
============================

To avoid being forced to execute all applications from their root folders, a system executable for each application can be generated and "installed". These system executables will be "installed" into ``~/.local/bin``. Additionally, bash completions for these system executables can be created. The function responsible for the creation of these files will also offer to add a mechanism to auto-load these bash completions in case the system isn't configured to do so.

- Command (For main application only): ``app.py gen_sys_exec_self``
- Command (For all applications): ``app.py gen_sys_exec_all``

.. note::

    I was forced to change from using Bash scripts as executables to Python scripts. Somehow, the arguments passed from a Bash script to a Python application were screwed up. Mainly, docopt parsed the arguments wrongly. Using the ``os.execv()`` function from a Python script works wonderfully and without any negative side effects (yet).

.. _installing-dependencies-reference:

Installing dependencies
=======================

All applications use one or more third party Python modules. Some of these third party modules are directly included with the main python application (**AppData/python_modules** folder), but some others need to be installed on the system.

- Command: ``app.py install_deps``

.. note::

    The third party modules that are directly included in the main application are modules that doesn't have dependencies (they only use modules from the Python standard library). The third party modules that need to be installed in the system are modules with one or more dependencies.

