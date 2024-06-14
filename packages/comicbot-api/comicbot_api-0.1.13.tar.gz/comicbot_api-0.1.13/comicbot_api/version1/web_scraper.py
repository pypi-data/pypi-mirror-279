from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
import requests
from comicbot_api.utils.comic import Comic
from bs4 import BeautifulSoup, Tag
from typing import List


def comic_title_finder(tag: Tag) -> bool:
    return tag.has_attr('class') and 'title' in tag.get('class')

def strip_comic_name(name: str) -> str:
    num_spaces = 0
    new_name = ""
    for char in name:
        if char.isspace() and num_spaces > 1:
            return str(new_name).strip()
        elif char.isspace():
            num_spaces += 1
        new_name += char
    return str(new_name)


def comic_cover_image_finder(tag: Tag) -> bool:
    return tag.has_attr('class') and 'cover-gallery' in tag.get('class')


def comic_publisher_finder(tag: Tag) -> bool:
    return tag.has_attr('class') and 'header-intro' in tag.get('class')


@dataclass
class WebScraper:
    base_url: str
    parser: str = 'html.parser'
    headers: dict = field(default_factory=lambda: {'User-Agent': 'Mozilla/5.0'})

    def scrape_comics(self, url: str) -> List:
        comic_releases_response = requests.get(url, headers=self.headers)
        if comic_releases_response.status_code == 200:
            comic_releases_html = comic_releases_response.json().pop('list')
            soup = BeautifulSoup(comic_releases_html, self.parser)
            all_comic_titles = soup.findAll(comic_title_finder)
            comics = list(map(lambda link:
                              Comic(base_url=self.base_url,
                                    link_suffix=link.attrs.pop('href'),
                                    title=link.contents[0].strip()),
                              all_comic_titles))
            with ThreadPoolExecutor() as executor:
                executor.map(self.set_comic_cover_image, comics)
            return comics
        return []

    def set_comic_cover_image(self, comic: Comic):
        """From a base url for a comic, searches for the image used for the comic and returns its URL"""
        comic_url = comic.url
        response = requests.get(comic_url, headers=self.headers)
        soup = BeautifulSoup(response.text, self.parser)
        cover_image_tags = soup.findAll(comic_cover_image_finder)
        publisher_tags = soup.findAll(comic_publisher_finder)
        if len(publisher_tags) > 0:
            comic.publisher = strip_comic_name(publisher_tags[0].get_text().strip())
        if len(cover_image_tags) > 0:
            comic.image_url = cover_image_tags[0].get('href', "cover image not found")
