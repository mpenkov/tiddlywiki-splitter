"""Attempts to convert TiddlyWiki markup to notes.vim markup.
WARNING: will overwrite the file it is processing."""
import re

def vim_notes_format(title, lines, raw_txt):
    """title    The title of the tiddler
       lines    A list of lines representing the tiddler body
       raw_txt  The tags as a string."""
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
        lines.append(" ".join(map(lambda t: "@%s" % t, tags)))
    except IndexError:
        pass

    return "\n".join(lines)
