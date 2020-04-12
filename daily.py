from abc import ABC
from html.parser import HTMLParser


class DailyParser(HTMLParser, ABC):
    def __init__(self, *, convert_charrefs=True):
        super().__init__(convert_charrefs=convert_charrefs)
        '''str array'''
        self.data = []

    def handle_starttag(self, tag, attrs):
        super().handle_starttag(tag, attrs)
        if tag == "section" and ("class", "ranking-item") in attrs:
            for attr in attrs:
                if attr[0] == "data-id":
                    self.data.append(attr[1])



