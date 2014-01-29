wol
===

Wol is named for Owl in *Winnie the Pooh* (by *A. A. Milne*).


>    And he respects Owl, because you can't help respecting anybody
>    who can spell TUESDAY, even if he doesn't spell it right; but
>    spelling isn't everything. There are days when spelling Tuesday
>    simply doesn't count.
>
>->*Rabbit*, speaking of *Christopher Robin*<-

It is a packge to manage arXiv papers.
This prevents multiple copies of the same paper in `Downloads`, and gives them named that are easier to remember than 1234.3532.
Wol can also allows searching, opening of files and opening a paper's arXiv page in a browser at the type of a word or two.
The user can move queried files to different directories which serves as a method of tagging.

The title is automatically quieried from the internet, and if an arXiv number is given (rather than a filename), the paper will be downloaded.


Usage
---

1) Basic, you can guess these:

        $ wol help
        $ wol info

2) Add an arXiv paper to directory dir, directory is optional, otherwise goes
into default directory:

        $ wol add *????.????* dir

3) Delete an arXiv paper:

        $ wol del 1111.1111

3) Configuration show or edit

        $ wol config

4) Add another dotwol file:

        $ wol addwol newdotwol

5) Find papers that match regexp expression:

        $ wol find thing
        $ wol find        # displays all

6) Move all files that match a find:

        $ wol mv *????.????* new_directory

7) Update, just checks all is well

        $ wol update

8) Show, displays (upto a maximum) number of files that match a criteria:

        $ wol show thing

9) Show arXiv page in browser, (upto a maximum) number of files that match a criteria:

        $ wol browse thing

ArXiv files are usually of the form `1234.5678`, but they can also be of the
form `name/1234567`.
These are also supported, use (for example) `wol add hep-ph/1234567`
for these.


Installation
------------
0) Get the package from github:

        $ git clone https://github.com/hippyPig/wol

1) Simply put /wol in your chosen path.
2) In ~/.bashrc specify WOLDIR with export, and an alias.
   WOLDIR is the directory where files will be downloaded to.

        $ export WOLDIR=/path/to/where/to/put/files
        $ export PATH=$PATH:/path/to/wol
        $ source /path/to/wol/python/wol_autocomplete.sh  # for autocompletion of args

3) **GO!**

Other
-----
I had problems with autocompletion of files, to resolve this try
`complete -p wol` (assuming wol is your alias). you should get:

        $ complete -p wol
        $ complete -F _wol wol

Then do, in .bashrc:

        $ complete -o nospace -f default -X '.*' -F _wol wol



