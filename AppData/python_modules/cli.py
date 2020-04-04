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
from .__init__ import __appdescription__
from .__init__ import __appname__
from .__init__ import __status__
from .__init__ import __version__
from .python_utils import cli_utils

root_folder = os.path.realpath(os.path.abspath(os.path.join(
    os.path.normpath(os.path.join(os.path.dirname(__file__), *([os.pardir] * 2))))))

docopt_doc = """{appname} {version} ({status})

{appdescription}

Usage:
    app.py (-h | --help | --manual | --version)
    app.py app_repos (submodules | subtrees) (init | update)
                     [-a <name>... | --app=<name>...]
                     [--dry-run]
    app.py bump_app_version [-a <name>... | --app=<name>...]
    app.py gen_base_app
    app.py (gen_docs | gen_docs_no_api) [-f | --force-clean-build]
                                        [-u | --update-inventories]
    app.py gen_man_pages [-a <name>... | --app=<name>...]
    app.py gen_readmes
    app.py gen_sys_exec_all
    app.py gen_sys_exec_self
    app.py install_deps [-a <name>... | --app=<name>...]
    app.py print_all_apps
    app.py repo (submodules | subtrees) (init | update) [--dry-run]
    app.py run_cmd_on_app (-c <command> | --command=<command>)
                          [-p | --parallel ]
                          [-a <name>... | --app=<name>...]
    app.py spacefm_find_files

Options:

-h, --help
    Show this application basic help.

--manual
    Show this application manual page.

--version
    Show application version.

-a, --app=<name>
    Specify one or more application name to work with. If this option isn't
    specified on the commands that make use of it, the command will work with
    all available applications.

-c <command>, --command=<command>
    Command to execute inside a managed application folder.

--dry-run
    Do not perform file system changes. Only display messages informing of the
    actions that will be performed or commands that will be executed.

-f, --force-clean-build
    Clear doctree cache and destination folder when building the documentation.

-p, --parallel
    Run command in parallel instead of after finishing each command execution.

-u, --update-inventories
    Update inventory files from their on-line resources when building the
    documentation. Inventory files will be updated automatically if they don't
    already exist.

""".format(appname=__appname__,
           appdescription=__appdescription__,
           version=__version__,
           status=__status__)


class CommandLineInterface(cli_utils.CommandLineInterfaceSuper):
    """Command line interface.

    It handles the arguments parsed by the docopt module.

    Attributes
    ----------
    a : dict
        Where docopt_args is stored.
    action : method
        Set the method that will be executed when calling CommandLineInterface.run().
    repo_action : str
        Which action to perform on a repository.
    """
    action = None
    repo_action = None
    app_slugs = []

    def __init__(self, docopt_args):
        """Initialize.

        Parameters
        ----------
        docopt_args : dict
            The dictionary of arguments as returned by docopt parser.
        """
        self.a = docopt_args
        self._cli_header_blacklist = [
            self.a["spacefm_find_files"],
            self.a["--manual"],
            self.a["print_all_apps"]
        ]

        super().__init__(__appname__, "UserData/0_manager/logs")

        self.app_slugs = list(set(self.a["--app"]))

        if self.a["spacefm_find_files"]:
            self.action = self.spacefm_find_files
        elif self.a["print_all_apps"]:
            self.action = self.print_all_apps
        elif self.a["--manual"]:
            self.action = self.display_manual_page
        elif self.a["bump_app_version"]:
            self.logger.info("**Bumping applications' versions...**")
            self.action = self.bump_versions
        elif self.a["gen_base_app"]:
            self.logger.info("**New application generation...**")
            self.action = self.generate_base_app
        elif self.a["gen_docs"] or self.a["gen_docs_no_api"]:
            self.logger.info("**Documentation generation...**")
            self.action = self.generate_docs
        elif self.a["gen_man_pages"]:
            self.logger.info("**Generating manual pages...**")
            self.action = self.generate_man_pages
        elif self.a["gen_readmes"]:
            self.logger.info("**Generating READMEs...**")
            self.action = self.generate_readmes
        elif self.a["gen_sys_exec_all"]:
            self.logger.info("**System executable generation for all applications...**")
            self.action = self.system_executable_generation_all
        elif self.a["gen_sys_exec_self"]:
            self.logger.info("**System executable generation...**")
            self.action = self.system_executable_generation_self
        elif self.a["install_deps"]:
            self.logger.info("**Installing dependencies...**")
            self.action = self.install_dependencies
        elif self.a["run_cmd_on_app"]:
            self.logger.info("**Running command on selected applications...**")
            self.action = self.run_cmd_on_apps
        elif self.a["repo"] or self.a["app_repos"]:
            self.repo_action = "init" if self.a["init"] else "update" if self.a["update"] else ""

            if self.a["submodules"]:
                if self.a["app_repos"]:
                    self.logger.info("**Managing application repositories sub-modules...**")
                    self.action = self.manage_app_repos_submodules
                elif self.a["repo"]:
                    self.logger.info("**Managing repository sub-modules...**")
                    self.action = self.manage_repo_submodules
            elif self.a["subtrees"]:
                if self.a["app_repos"]:
                    self.logger.info("**Managing application repositories sub-trees...**")
                    self.action = self.manage_app_repos_subtrees
                elif self.a["repo"]:
                    self.logger.info("**Managing repository sub-trees...**")
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
        app_utils.generate_docs(generate_api_docs=self.a["gen_docs"],
                                update_inventories=self.a["--update-inventories"],
                                force_clean_build=self.a["--force-clean-build"],
                                logger=self.logger)

    def install_dependencies(self):
        """See :any:`app_utils.install_dependencies`
        """
        app_utils.install_dependencies(app_slugs=self.app_slugs,
                                       logger=self.logger)

    def generate_readmes(self):
        """See :any:`app_utils.generate_readmes`
        """
        app_utils.generate_readmes(self.logger)

    def run_cmd_on_apps(self):
        """See :any:`app_utils.run_cmd_on_apps`
        """
        app_utils.run_cmd_on_apps(self.a["--command"],
                                  run_in_parallel=self.a["--parallel"],
                                  app_slugs=self.app_slugs,
                                  logger=self.logger)

    def system_executable_generation_self(self):
        """See :any:`cli_utils.CommandLineInterfaceSuper._system_executable_generation`.
        """
        self._system_executable_generation(
            exec_name="apps-manager-cli",
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
            dry_run=self.a["--dry-run"],
            logger=self.logger
        )

    def manage_repo_subtrees(self):
        """See :any:`git_utils.manage_repo`
        """
        self.logger.warning("**Not using sub-trees in this application for now.**")

    def manage_app_repos_submodules(self):
        """See :any:`git_utils.manage_repo`
        """
        self.logger.warning("**Not using sub-modules in applications for now.**")

    def manage_app_repos_subtrees(self):
        """See :any:`git_utils.manage_repo`
        """
        app_utils.manage_app_repos_subtrees(self.repo_action,
                                            app_slugs=self.app_slugs,
                                            dry_run=self.a["--dry-run"],
                                            logger=self.logger)

    def display_manual_page(self):
        """See :any:`cli_utils.CommandLineInterfaceSuper._display_manual_page`.
        """
        self._display_manual_page(os.path.join(root_folder, "AppData", "data", "man", "app.py.1"))

    def generate_man_pages(self):
        """See :any:`app_utils.generate_man_pages`
        """
        app_utils.generate_man_pages(app_slugs=self.app_slugs,
                                     logger=self.logger)

    def print_all_apps(self):
        """See :any:`app_utils.print_all_apps`
        """
        app_utils.print_all_apps()

    def spacefm_find_files(self):
        """See :any:`app_utils.spacefm_find_files`
        """
        app_utils.spacefm_find_files()


def main():
    """Initialize command line interface.
    """
    cli_utils.run_cli(flag_file=".cli-applications-manager.flag",
                      docopt_doc=docopt_doc,
                      app_name=__appname__,
                      app_version=__version__,
                      app_status=__status__,
                      cli_class=CommandLineInterface)


if __name__ == "__main__":
    pass
