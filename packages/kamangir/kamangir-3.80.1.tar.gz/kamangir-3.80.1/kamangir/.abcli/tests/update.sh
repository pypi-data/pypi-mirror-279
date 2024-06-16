#! /usr/bin/env bash

function test_kamangir_update() {
    local options=$1
    local do_dryrun=$(abcli_option_int "$options" dryrun 0)

    abcli_eval dryrun=$do_dryrun \
        "kamangir update ${@:2}"
}
