#!/bin/bash

# It would have been impossible to create this without the following post on Stack Exchange!!!
# https://unix.stackexchange.com/a/55622

_have {executable_name} &&
_decide_nospace(){
    if [[ ${1} == "--"*"=" ]] ; then
        compopt -o nospace
    fi
} &&
_list_dirs(){
    # <3 https://stackoverflow.com/a/31603260
    # List all directories found inside the passed folder ($1).
    # WARNING! Fails on empty directories!
    (
        cd "${1}" && \
        set -- */; printf "%s\n" "${@%/}";
    )
} &&
_my_python_apps_{current_date}(){
    local cur prev cmd app_names apps_dir
    COMPREPLY=()
    cur="${COMP_WORDS[COMP_CWORD]}"
    prev="${COMP_WORDS[COMP_CWORD-1]}"
    apps_dir="{full_path_to_app_folder}/UserData"
    app_names=( $(_list_dirs ${apps_dir}) )

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
        COMPREPLY=( $(compgen -W "bump_app_version gen_base_app gen_docs gen_docs_no_api \
gen_sys_exec_self gen_sys_exec_all gen_readmes install_deps repo \
-h --help --version" -- "${cur}") )
        return 0
    fi

    # Completion of options and sub-commands.
    cmd="${COMP_WORDS[1]}"

    case $cmd in
    "gen_docs"|"gen_docs_no_api")
        COMPREPLY=( $(compgen -W \
            "-f --force-clean-build -u --update-inventories" -- "${cur}") )
        ;;
    "install_deps"|"bump_app_version")
        COMPREPLY=( $(compgen -W "-a --app=" -- "${cur}") )
        _decide_nospace ${COMPREPLY[0]}
        ;;
    "repo")
        COMPREPLY=( $(compgen -W \
            "submodules subtrees" -- "${cur}") )
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

    return 0
} &&
complete -F _my_python_apps_{current_date} {executable_name}
