#!/bin/bash

#
# Script to use Skim to convert PDF annotations and then export an easily 
# parsable text file
#

if [[ $# -ne 2 ]]; then
    echo "Usage: `basename "$0"` pdf_file txt_file"
    exit 1
fi

INPUTPDF="$1"
BASE=`basename "$INPUTPDF"`

OUTPUTTXT="$2"

# Copy the original file to a temp directory
TMP=`mktemp -d -t skim-notes`
DUPE="$TMP/$BASE"
cp "$INPUTPDF" "$TMP"

# Open duplicate in Skim, convert notes, then collect note data in clipboard
open "$DUPE" -a skim
/usr/bin/osascript <<CONVERT
tell application "Skim"
    convert notes document 1
    save document 1

    set the clipboard to ""
    
    set allNotes to notes of document 1
    repeat with i from 1 to count of allNotes
        set theNote to item i of allNotes
        
        set noteType to type of theNote
        set noteText to text of theNote
        set notePage to index of page of theNote
        
        set noteLeft to item 1 of (get bounds for theNote) as string
        set noteTop to item 2 of (get bounds for theNote) as string
        
        set the clipboard to (the clipboard) & notePage & ":" & noteLeft & ¬
            ":" & noteTop & ":" & noteType & ":" & noteText & return & return
        
    end repeat
    close document 1
end tell
CONVERT

# Create a new text file with the note data while also translating
# the Applescript carriage returns into proper newlines
pbpaste -Prefer txt | tr "\r" "\n" > "$OUTPUTTXT"
