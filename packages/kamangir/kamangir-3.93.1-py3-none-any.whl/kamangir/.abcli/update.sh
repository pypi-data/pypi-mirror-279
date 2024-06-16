#! /usr/bin/env bash

function kamangir_update() {
    local options=$1

    if [ $(abcli_option_int "$options" help 0) == 1 ]; then
        abcli_show_usage "kamangir update [push]" \
            "update README.md."
        return
    fi

    local do_push=$(abcli_option_int "$options" push 0)

    python3 -m kamangir \
        update \
        "${@:2}"

    if [[ "$do_push" == 1 ]]; then
        abcli_git kamangir push \
            "$(python3 -m kamangir version) update"
    else
        abcli_git kamangir status ~all
    fi
}
