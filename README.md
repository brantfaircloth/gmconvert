# README GMCONVERT v 0.31; Copyright (c) 2005-2006, Brant C. Faircloth

## Disclaimer

GeneMapper(TM) is a registered trademark of Applera Corporation and its subsidiaries in the U.S. and other countries.

I am in no way associated with Applera, Perkin-Elmer, Applied Biosystems, Life Technologies, etc. I wrote this program to help myself and those in my group work a bit faster. I thought it might help others.

## About this program

This program is mean to convert files exported by Applied Biosystem's GeneMapper(TM) software to a format that is more useful. It essentially re-arrays the data from row to column format. Pretty much every program i have used for analysis demands the data be in column format of some sort.

The program is distributed as executables for both OS X and Windows (XP). These both have a simple GUI allowing user interaction. Neither require that python or wxpython (the windowing system) be installed as they are bundled with the application.

There is also a command-line version (GMCONVERT_command) that should be supported on all operating systems supporting Python and with Python installed. My machine runs python 2.4.2 at the moment, so you should have at least that version. If you do not, things may work strangely.

## Caveats

Generally, I haven't found too many. However, you should be aware that your markers must have consistent names if they are placed in different panels. For example, if you have 'Primer15' in one panel and 'primer15' in another and these are actually the same primer, then you are going to have some problems. The main reason is that the program is case sensitive, so the previous examples are NOT the same. So, if you run your exported file with this sort of thing in there, then you will get separate results for 'Primer15' and 'primer15'. Bummer. This is easily remedied by ensuring your primer names are the same across any and all panels in which they happen to be found.

You should also be aware that + and - control samples will be exported from GeneMapper assuming they pass concordance control. This is stupid, but not my fault. So, once you have converted your files, you should remove these.

Finally, GMCONVERT does not count samples with GQ scores < 0.75. Typically, these should not be used in analysis. If you manually edit allele calls, your GQ score should be set to 1.0 (this occurs automatically). If there is interest, I may add an option to include calls of lesser quality in a subsequent release.

## Platforms

I have tested the binary, executable versions of GMCONVERT on the following platforms:

* Apple OS X (10.4.4) - all worked well
* Windows XP, SP2 - all worked well
* Linux - all worked

## About the files in the archive

* cli/gmconvert_command.py (command line version)
* gui/gmconvert_source.py (source code for GUI version)
* README.md - this file
* CHANGELOG.md
* test.genemapper - data file for testing

## Invoking the program

    $./gmconvert_command.py -i /Users/bcf/15_good_samples_3OLG_ls.txt -o /users/bcf/desktop/test5.csv -f gerud

Where the options are as follows:

-i [file_of sequences]
-f [format of outfile]
-o [output file location]
-h [shows command-line options and an example]
where -f = 'cervus' | 'genepop' | 'gerud'

## Why are there 2 versions?

There are 2 versions for several reasons. There is a GUI version for OS X and Windows because it is easy to use. There is a command-line version because it can be used for batch-processing of numerous file given a little python or shell-scripting magic (this is up to you). The command-line version will also run on numerous platforms for which I don't have time to create a GUI.

## Why only 3 file format options?

Well, because I am lazy. Seriously, cervus, genepop, and gerud ought to cover a lot of actual programs since many do cross-conversion of files from one type to another these days. If there is something that you absolutely must have, let me know and I will add it to the list.

## Technical details

The actual script was created using python, the windowing system uses wxPython, the application bundles were built with py2app (OS X) or py2exe (Windows), the icons were made in Photoshop, the .dmg file for OS X was created using DropDMG, and the Zip file for Windows was created on XP.