#! /usr/bin/env bash

function kamangir() {
    local task=$(abcli_unpack_keyword $1 help)

    if [ $task == "help" ]; then
        kamangir_update "$@"
        return
    fi

    abcli_generic_task \
        plugin=kamangir,task=$task \
        "${@:2}"
}

abcli_source_path - caller,suffix=/tests
