#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Main command line application.

Attributes
----------
docopt_doc : str
    Used to store/define the docstring that will be passed to docopt as the "doc" argument.
root_folder : str
    The main folder containing the application. All commands must be executed from this location
    without exceptions.
"""

import os
import sys

from . import app_utils
from .__init__ import __appname__, __version__, __status__
from .python_utils import exceptions, shell_utils, file_utils, log_system
from .python_utils.docopt import docopt


if sys.version_info < (3, 5):
    raise exceptions.WrongPythonVersion()


root_folder = os.path.realpath(os.path.abspath(os.path.join(
    os.path.normpath(os.path.join(os.path.dirname(__file__), *([".."] * 2))))))


docopt_doc = """{__appname__} {__version__} {__status__}

Usage:
    app.py gen_base_app
    app.py gen_sys_exec_self
    app.py gen_sys_exec_all
    app.py bump_app_version [-a <name>... | --app=<name>...]
    app.py install_deps [-a <name>... | --app=<name>...]
    app.py repo (submodules | subtrees) (init | update)
    app.py (gen_docs | gen_docs_no_api)
           [-f | --force-clean-build]
           [-u | --update-inventories]
    app.py (-h | --help | --version)

Options:

-h, --help
    Show this screen.

--version
    Show application version.

-a, --app=<name>
    Specify one or more application name to work with. If this option isn't
    specified on the commands that make use of it, the command will work with
    all available applications.

-f, --force-clean-build
    Clear doctree cache and destination folder when building the documentation.

-u, --update-inventories
    Update inventory files from their on-line resources when building the
    documentation. Inventory files will be updated automatically if they don't
    already exist.

Command `bump_app_version`:
    Bump the specified application version.

Command `gen_base_app`:
    Generate a new base ("empty") application from template.

Command `gen_docs`:
    Generate documentation page.

Command `gen_docs_no_api`:
    Generate documentation page without extracting Python modules docstrings.

Command `gen_sys_exec_self`:
    Create an executable for this application on the system PATH to be able
    to run it from anywhere.

Command `gen_sys_exec_all`:
    Create an executable for all applications on the system PATH to be able
    to run them from anywhere.

Command `install_deps`:
    Install the dependencies for all Python applications.

Sub-commands for the `repo` command:
    submodules           Manage repository's sub-modules.
    subtrees             Manage repository's sub-trees.

""".format(__appname__=__appname__,
           __version__=__version__,
           __status__=__status__)


class CommandLineTool():
    """Command line tool.

    It handles the arguments parsed by the docopt module.

    Attributes
    ----------
    action : method
        Set the method that will be executed when calling CommandLineTool.run().
    app_slugs : list
        List of applications.
    update_inventories : bool
        See :any:`sphinx_docs_utils.generate_docs`.
    force_clean_build : bool
        See :any:`sphinx_docs_utils.generate_docs`.
    generate_api_docs : bool
        See :any:`sphinx_docs_utils.generate_docs`.
    logger : object
        See <class :any:`LogSystem`>.
    """

    def __init__(self, args):
        """
        Parameters
        ----------
        args : dict
            The dictionary of arguments as returned by docopt parser.
        """
        super(CommandLineTool, self).__init__()

        self.action = None
        self.force_clean_build = args["--force-clean-build"]
        self.update_inventories = args["--update-inventories"]
        self.generate_api_docs = args["gen_docs"]

        self.app_slugs = list(set(args["--app"]))
        file_utils.remove_surplus_files("AppData/logs", "CLI*")
        self.logger = log_system.LogSystem(filename=log_system.get_log_file(
            storage_dir="AppData/logs", prefix="CLI"), verbose=True)

        self.logger.info(shell_utils.get_cli_header(__appname__), date=False)
        print("")

        if args["bump_app_version"]:
            self.logger.info("Bumping applications' versions...")
            self.action = self.bump_versions

        if args["gen_base_app"]:
            self.logger.info("New application generation...")
            self.action = self.generate_base_app

        if args["gen_docs"] or args["gen_docs_no_api"]:
            self.logger.info("Documentation generation...")
            self.action = self.generate_docs

        if args["gen_sys_exec_all"]:
            self.logger.info("System executable generation for all applications...")
            self.action = self.system_executable_generation_all

        if args["gen_sys_exec_self"]:
            self.logger.info("System executable generation...")
            self.action = self.system_executable_generation_self

        if args["install_deps"]:
            self.logger.info("Installing dependencies...")
            self.action = self.install_dependencies

        if args["repo"]:
            self.repo_action = "init" if args["init"] else "update" if args["update"] else ""

            if args["submodules"]:
                self.logger.info("Managing repository sub-modules...")
                self.action = self.manage_repo_submodules

            if args["subtrees"]:
                self.logger.info("Managing repository sub-trees...")
                self.action = self.manage_repo_subtrees

    def run(self):
        """Execute the assigned action stored in self.action if any.
        """
        if self.action is not None:
            self.action()
            sys.exit(0)

    def bump_versions(self):
        """See :any:`app_utils.bump_versions`
        """
        app_utils.bump_versions(self.app_slugs, logger=self.logger)

    def generate_base_app(self):
        """See :any:`app_utils.BaseAppGenerator`
        """
        base_app_generetor = app_utils.BaseAppGenerator(logger=self.logger)
        base_app_generetor.generate()

    def generate_docs(self):
        """See :any:`sphinx_docs_utils.generate_docs`
        """
        app_utils.generate_docs(generate_api_docs=self.generate_api_docs,
                                update_inventories=self.update_inventories,
                                force_clean_build=self.force_clean_build,
                                logger=self.logger)

    def install_dependencies(self):
        """See :any:`app_utils.install_dependencies`
        """
        app_utils.install_dependencies(app_slugs=self.app_slugs, logger=self.logger)

    def system_executable_generation_self(self):
        """See :any:`template_utils.system_executable_generation`
        """
        from .python_utils import template_utils

        template_utils.system_executable_generation(
            exec_name="app-manager-cli",
            app_root_folder=root_folder,
            sys_exec_template_path=os.path.join(
                root_folder, "AppData", "data", "templates", "system_executable"),
            bash_completions_template_path=os.path.join(
                root_folder, "AppData", "data", "templates", "bash_completions.bash"),
            logger=self.logger
        )

    def system_executable_generation_all(self):
        """See :any:`app_utils.system_executable_generation_for_all_apps`
        """
        app_utils.system_executable_generation_for_all_apps(logger=self.logger)

    def manage_repo_submodules(self):
        """See :any:`git_utils.manage_repo`
        """
        from .python_utils import git_utils

        git_utils.manage_repo(
            "submodule",
            self.repo_action,
            cwd=root_folder,
            logger=self.logger
        )

    def manage_repo_subtrees(self):
        """See :any:`git_utils.manage_repo`
        """
        self.logger.warning("Not using sub-trees in this application for now.")


def main():
    """Initialize main command line interface.

    Raises
    ------
    exceptions.BadExecutionLocation
        Do not allow to run any command if the "flag" file isn't
        found where it should be. See :any:`exceptions.BadExecutionLocation`.
    """
    if not os.path.exists(".cli-applications-manager.flag"):
        raise exceptions.BadExecutionLocation()

    arguments = docopt(docopt_doc, version="%s %s %s" % (__appname__, __version__, __status__))
    cli = CommandLineTool(arguments)
    cli.run()


if __name__ == "__main__":
    pass
