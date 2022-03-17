
*************************
General development notes
*************************

- :ref:`docopt-usage-notes-reference`
- :ref:`application-generation-reference`
- :ref:`docs-generation-reference`
- :ref:`sys-exec-generation-reference`
- :ref:`installing-dependencies-reference`
- :ref:`web-apps-reference`

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

Troubleshooting
---------------

The following error might arise when building documentations.

.. code::

    Configuration error:
    The configuration file (or one of the modules it imports) called sys.exit()

Using my f\*cking magic ball I devined that the ``eval_config_file`` method (found in ``sphinx.config`` module) eats the exception to display the useless message. Except for :py:class:`SystemExit`, all other exceptions raised there will display an actually usefull message.

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

    The third party modules that are directly included in the main application are modules that doesn't have dependencies (they only use modules from the Python standard library). The third party modules that need to be installed in the environment are modules with one or more dependencies.


.. _web-apps-reference:

|HTML| pages (|a.k.a.| web apps)
================================

Bootstrap framework
-------------------

- Tooltips: I like Bootstrap tooltips because they are semi-permanent; and I hate them for the exact same reason.

    + Pros

        * When the mouse cursor is moved over an element with a Bootstrap tooltip, the tooltip will stay visible, while a native tooltip will appear and immediately disappear.
        * Their visibility triggers on ``hover`` and ``focus`` by default.

    + Cons

        * One being accustomed for tooltips to behave somewhat in a *fleeting way*, Bootstrap tooltips feel kind of invasive. This falls into the category *better to have it and not need it than to need it and not have it* because otherwise tooltips are useless when not using a mouse.

Cautionary tales
----------------

- *Interesting* fact. If the Firefox setting called ``browser.zoom.full`` is set to ``false`` the zooming of the page will not trigger breakpoint changes.
- Another *interesting* fact. With the Firefox preference ``privacy.resistFingerprinting`` set to true animations using ``window.requestAnimationFrame`` are jerky. Retarded, right!?!?!?!
- And the *interesting* things won't stop. Having the preference ``network.http.referer.XOriginPolicy`` set to 1 in Waterfox Classic renders the ``fetch`` API useless in all my *web apps.*.
- When the Firefox developer tools is open, a search input doesn't focus on page load. It took me hours to discover this stupid behavior!!! (&%$$)
- Input search nightmare!! I wanted something simple. To store search terms when pressing :kbd:`Enter` without the input search being cleared and without submitting the form. Simple, right?!? Nothing is ever so with shite *designed* by f\*cking web developers!!! The way that I made it work is as follows:

    + Added ``action="javascript:void(0)"`` attribute to the form.
    + Added ``name="input-id"`` attribute to the input of type search.
    + On the ``keypress`` event for the input I prevent default and return false when pressing the :kbd:`Enter` key. In the middle of these calls I call the form's ``submit`` method.
    + Why all of this works (in Firefox based browsers only, because in Shitemium based browsers nothing f\*cking works!!!), and which part of these changes actually made it work, I have no idea. Like with everything derived from *web technologies*, I will keep *enjoying* it while it last. It's pointless to expect any kind of stability or congruency from any of these *technologies*.

- Reasons (other than them being shite) for autocomplete not working on Shitemium based browsers:

    + The input isn't the first child of the form. Typical Google shite, to tell everybody how things should be designed!!!
    + Autocomplete is disabled when not using SSL in Shitemium based browsers. Typical web developers shite mentality, EVERYTHING in the f\*cking cloud! Local HTML files can't be viewed in a f\*cking HTML viewer!!! And SSL forced on locally hosted sites without internet access that DO NOT handle ANY data that needs to be securely handled!!!
    + Lastly, Google's design decision that the current behavior is the desired behavior by ALL Chrome users. This is the most likely problem. 90% of Chrome's users are morons that installed the browser without even knowing while blindly clicking Next in a wizard that they didn't even knew WTF they were installing, like every single f\*cking Windows user!!!

- Having the web developers tools open will make a `DataTables <http://www.datatables.net/>`__ table render very slowly in Firefox based browsers.
- ``document.querySelector`` and ``document.querySelectorAll`` are quite **SLOW**, thus try to use ``document.getElementById``, ``document.getElementsByClassName`` or ``document.getElementsByTagName`` for a performance bonus.
