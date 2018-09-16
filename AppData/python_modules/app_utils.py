#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Module with utility functions and classes.

Attributes
----------
root_folder : str
    The main folder containing the application. All commands must be executed from this location
    without exceptions.
"""

import os

from subprocess import check_call, CalledProcessError

from .python_utils import string_utils, prompts, exceptions, file_utils, misc_utils
from .python_utils.ansi_colors import Ansi


root_folder = os.path.realpath(os.path.abspath(os.path.join(
    os.path.normpath(os.path.join(os.path.dirname(__file__), *([".."] * 2))))))


class InvalidApplicationName(exceptions.ExceptionWhitoutTraceBack):
    """InvalidApplicationName
    """

    def __init__(self, msg="Use the name of an existent application!!!"):
        """Initialize.

        Parameters
        ----------
        msg : str, optional
            Message that the exception should display.
        """
        super(InvalidApplicationName, self).__init__(msg=msg)


def get_apps():
    """Get application directories.

    Returns
    -------
    list
        The application directory names or paths.
    """
    root_app_user_data = os.path.join(root_folder, "UserData")
    list_of_app_dirs = os.listdir(root_app_user_data)
    apps = []

    for dir_name in list_of_app_dirs:
        app_data_dir = os.path.join(root_app_user_data, dir_name, "AppData")

        # Check for the AppData dir in case in the future there are other directories
        # that aren't actual applications.
        if os.path.exists(app_data_dir):
            apps.append({
                "slug": dir_name,
                "path": os.path.dirname(app_data_dir)
            })

    return apps


def system_executable_generation_for_all_apps(logger):
    """Create executables for all Python applications including the "master app".

    Parameters
    ----------
    logger : object
        See <class :any:`LogSystem`>.
    """
    from .python_utils import template_utils

    print(Ansi.WARNING("""
1. System executables will be created and bash completions will be installed \
for all Python applications, including the master application.
2. The executable names are pre-defined.
3. Any existent files will be overwritten without exceptions.
4. There will be no attempt to set up a Bash completions loading mechanism. \
It will have to be done manually.
5. There will be no prompts of any king, except to ask once for the location \
where the executables will be stored.
"""))

    if prompts.confirm(prompt="Proceed?", response=False):
        user_home = os.path.expanduser("~")

        d = {
            "sys_exec_path": os.path.join(user_home, ".local", "bin")
        }

        print(Ansi.PURPLE("Set path to store all generated executable files or press Enter to use default"))
        prompts.do_prompt(d, "sys_exec_path", "Enter path", d["sys_exec_path"])

        d["sys_exec_path"] = os.path.expanduser(d["sys_exec_path"])
        d["sys_exec_path"] = os.path.expandvars(d["sys_exec_path"])

        # Define arguments for "master app".
        apps_args = [{
            "exec_name": "apps-manager-cli",
            "app_root_folder": root_folder,
            "sys_exec_template_path": os.path.join(
                root_folder, "AppData", "data", "templates", "system_executable"),
            "bash_completions_template_path": os.path.join(
                root_folder, "AppData", "data", "templates", "bash_completions.bash")
        }]

        # Define arguments for the rest of apps.
        for app in get_apps():
            app_root_folder = os.path.join(root_folder, "UserData", app["slug"])

            apps_args.append({
                "exec_name": "-".join([s.lower() for s in string_utils.split_on_uppercase(app["slug"])]) + "-cli",
                "app_root_folder": app_root_folder,
                "sys_exec_template_path": os.path.join(
                    app_root_folder, "AppData", "data", "templates", "system_executable"),
                "bash_completions_template_path": os.path.join(
                    app_root_folder, "AppData", "data", "templates", "bash_completions.bash")
            })

        # Extend with arguments common to all apps.
        for kwargs in apps_args:
            kwargs.update({
                "exec_destination": d["sys_exec_path"],
                "bash_comp_step_one_confirmed": True,
                "bash_comp_step_two": False,
                "confirm_overwrite": False,
                "logger": logger,
                "prompt_for_name": False,
                "prompt_for_path": False,
            })

            template_utils.system_executable_generation(**kwargs)


def install_dependencies(app_slugs, logger):
    """Install dependencies for all Python applications.

    Parameters
    ----------
    app_slugs : list
        List of applications. If empty, try to install dependencies for all applications.
    logger : object
        See <class :any:`LogSystem`>.

    Raises
    ------
    exceptions.KeyboardInterruption
        See <class :any:`exceptions.KeyboardInterruption`>.
    """
    print(Ansi.PURPLE("""
The command "pip3" will be used to install dependencies.
Installing dependencies requires administrative privileges.
You might need to enter your password.
"""))

    do_install = False
    all_apps = get_apps()
    cmd = ["/usr/bin/sudo", "--set-home", "pip3", "install"]

    for app in app_slugs if app_slugs else all_apps:
        if isinstance(app, dict):
            app_slug = app["slug"]
            app_path = app["path"]
        else:
            if app not in [a["slug"] for a in all_apps]:
                raise InvalidApplicationName(app)

            app_slug = app

            for a in all_apps:
                if a["path"].endswith(app):
                    app_path = a["path"]
                    break

        req_file_path = os.path.join(app_path, "requirements.txt")

        if file_utils.is_real_file(req_file_path):
            print()
            logger.warning("The following dependencies for %s will be installed." % app_slug)

            do_install = True
            cmd += ["--requirement", req_file_path]

            with open(req_file_path, "r+", encoding="UTF-8") as req_file:
                lines = [line.strip() for line in req_file.readlines()]

                for line in lines:
                    if line:
                        logger.info(line, date=False)
        else:
            print()
            logger.info("%s has no extra dependencies." % app_slug)

    print()
    logger.warning("The following command will be executed:")
    logger.info(" ".join(cmd), date=False)
    print()

    if do_install and prompts.confirm(prompt="Proceed?", response=False):
        try:
            check_call(cmd, cwd=root_folder)
        except (KeyboardInterrupt, SystemExit):
            raise exceptions.KeyboardInterruption()
        except CalledProcessError as err:
            logger.error(err)


def generate_docs(generate_api_docs=False,
                  update_inventories=False,
                  force_clean_build=False,
                  logger=None):
    """See :any:`sphinx_docs_utils.generate_docs`

    Parameters
    ----------
    generate_api_docs : bool, optional
        See :any:`sphinx_docs_utils.generate_docs`.
    update_inventories : bool, optional
        See :any:`sphinx_docs_utils.generate_docs`.
    force_clean_build : bool, optional
        See :any:`sphinx_docs_utils.generate_docs`.
    logger : None, optional
        See :any:`LogSystem`.
    """
    from .python_utils import sphinx_docs_utils

    ignored_apidoc_modules = [
        os.path.join("AppData", "python_modules", "python_utils", "bottle.py"),
        os.path.join("AppData", "python_modules", "python_utils", "docopt.py"),
        os.path.join("AppData", "python_modules", "python_utils", "mistune.py"),
        os.path.join("AppData", "python_modules", "python_utils", "polib.py"),
        os.path.join("AppData", "python_modules", "python_utils", "pyperclip"),
        os.path.join("AppData", "python_modules", "python_utils", "titlecase.py"),
        os.path.join("AppData", "python_modules", "python_utils", "tqdm"),
        # The following module has perfectly valid docstrings, but Sphinx is being a
        # b*tch and throws a million warnings for no reason.
        # Ignore it until Sphinx gets its sh*t together.
        os.path.join("AppData", "python_modules", "python_utils", "tqdm_wget.py"),
        # Ignore the python_utils folder from all apps.
    ] + [os.path.join("UserData", app["slug"], "AppData", app["slug"] + "App", "python_utils")
         for app in get_apps()]

    base_apidoc_dest_path_rel_to_root = os.path.join("AppData", "docs_sources", "modules")

    apidoc_paths_rel_to_root = [
        (os.path.join("AppData", "python_modules"),
            os.path.join(base_apidoc_dest_path_rel_to_root, "python_modules"))
    ] + [(os.path.join("UserData", app["slug"], "AppData", app["slug"] + "App"),
          os.path.join(base_apidoc_dest_path_rel_to_root, app["slug"]))
         for app in get_apps()]

    sphinx_docs_utils.generate_docs(root_folder=root_folder,
                                    docs_src_path_rel_to_root=os.path.join(
                                        "AppData", "docs_sources"),
                                    docs_dest_path_rel_to_root="docs",
                                    apidoc_paths_rel_to_root=apidoc_paths_rel_to_root,
                                    doctree_temp_location_rel_to_sys_temp="PythonCLIApps-doctrees",
                                    ignored_modules=ignored_apidoc_modules,
                                    generate_api_docs=generate_api_docs,
                                    update_inventories=update_inventories,
                                    force_clean_build=force_clean_build,
                                    logger=logger)


class BaseAppGenerator():
    """Base application generator.

    Attributes
    ----------
    app : dict
        The dictionary were the app name is stored.
    app_slug : str
        The application name without spaces.
    app_slug_lower_dashed : str
        The application name lower-cased and separated by dashes.
    app_slug_lower_lodashed : str
        The application name lower-cased and separated by low-dashes.
    base_app_path : str
        Path to the base application (the template).
    default_name : str
        Default name for the base application.
    logger : object
        See <class :any:`LogSystem`>.
    new_app_destination : str
        The path to the new generated application.
    replacement_data : list
        List of tuples containing (template, replacement) data.
    """

    def __init__(self, logger):
        """Initialize.

        Parameters
        ----------
        logger : object
            See <class :any:`LogSystem`>.
        """
        super(BaseAppGenerator, self).__init__()
        self.logger = logger
        self.default_name = "My Python Application"
        self.app = {
            "name": self.default_name
        }

    def generate(self):
        """Generate.
        """
        print(Ansi.PURPLE("""
1. The application name should contain two or more words.
2. All the words should be camel cased.
"""))

        prompts.do_prompt(
            self.app, "name", "Enter the desired name for the application", self.default_name)

        self._do_setup()
        self._do_copy()
        self._do_substitutions()

    def _do_setup(self):
        """Do setup.
        """
        self.app_slug = "".join(self.app["name"].split())
        self.app_slug_lower_dashed = "-".join(self.app["name"].split()).lower()
        self.app_slug_lower_lodashed = "_".join(self.app["name"].split()).lower()
        self.base_app_path = os.path.join(root_folder, "__app__", "data", "templates", "BaseApp")
        self.new_app_destination = os.path.join(root_folder, self.app_slug)
        self.replacement_data = [
            ("{{APP-NAME}}", self.app["name"]),
            ("{{APP-SLUG-LOWER-DASHED}}", self.app_slug_lower_dashed),
            ("{{APP-SLUG-LOWER-LODASHED}}", self.app_slug_lower_lodashed),
            ("{{APP-SLUG-CAMEL}}", self.app_slug)
        ]

    def _do_copy(self):
        """Do copy.

        Raises
        ------
        exceptions.ExistentLocation
            See <class :any:`exceptions.ExistentLocation`>.
        """
        if os.path.exists(self.new_app_destination):
            raise exceptions.ExistentLocation("New application cannot be created.")

        self.logger.info("Copying files...")
        file_utils.custom_copytree(self.base_app_path, self.new_app_destination)

    def _do_substitutions(self):
        """Do substitutions.
        """
        self.logger.info("Performing string substitutions...")
        for root, dirs, files in os.walk(self.new_app_destination, topdown=False):
            for fname in files:
                file_path = os.path.join(root, fname)

                with open(file_path, "r+", encoding="UTF-8") as file:
                    file_data = file.read()
                    file.seek(0)
                    file_data = self._do_replacements(file_data)
                    file.write(file_data)
                    file.truncate()

                fname_renamed = self._do_replacements(fname)

                if fname != fname_renamed:
                    os.rename(file_path, os.path.join(os.path.dirname(file_path), fname_renamed))

            for dname in dirs:
                dir_path = os.path.join(root, dname)

                dname_renamed = self._do_replacements(dname)

                if dname != dname_renamed:
                    os.rename(dir_path, os.path.join(os.path.dirname(dir_path), dname_renamed))

    def _do_replacements(self, data):
        """Do replacements.

        Parameters
        ----------
        data : str
            Data to modify.

        Returns
        -------
        str
            Modified data.
        """
        for template, replacement in self.replacement_data:
            if template in data:
                data = data.replace(template, replacement)

        return data


def bump_versions(app_slugs, logger):
    """Bump applications versions.

    Parameters
    ----------
    app_slugs : list
        List of applications. If empty, try to bump the version of all applications.
    logger : object
        See <class :any:`LogSystem`>.
    """
    print()

    for app in app_slugs if app_slugs else get_apps():
        bump_app_version(app["slug"] if isinstance(app, dict) else app, logger)


def bump_app_version(app_slug, logger):
    """Bump application version.

    Parameters
    ----------
    app_slug : str
        The application to which to bump its version.
    logger : object
        See <class :any:`LogSystem`>.

    Raises
    ------
    InvalidApplicationName
        See <class :any:`InvalidApplicationName`>.
    """
    if app_slug not in [app["slug"] for app in get_apps()]:
        raise InvalidApplicationName(app_slug)

    logger.info("Bumping %s's version..." % app_slug)
    version_number = misc_utils.micro_to_milli(misc_utils.get_date_time())
    init_file_path = os.path.join(root_folder, "UserData", app_slug, "AppData",
                                  "%sApp" % app_slug, "__init__.py")

    with open(init_file_path, "r", encoding="UTF-8") as old:
        old_lines = old.readlines()

    new_lines = "".join(['__version__ = "%s"' % version_number if l.startswith(
        "__version__") else l for l in old_lines])

    with open(init_file_path, "w", encoding="UTF-8") as new:
        new.write("%s\n" % new_lines)

    logger.info("%s's version updated." % app_slug)
    print()


apps_manager_readme_template = """
## {apps_man_name} ([documentation]({docs_url}))

{apps_man_description}

## List of CLI applications

[GitLab]: https://i.imgur.com/Z4XcUKe.png "GitLab"
[GitHub]: https://i.imgur.com/J015ugC.png "GitHub"
[BitBucket]: https://i.imgur.com/igK1F8b.png "BitBucket"

| App. name | Status | Description | Repositories | Docs |
| --------- | :----: | ----------- | :----------: | :--: |
"""

app_table_row_template = """| **{app_name}** | {app_status} | {app_description} | \
[![GitLab][GitLab]]({app_repo_url}) \
[![GitHub][GitHub]](https://github.com/Odyseus/{app_slug}) \
[![BitBucket][BitBucket]](https://bitbucket.org/Odyseus/{app_slug}) \
| [Docs]({app_docs_url}) |
"""

app_readme_template = """
## {app_name} ([documentation]({app_docs_url}))

{app_description}
"""


def generate_readmes(logger):
    from runpy import run_path

    from .__init__ import __appname__, __appdescription__

    docs_base_url = "https://pythoncliapplications.gitlab.io/CLIApplicationsManager"
    repo_base_url = "https://gitlab.com/PythonCLIApplications/{app_slug}"
    apps_manager_readme_path = os.path.join(root_folder, "README.md")
    apps_table_data = ""
    apps_manager_readme_data = apps_manager_readme_template.format(
        apps_man_name=__appname__,
        apps_man_description=__appdescription__,
        docs_url=docs_base_url
    )

    for app in sorted(get_apps(), key=lambda k: k["slug"]):
        app_docs_url = docs_base_url + "/includes/%s/index.html" % app["slug"]
        app_init_file_path = os.path.join(root_folder, "UserData", app["slug"], "AppData",
                                          "%sApp" % app["slug"], "__init__.py")
        app_readme_file_path = os.path.join(root_folder, "UserData", app["slug"], "README.md")
        init_data = run_path(app_init_file_path)
        apps_table_data += app_table_row_template.format(
            app_slug=app["slug"],
            app_name=init_data["__appname__"],
            app_status=init_data["__status__"][1:-1],
            app_description=init_data["__appdescription__"],
            app_repo_url=repo_base_url.format(app_slug=app["slug"]),
            app_docs_url=app_docs_url
        )

        logger.info("Generating README for %s" % init_data["__appname__"])
        with open(app_readme_file_path, "w", encoding="UTF-8") as app_readme_file:
            app_readme_file.write(app_readme_template.format(
                app_name=init_data["__appname__"],
                app_description=init_data["__appdescription__"],
                app_docs_url=app_docs_url
            ))

    logger.info("Generating README for %s" % __appname__)
    with open(apps_manager_readme_path, "w", encoding="UTF-8") as main_readme_file:
        main_readme_file.write(apps_manager_readme_data + apps_table_data)

    logger.info("READMEs generation finished")


if __name__ == "__main__":
    pass
