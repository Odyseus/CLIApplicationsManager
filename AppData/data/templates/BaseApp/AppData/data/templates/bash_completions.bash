#!/bin/bash

# It would have been impossible to create this without the following post on Stack Exchange!!!
# https://unix.stackexchange.com/a/55622

_have {executable_name} &&
__{{APP-SLUG-LOWER-LODASHED}}_{current_date}(){
    local cur prev cmd
    COMPREPLY=()
    cur="${COMP_WORDS[COMP_CWORD]}"
    prev="${COMP_WORDS[COMP_CWORD-1]}"

    # Completion of commands and "first level options.
    if [[ $COMP_CWORD == 1 ]]; then
        COMPREPLY=( $(compgen -W "generate -h --help --version" -- "${cur}") )
        return 0
    fi

    # Completion of options and sub-commands.
    cmd="${COMP_WORDS[1]}"

    case $cmd in
    "generate")
        COMPREPLY=( $(compgen -W "system_executable" -- "${cur}") )
        ;;
    esac
} &&
complete -F __{{APP-SLUG-LOWER-LODASHED}}_{current_date} {executable_name}
