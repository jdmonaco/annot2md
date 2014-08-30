#!/usr/bin/osascript 

on run argv
	
	set usageString to "Usage: " & (my name as string) & " <field-name> <cite-key>"
	
	if (length of argv = 2) then
		set queryField to item 1 of argv
		set citeKey to item 2 of argv
	else
		return usageString
	end if
	
	tell application "BibDesk"
			
		set theDoc to get first document
		tell theDoc
			
			set thePub to get item 1 of (publications whose cite key contains citeKey)
			tell thePub
			
				set theTitle to get value of field queryField
				
			end tell --thePub				
		end tell --theDoc
		
		return theTitle		
	end tell	
end run