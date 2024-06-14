#!/bin/bash

# $1 - a request: '?' - list actions, '!' - execute the command.
# $2 - an action to perform. If empty, a single action is assumed.
# $@ - the action's arguments, if any.

set -e
ROOT="$(realpath $(dirname "${BASH_SOURCE[0]}")/..)"

if [[ $1 == '?' ]]; then
    # TODO: Populate the actions, if any.
    LIST=()
    for ITEM in "${LIST[@]}"; do
        echo ${ITEM}
    done
fi

if [[ $1 == '!' ]]; then
    LIST=("${@:3}")
    # TODO: Perform an action.
    echo "Action: $2"
    for ITEM in "${LIST[@]}"; do
        echo "Argument: ${ITEM}"
    done
fi
