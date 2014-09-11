#!/usr/bin/osascript 

tell application "Skim"
	
	set the clipboard to ""
	activate
	
	set allNotes to notes of document 1
	
	repeat with i from 1 to count of allNotes
		
		set theNote to item i of allNotes
		
		set noteType to type of theNote
		set noteText to text of theNote
		set notePage to index of page of theNote
		
		set noteLeft to item 1 of (get bounds for theNote) as string
		set noteTop to item 2 of (get bounds for theNote) as string
		
		set the clipboard to (the clipboard) & notePage & ":" & noteLeft & Â
			":" & noteTop & ":" & noteType & ":" & noteText & return & return
		
	end repeat
end tell