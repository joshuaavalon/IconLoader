from pathlib import Path
from typing import List
from urllib.parse import urljoin

import requests
from PIL import Image
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/66.0.3359.170 Safari/537.36"
}


def download_favicon(url: str, path: Path) -> bool:
    icon_url = urljoin(url, "favicon.ico")
    success = download_image(icon_url, path)
    if success:
        return True
    icons = get_icons(url)
    for icon in icons:
        success = download_image(icon, path)
    if success:
        return True
    return False


def get_icons(url: str) -> List[str]:
    icons = []
    response = requests.get(url, stream=True, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        for link in soup.select("head > link"):
            if not link.has_attr("rel") or not link.has_attr("href"):
                continue
            rels = link["rel"]
            if "shortcut" in rels or "icon" in rels or "apple-touch-icon" in rels:
                icons.append(urljoin(url, link["href"]))
    return icons


def download_image(url: str, path: Path) -> bool:
    response = requests.get(url, stream=True, headers=headers)
    if response.status_code == 200:
        response.raw.decode_content = True
        image = Image.open(response.raw)  # type: Image
        image.save(path)
        return True
    return False
