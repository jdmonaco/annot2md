#!/bin/bash

#
# Batch script to extract all annotations from directory tree of pdf files
#

PAPERS="$HOME/Dropbox/Papers"
PDF_FILES=`find "$PAPERS" -name "*.pdf"`

IFS=$(echo -en "\n\b")
SUBTYPE=/Type/Annot/Subtype/

for f in $PDF_FILES; do
    if grep "$SUBTYPE" "$f" > /dev/null; then
        echo "calling: annot2md \"$f\""
        annot2md "$f"
    fi
done
