#!/usr/bin/python3

import os

# The root_folder is three (3) levels up from were the argos script is located.
root_folder = os.path.realpath(os.path.abspath(os.path.join(
    os.path.normpath(os.path.join(os.getcwd(), *([".."] * 3))))))

print("""---
Bump all apps versions | iconName=add \
bash="(cd {root_folder} && {root_folder}/app.py bump_app_version)" terminal=true

Generate documentation | iconName=devhelp \
bash="(cd {root_folder} && {root_folder}/app.py gen_docs)" terminal=true

Generate documentation (no API) | iconName=devhelp \
bash="(cd {root_folder} && {root_folder}/app.py gen_docs_no_api)" terminal=true

Generate base app | iconName=system-run \
bash="(cd {root_folder} && {root_folder}/app.py gen_base_app)" terminal=true

Generate self executable | iconName=application-x-executable \
bash="(cd {root_folder} && {root_folder}/app.py gen_sys_exec_self)" terminal=true

Generate executables for all apps | iconName=application-x-executable \
bash="(cd {root_folder} && {root_folder}/app.py gen_sys_exec_all)" terminal=true

Install dependencies | iconName=system-installer \
bash="(cd {root_folder} && {root_folder}/app.py install_deps)" terminal=true

Open local documentation webpage | iconName=html \
bash="(cd {root_folder} && xdg-open {root_folder}/docs/index.html)"

---

Search all apps AppData folder | iconName=search bash="(spacefm --find-files \
{root_folder}/AppData \
{root_folder}/UserData/BackupTool/AppData \
{root_folder}/UserData/ChrootHelper/AppData \
{root_folder}/UserData/FilesCleaner/AppData \
{root_folder}/UserData/HostsManager/AppData \
{root_folder}/UserData/KnowledgeBase/AppData \
{root_folder}/UserData/MakeCinnamonXletPOT/AppData \
{root_folder}/UserData/MoviesDB/AppData \
{root_folder}/UserData/PackageManager/AppData)"


""".format(root_folder=root_folder))
