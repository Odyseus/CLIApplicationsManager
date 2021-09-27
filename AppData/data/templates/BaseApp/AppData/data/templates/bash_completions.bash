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
# Function that "returns" the value of an argument that already exists in the CLI while one is
# writing command arguments/options. Explaining why this is needed is even more complex than
# what I just wrote! LOL
# TODO: Create article in my own knowledge base based on the StackOverflow answer.
# <3 https://stackoverflow.com/a/7948533
_get_argument_value_from_cli_{current_date}(){
    local tmp
    tmp=$(getopt --quiet --options p: --longoptions profile: -- "${COMP_WORDS[@]}")

    eval set -- "$tmp"

    while true; do
        case "$1" in
        -p|--profile)
            echo "$2"
            shift 2
            ;;
        --)
            shift
            break
            ;;
        *)
            break
            ;;
        esac
    done
} &&
# Function to call app.py (the app for which this auto-completion script is written for)
# with a single argument that will print data (a "list" of strings separated by new lines)
# to STDOUT.
# I use this function basically for two tasks:
# 1. To get a list of files from a folder that exists inside the Python application structure
#    (AppData or UserData).
# 2. To get data from a file which is easily parseable by Python (basically anything). In Bash
#    I can barely parse data that's arranged with spaces/new lines.
_function_to_easyly_get_data_{current_date}(){
    echo $(cd {full_path_to_app_folder}; ./app.py argument)
} &&
# Function to decide if after the completion of a term should a space character be added or not.
# It only works on Bash, not on Zsh. Not tested in any other shell.
_decide_nospace_{current_date}(){
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
