#!/usr/bin/osascript 

on run argv
	
	set usageString to "Usage: BibdeskTitle.scpy <cite-key>"
	
	if (length of argv = 1) then
		set citeKey to item 1 or argv
	else
		return usageString
	end if
	
	tell application "BibDesk"
		
		set theDoc to get first document
		tell theDoc
			
			set thePubs to (publications whose cite key contains citeKey)
			set thePub to get item 1 of thePubs
			
			tell thePub
				
				set theTitle to get value of field "Title"
				
			end tell --thePub	
		end tell --theDoc
		
		return theTitle
		
	end tell
	
end run