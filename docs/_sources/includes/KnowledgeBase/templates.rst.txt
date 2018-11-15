
File templates
==============

These templates are files used to perform several tasks within the Knowledge Base application.

**archives.py** template
------------------------

In this file is stored all the data to handle on-line archives. Its location should always be **/UserData/KnowledgeBase/UserData/data_sources/archives.py**.

.. contextual-admonition::
    :context: info
    :title: Highlights

    - Compressed/Tared archives are downloaded into a temporary location (**UserData/data_storage/downloaded_archives**) and then their content extracted into their final location (**UserData/www/html_pages_from_archives/<kb_title>**).
    - Non-compressed/Non-tared files are directly downloaded into their final destination.

.. literalinclude:: ../../../../UserData/KnowledgeBase/AppData/data/templates/archives.py
    :language: python

Data keys
^^^^^^^^^

- ``kb_title`` (Madatory): The title that will be displayed in the web page index.
- ``kb_category`` (Madatory): A category name to organize the web page index.
- ``arch_url`` (Madatory): The url from which to download an archive.
- ``kb_rel_path`` (**Optional**): The path (relative to **UserData/www/html_pages_from_archives/<kb_title>**) to the a folder containing an HTML file (``kb_filename``) found inside the extracted content of an archive. **Default**: empty.
- ``kb_filename`` (**Optional**): The file name found inside the extracted content of an archive relative to ``kb_rel_path``. **Default**: **index.html**.
- ``kb_file_append`` (**Optional**): A list of tuples. Each tuple must contain a path to a file (relative to **UserData/www/html_pages_from_archives/<title key>**) at index 0 (zero) and a string at index 1 (one). The string will be appended at the end of the file defined at index zero.
- ``download_frequency`` (**Optional**): The frequency at which an archive should be downloaded. Default: **m**. Possible values:

    + ``w``: Weekly.
    + ``m``: Monthly.
    + ``s``: Semestrial.

- ``unzip_prog`` (**Optional**): The command to use to decompress archives. Possible values are **7z**, **unzip** and **tar**. The tar command can accept a decompression argument (See ``untar_arg``).
- ``untar_arg`` (**Optional**): The decompress argument used by the ``tar`` program. Possible values are **--xz**, **-J**, **--gzip**, **-z**, **--bzip2** or **-j**. **Default**: empty (no decompression argument is passed to ``tar``).

**repositories.py** template
----------------------------

In this file is stored all the data to handle on-line repositories. Its location should always be **/UserData/KnowledgeBase/UserData/data_sources/repositories.py**.

.. contextual-admonition::
    :context: info
    :title: Highlights

    - **sphinx>=1.6.5**: ``sudo pip3 install sphinx``

.. literalinclude:: ../../../../UserData/KnowledgeBase/AppData/data/templates/repositories.py
    :language: python

Data keys
^^^^^^^^^

- ``repo_owner`` (**Mandatory**): Repository owner/organization.
- ``repo_name`` (**Mandatory**): Repository name.
- ``repo_service`` (**Optional**): **Default**: **github**.
- ``repo_handler`` (**Mandatory**): Repository handler. Possible values:

    + ``sphinx_docs``: Repositories that contain Sphinx documentation sources. These sources are then used to build the HTML documentation.
    + ``single_file``: Repositories from which one file is used.
    + ``multi_files``: Repositories from which more than file is used.

- ``repo_type`` (**Optional**): Repository type (**git** or **hg**). **Default**: **git**.
- ``repo_filename`` (**Optional**): **Default**: **index.html** for **repo_handler** ``sphinx_docs`` and **README.md** for **repo_handler** ``single_file``.
- ``repo_files_ignore`` (**Optional|List**):
- ``repo_file_pattern`` (**Optional**):
- ``kb_category`` (**Optional**): **Default**: **Uncategorized**.
- ``kb_title`` (**Optional**):
- ``kb_title_prefix`` (**Optional**):
- ``kb_rel_path`` (**Optional**): Relative path to the desired file/folder/Sphinx docs sources.

    + ``sphinx_docs``: The path should be relative to a downloaded repository and point to a Sphinx docs source folder (e.g. if the docs sources of a downloaded repository are at **UserData/tmp/<repo_service>_repositories/<repo_owner>-<repo_name>/doc**, then the ``kb_rel_path`` key value should be **doc**).
    + ``single_file``: Repositories that 
    + ``multi_files``:

- ``kb_file_append`` (**Optional|List**):

.. note::

    Both previously mentioned files should contain one property called **data**. A list containing dictionaries.

**categories.json** template
----------------------------
