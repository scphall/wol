wol
===

Wol is named for Owl in Winnie the Pooh (by A. A. Milne).**

    "And he respects Owl, because you can't help respecting anybody
    who can spell TUESDAY, even if he doesn't spell it right; but
    spelling isn't everything. There are days when spelling Tuesday
    simply doesn't count."
        - Rabbit, speaking of Christopher Robin

It is a packge to manage arXiv papers to prevent multiple instances in
Downloads directory.

Usage
-----
Apologies, this is out of date, done a load of changes, but the basics hold


1) Basic, you can guess these:

        $ wol help
        $ wol info

2) Add or move with add

        $ wol add *????.????*

   Can specify directory in which to add to:

        $ wol add *????.????* directory

   Can also add another .wol file (extension must be .wol) from someone else.

        $ wol add my_pals.wol

3) Move, mv all files from current location to new directory

        $ wol mv *????.????* new_directory

4) Update, just checks all is well

        $ wol update

5) Recent, lists up to 10 most recently added files

        $ wol recent

6) Config, configurables given in 'wol info' change using (for example):

        $ wol config viewer okular

7) Find, with no arguments all info will be printed, otherwise will print
   details on all files which match all arguments.  The findor command will
   do an or:

        $ wol find
        $ wol find options with an and
        $ wol findor options with an or

8)  Show, will open (in background) all files matching find arguments (with
   and).  Will not open if there are more than 5 papers which match.

9) Clean, removes dead stuff and empty dirs

        $ wol clean

10) Remove, remove a symbolic link and puts the arxiv paper in the .delete
   directory, this is removed with clean

        $ wol rm *????.????*

Installation
------------
0) Get the package from github:

        git clone https://github.com/hippyPig/wol

1) Simply put /wol in your chosen path.
2) In ~/.bashrc specify WOLDIR with export, and an alias.
   WOLDIR is the directory where files will be downloaded to.

        export WOLDIR=/path/to/where/to/put/files
        alias wol="/path/to/wol/python/wol.py"

3) GO!

Other
-----
I had problems with autocompletion, to resolve this try
`complete -p wol` (assuming wol is your alias). you should get:

        $ complete -p wol
        complete -F _wol wol

Then do, in .bashrc:

        $ complete -o nospace -f default -X '.*' -F _wol wol

Does not autocomplete options, this is on my todo list.
For old arxiv files, you must add with:

        $ wol add hep-ph/0123456


