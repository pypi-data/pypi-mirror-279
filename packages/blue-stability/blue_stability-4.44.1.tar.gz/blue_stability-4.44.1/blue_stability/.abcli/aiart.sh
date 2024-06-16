#! /usr/bin/env bash

function blue_stability_generate() {
    aiart_generate \
        "$1" \
        app=blue_stability,image.args=++seed@42,video.args=++seed@42@++start_schedule@0.9,$2 \
        "${@:3}"
}

function blue_stability_transform() {
    aiart_transform \
        app=blue_stability,$1 \
        "${@:2}"
}
