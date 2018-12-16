#!/bin/bash

# It would have been impossible to create this without the following post on Stack Exchange!!!
# https://unix.stackexchange.com/a/55622

type "{executable_name}" &> /dev/null &&
_decide_nospace_{current_date}(){
    if [[ ${1} == "--"*"=" ]] ; then
        type "compopt" &> /dev/null && compopt -o nospace
    fi
} &&
_get_app_slugs_{current_date}(){
    echo $(cd {full_path_to_app_folder}; ./app.py print_all_apps)
} &&
_apps_manager_cli_{current_date}(){
    local cur prev cmd app_names apps_dir
    COMPREPLY=()
    cur="${COMP_WORDS[COMP_CWORD]}"
    prev="${COMP_WORDS[COMP_CWORD-1]}"
    app_names=( $(_get_app_slugs_{current_date}) )

    case $prev in
        --app)
            COMPREPLY=( $( compgen -W "${app_names[*]}") )
            return 0
            ;;
        -a)
            COMPREPLY=( $( compgen -W "${app_names[*]}" -- ${cur}) )
            return 0
            ;;
    esac

    # Handle --xxxxx=path
    if [[ ${prev} == "=" ]] ; then
        if [[ ${cur} != *"/"* ]]; then
            COMPREPLY=( $( compgen -W "${app_names[*]}" -- ${cur}) )
            return 0
        fi

        return 0
    fi

    # Completion of commands and "first level options.
    if [[ $COMP_CWORD == 1 ]]; then
        COMPREPLY=( $(compgen -W "
bump_app_version \
gen_base_app \
gen_docs \
gen_docs_no_api \
gen_man_pages \
gen_readmes \
gen_sys_exec_all \
gen_sys_exec_self \
git_gui_apps \
install_deps \
repo app_repos \
run_cmd_on_app \
-h --help --manual --version" -- "${cur}") )
        return 0
    fi

    # Completion of options and sub-commands.
    cmd="${COMP_WORDS[1]}"

    case $cmd in
    "gen_docs"|"gen_docs_no_api")
        COMPREPLY=( $(compgen -W \
            "-f --force-clean-build -u --update-inventories" -- "${cur}") )
        ;;
    "install_deps"|"bump_app_version"|"gen_man_pages")
        COMPREPLY=( $(compgen -W "-a --app=" -- "${cur}") )
        _decide_nospace_{current_date} ${COMPREPLY[0]}
        ;;
    "repo"|"app_repos")
        COMPREPLY=( $(compgen -W \
            "submodules subtrees" -- "${cur}") )
        ;;
    "run_cmd_on_app")
        COMPREPLY=( $(compgen -W \
            "-c --command= -a --app= -p --parallel" -- "${cur}") )
        _decide_nospace_{current_date} ${COMPREPLY[0]}
        ;;
    esac


    # Completion of options and sub-commands.
    cmd="${COMP_WORDS[2]}"

    case $cmd in
    "submodules"|"subtrees")
        COMPREPLY=( $(compgen -W \
            "init update" -- "${cur}") )
        ;;
    esac

    # Completion of options and sub-commands.
    cmd="${COMP_WORDS[3]}"

    case $cmd in
    "init"|"update")
        COMPREPLY=( $(compgen -W "--dry-run -a --app=" -- "${cur}") )
        _decide_nospace_{current_date} ${COMPREPLY[0]}
        ;;
    esac

    return 0
} &&
complete -F _apps_manager_cli_{current_date} {executable_name}
