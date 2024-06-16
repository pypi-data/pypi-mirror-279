#! /usr/bin/env bash

function blue_stability_generate_function() {
    local options=$1
    local dryrun=$(abcli_option_int "$options" dryrun 1)
    local height=$(abcli_option "$options" height)
    local width=$(abcli_option "$options" width)

    local filename=$(abcli_clarify_input $2 frame)

    local prev_filename=$(abcli_clarify_input $3)

    local sentence=$4

    abcli_log "blue_stability: generate: image: \"$sentence\" -[$prev_filename.png ${@:5}]-> $filename.png"

    local extra_args="--seed 42"
    if [ ! -z "$prev_filename" ] ; then
        local extra_args="$extra_args --init ../raw/$prev_filename.png --start_schedule 0.9"
    fi
    if [ ! -z "$height" ] ; then
        local extra_args="$extra_args --height $height"
    fi
    if [ ! -z "$width" ] ; then
        local extra_args="$extra_args --width $width"
    fi

    local command_line="python3 -m stability_sdk.client \
        $extra_args \
        ${@:5} \
        \"$sentence\""

    abcli_log "⚙️  $command_line"

    if [ "$dryrun" == 1 ] ; then
        return
    fi

    local temp_path=$abcli_object_path/$app_name-$(abcli_string_timestamp)
    mkdir -p $temp_path

    pushd $temp_path > /dev/null
    eval $command_line
    popd > /dev/null

    mv -v $temp_path/*.png $abcli_object_path/raw/$filename.png
    mv -v $temp_path/*.json $abcli_object_path/raw/$filename.json

    rm -rf $temp_path
}