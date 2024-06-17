from html.parser import HTMLParser
from typing import List

__all__ = ["DataFromHTMLSnippet"]


class DataFromHTMLSnippet(HTMLParser):
    """Class to turn a html fragmet into a list of data items.

    Usage:
    >>> parser = MyHTMLParser()
    >>> parser.to_list(html_fragmemt)
    [<list with data objects from html_fragment>]

    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.result_list = []

    def to_list(self, html_fragment: str) -> List:
        self.feed(html_fragment)
        return self.result_list

    def handle_data(self, data):
        if data := data.strip():
            self.result_list.append(data)
