"""Attempts to convert TiddlyWiki markup to notes.vim markup.
WARNING: will overwrite the file it is processing."""

if __name__ == "__main__":
    import sys
    import re
    if len(sys.argv) != 2:
        print >> sys.stderr, "usage: %s filename.txt" % __file__
        sys.exit(1)

    lines = open(sys.argv[1]).read().strip().split("\n")
    for i,line in enumerate(lines):
        # numbered lists (convert them to bulleted lists for simplicity)
        line = re.sub("^###", u"        \u2022", line)
        line = re.sub("^##", u"    \u2022", line)
        line = re.sub("^#", u"\u2022", line)
        # bulleted lists
        line = re.sub("^\*\*\*", u"        \u2022", line)
        line = re.sub("^\*\*", u"    \u2022", line)
        line = re.sub("^\*", u"\u2022", line)
        # headings
        line = re.sub("^!+", "#", line)
        # TiddlyWiki-specific markup
        line = re.sub("~", "", line)
        line = re.sub("}}}", "", line)
        line = re.sub("{{{", "", line)
        line = re.sub("//", "_", line)
        lines[i] = line

    import codecs
    fout = codecs.open(sys.argv[1], "w", "utf-8")
    fout.write("\n".join(lines))
    fout.close()
