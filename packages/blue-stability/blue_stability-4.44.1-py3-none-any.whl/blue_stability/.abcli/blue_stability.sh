#! /usr/bin/env bash

function blue_stability() {
    local task=$(abcli_unpack_keyword $1 help)

    if [ $task == "help" ]; then
        abcli_show_usage "blue_stability dashboard" \
            "browse blue-stability dashboard."

        blue_stability_generate "$@"

        abcli_show_usage "blue_stability notebook" \
            "browse blue stability notebook."

        blue_stability_transform "$@"
        return
    fi

    if [ "$task" == "dashboard" ]; then
        abcli_browse https://beta.dreamstudio.ai/membership
        return
    fi

    if [ "$task" == "notebook" ]; then
        pushd $abcli_path_git/blue-stability/nbs >/dev/null
        jupyter notebook
        popd >/dev/null
        return
    fi

    abcli_generic_task \
        plugin=blue_stability,task=$task \
        "${@:2}"
}

abcli_source_path - caller,suffix=/tests
