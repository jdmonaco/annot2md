#!/usr/bin/osascript 

tell application "Skim"
	
	set the clipboard to ""
	activate
	
	set listOfNoteTypes to every type of notes of document 1
	set listOfNoteText to text of every note of document 1
	set listOfNotePages to index of every page of every note of document 1
	
	repeat with i from 1 to count of listOfNoteTypes
		
		set noteText to item i of listOfNoteText
		set thePage to item i of listOfNotePages as string
		set theType to item i of listOfNoteTypes as string
		
		set the clipboard to (the clipboard) & thePage & ":" & Â
			theType & ":{" & noteText & "}" & return & return
		
	end repeat
	
end tell