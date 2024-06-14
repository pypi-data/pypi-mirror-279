import dataclasses
import pprint
from dataclasses import dataclass


@dataclass(repr=False, init=False)
class Comic:
    link_suffix: str
    title: str
    base_url: str
    url: str
    publisher: str
    format: str
    image_url: str

    def __init__(self, **kwargs):
        self.link_suffix = kwargs.pop('link_suffix', "")
        self.title = kwargs.pop('title', "")
        self.base_url = kwargs.pop('base_url', "")
        if self.base_url and self.link_suffix:
            self.url = self.base_url + self.link_suffix
        else:
            self.url = kwargs.pop('url', '')
        self.image_url = kwargs.pop('image_url', '')
        self.publisher = kwargs.pop('publisher', "unknown")
        self.determine_format()

    def get_link(self) -> str:
        return self.base_url + self.link_suffix

    def determine_format(self):
        """Determines the format of the comic based on the presence of key identifiers in the source's name"""
        tpb_key_identifiers = ["tp", "tpb"]
        hardcover_key_identifiers = ["hardcover", "hc"]
        tokenized_title = self.title.lower().split(" ")
        for token in tokenized_title:
            if token in tpb_key_identifiers:
                self.format = "tradepaperback"
                return
            elif token in hardcover_key_identifiers:
                self.format = "hardcover"
                return

        self.format = "unknown"



    def __repr__(self):
        return pprint.pformat(dataclasses.asdict(self))
