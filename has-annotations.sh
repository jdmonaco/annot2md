#!/bin/bash

IFS=$(echo -en "\n\b")
SUBTYPE=/Type/Annot/Subtype/

if [[ $# = 0 ]]; then
    echo "Usage: `basename ${0}` pdf-file [pdf-file ...]"
    exit 1
fi

for f in $@; do
    if grep "$SUBTYPE" "$f" > /dev/null; then
        echo "found annotations: \"$f\""
    fi
done
