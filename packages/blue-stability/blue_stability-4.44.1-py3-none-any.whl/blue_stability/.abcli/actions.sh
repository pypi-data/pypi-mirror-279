#! /usr/bin/env bash

function blue_stability_action_git_before_push() {
    [[ "$(abcli_git get_branch)" == "main" ]] &&
        blue_stability pypi build
}
