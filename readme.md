annot2md
--------

This is a set of scripts for an automatic PDF annotation extraction workflow based around the Skim viewer and BibDesk bibliography manager for OS X. Skim is leveraged for its ability to cleanly extract text from Adobe-style highlight/underline/strike-through annotations. 

The script `bin/annot2md` ties everything together and should be the single entry point for taking the path to an annotated PDF file and producing a beautifully formatted markdown file presenting the annotated text.

>    Usage: annot2md [-h] filename
>
>    Use Skim to extract standard Adobe annotations and other
>    information about a PDF article to markdown format.

Some notes:

* Put `annot2md/bin` on your `$PATH`. If the `annot2md/bin/annot2md` script is directly symlinked, it won't be able to find the other scripts that it calls. Theoretically, all of the scripts could just be symlinked into your `~/bin` or whatever, but I didn't want to pollute the executable namespace.
* Markdown output files currently go to `~/Dropbox/Papers/Annotations`, but this can be changed at the top of the `annot2md` script if you want.
* No guarantees, this is working for my setup, but that's all I know for now.

Todo:

* Notes and highlights should be ordered by (-y, x) of top/left bounds; they seem to be nearly random right now for a given PDF page
* There should be a batch script to process a directory full of PDFs, find the ones with annotations, and then extract all notes
