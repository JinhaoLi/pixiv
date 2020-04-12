from html.parser import HTMLParser


class IllustParser(HTMLParser):
    def __init__(self, *, convert_charrefs=True):
        super().__init__(convert_charrefs=convert_charrefs)
        self.json_text=""

    def handle_starttag(self, tag, attrs):
        super().handle_starttag(tag, attrs)
        if tag == "meta" and ("id", "meta-preload-data") in attrs:
            for attr in attrs:
                if attr[0] == "content":
                    self.json_text = attr[1]