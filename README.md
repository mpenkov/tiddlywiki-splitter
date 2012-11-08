tiddlywiki-splitter
===================

Split a TiddlyWiki into multiple text files, one file per tiddler.

A TiddlyWiki (http://tiddlywiki.com) can be great for keeping notes.  However,
it keeps everything in a single file, and can become difficult to manage when
the volume of notes gets large.

This project splits a TiddlyWiki into multiple text files.  The files can then
be imported into vim.notes (https://github.com/xolox/vim-notes) or an
alternative note-keeping solution.

Usage
-----

    git clone https://github.com/mpenkov/tiddlywiki-splitter.git
    cd tiddlywiki-splitter
    python splitter.py wiki.html -d destination_directory

The wiki.html file will then be split into separate text files in destination directory.  Optionally, if you want to convert the text files from TiddlyWiki syntax to notes.vim syntax:

    for f in destination_directory/*.txt; do python formatter.py "$f"; done

Note that this will **overwrite** the text files.  Back them up first if it's a big deal to you (they can also be recovered by re-splitting
the wiki.html).
