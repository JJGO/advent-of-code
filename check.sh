#!/usr/bin/env bash

# set -euo pipefail

for i in $1/p*; do
    python "$i" &> /dev/null
    if [[ "$?" -eq 0 ]]; then
        echo "$i ✅"
    else
        echo "$i ❌"
    fi
done
