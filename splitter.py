from sgmllib import SGMLParser

class WikiParser(SGMLParser):
    """Parses a TiddlyWiki into individual tiddlers."""
    def __init__(self):
        SGMLParser.__init__(self)
        self.tiddlers = list()
        self.current_tiddler = None

    def start_div(self, attrs):
        title, creator, tags = "", "", ""
        try:
            title = [y for (x,y) in attrs if x == "title" ][0]
            creator = [y for (x,y) in attrs if x == "creator"][0]
            tags = [y for (x,y) in attrs if x == "tags"][0]
        except IndexError:
            return

        self.current_tiddler = {"text": list(), "title": title, "tags": tags}

    def end_div(self):
        if self.current_tiddler:
            self.current_tiddler["text"] = "".join(self.current_tiddler["text"])
            self.tiddlers.append(self.current_tiddler)
            self.current_tiddler = None

    def handle_data(self, data):
        if self.current_tiddler:
            self.current_tiddler["text"].append(data)

def main():
    from optparse import OptionParser
    parser = OptionParser(usage="%prog [options] wiki.html")
    parser.add_option("-d", "--destination", dest="dest", default="txt", help="the directory to write text files to")
    opts, args = parser.parse_args()
    if not args:
        parser.error("you must specify the path to the TiddlyWiki file")
    wiki = open(args[0]).read().strip()
    parser = WikiParser()
    parser.feed(wiki)

    import os.path as P
    import os

    if not P.isdir(opts.dest):
        os.makedirs(opts.dest)

    for t in parser.tiddlers:
        fname = P.join(opts.dest, t["title"]) + ".txt"
        fout = open(fname, "w")
        fout.write(t["text"])
        fout.close()
        print "wrote [%s] to [%s]" % (t["title"], fname)
    
if __name__ == "__main__":
    import sys
    sys.exit(main())
