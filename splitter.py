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
    import sys
    wiki = open(sys.argv[1]).read().strip()
    parser = WikiParser()
    parser.feed(wiki)
    print len(parser.tiddlers), "tiddlers parsed"
    for i,t in enumerate(parser.tiddlers):
        print i, t["title"]

if __name__ == "__main__":
    main()
