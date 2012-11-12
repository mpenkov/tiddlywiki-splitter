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

    #
    # Handle tags.
    #
    try:
        raw_txt = filter(lambda l: l.startswith("tags:"), lines)[0][6:]
        raw_txt = raw_txt.replace("[[", " [[ ").replace("]]", " ]] ")
        tokens = filter(None, raw_txt.split(" "))
        tags = list()
        escape = False
        start = 0
        for i,t in enumerate(tokens):
            if t == "[[":
                escape = True
                start = i+1
            elif t == "]]":
                escape = False
                tags.append("_".join(tokens[start:i]))
            elif not escape:
                tags.append(t)

        for i,l in enumerate(lines):
            if l.startswith("tags:"):
                lines[i] = " ".join(map(lambda t: "@%s" % t, tags))
    except IndexError:
        pass

    import codecs
    fout = codecs.open(sys.argv[1], "w", "utf-8")
    fout.write("\n".join(lines))
    fout.close()
