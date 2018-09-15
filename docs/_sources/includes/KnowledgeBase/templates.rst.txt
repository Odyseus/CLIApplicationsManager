
File templates
==============

These templates are files used to perform several tasks within the Knowledge Base application.

**argos_helper_script.py** script
---------------------------------

Script to be used with Argos for Cinnamon extension.

.. literalinclude:: ../../../../UserData/KnowledgeBase/AppData/data/templates/argos_helper_script.py
    :language: python

**app_launcher.sh** script
--------------------------

This script is used to launch applications *in bulk* through the ``kbapp.py`` :abbr:`CLI (Command Line Interface)`. It's mostly useful if used to launch *self contained* applications that are stored inside **Data/apps** and if at the same time the Argos for Cinnamon extension is used.

.. literalinclude:: ../../../../UserData/KnowledgeBase/AppData/data/templates/app_launcher.sh
    :language: bash

**bitbucket.py** and **github.py** scripts
------------------------------------------

.. literalinclude:: ../../../../UserData/KnowledgeBase/AppData/data/templates/repository.py
    :language: python
