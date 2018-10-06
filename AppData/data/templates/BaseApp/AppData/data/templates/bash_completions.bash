#!/bin/bash

# It would have been impossible to create this without the following post on Stack Exchange!!!
# https://unix.stackexchange.com/a/55622

# Other shells support. There is only Bash, nothing else exists.
# The nightmares caused by the use of Bash are more than enough to be bothered
# with support for any other shell in existence.

# Tested on Zsh:
#
# Completions work just fine provided that Zsh has been configured to support
# Bash completions.
#
# Things that doesn't work:
# - Auto completion of long options values. Short options values work just fine.
# - No space after auto-completing a long option. Most likely this is why the auto completion
#   of long options values doesn't work. Can't be bothered to fix this.

# Function definitions.
# Use the placeholder { current_date } (without the spaces) in the function names.
# This is to avoid conflicts between functions with the same name that are defined
# in different files that may perform slightly different tasks.

type "{executable_name}" &> /dev/null &&
_list_dirs(){
    # <3 https://stackoverflow.com/a/31603260
    # List all directories found inside the passed folder ($1).
    # WARNING! Fails on empty directories!
    # If certain amount of complexity is needed, just create a Python function on
    # the application's side that can be accessed as exemplified in the
    # _command_to_create_update_a_file_ function.
    (
        cd "${1}" && \
        set -- */; printf "%s\n" "${@%/}";
    )
} &&
_command_to_create_update_a_file_{current_date}(){
    echo $(cd {full_path_to_app_folder}; ./app.py argument)
} &&
_get_array_of_file_content_{current_date}(){
    local file_that_should_exist oldIFS
    file_that_should_exist="{full_path_to_app_folder}/UserData/app_ids"

    if [[ ! -f $file_that_should_exist ]]; then
        _command_to_create_update_a_file_{current_date}
    fi

    oldIFS="$IFS"
    IFS=$'\n'
    echo $(<$file_that_should_exist)
    IFS="$oldIFS"
} &&
_decide_nospace_{current_date}(){
    # Decide if after the completion of a term should a space character should be added or not.
    # It only works on Bash, not on Zsh. Not tested in any other shell.
    if [[ ${1} == "--"*"=" ]] ; then
        type "compopt" &> /dev/null && compopt -o nospace
    fi
} &&
_{{APP-SLUG-LOWER-LODASHED}}_cli_{current_date}(){
    local cur prev cmd
    COMPREPLY=()
    cur="${COMP_WORDS[COMP_CWORD]}"
    prev="${COMP_WORDS[COMP_CWORD-1]}"

    # Auto-complete items from an array.
    case $prev in
        --long-option-ending-with-equal-sign)
            COMPREPLY=( $( compgen -W "${array[*]}") )
            return 0
            ;;
        -short-option-not-ending-with-equal-sign)
            COMPREPLY=( $( compgen -W "${array[*]}" -- ${cur}) )
            return 0
            ;;
    esac

    # Completion of commands and "first level" options.
    if [[ $COMP_CWORD == 1 ]]; then
        COMPREPLY=( $(compgen -W "generate -h --help --manual --version" -- "${cur}") )
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
complete -F _{{APP-SLUG-LOWER-LODASHED}}_cli_{current_date} {executable_name}
