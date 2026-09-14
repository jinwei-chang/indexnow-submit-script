import xml.etree.ElementTree as ET

import httpx


def is_url(source: str) -> bool:
    return source.startswith("http://") or source.startswith("https://")


def _load_root(source: str) -> ET.Element:
    if is_url(source):
        response = httpx.get(source, follow_redirects=True)
        response.raise_for_status()
        return ET.fromstring(response.content)
    return ET.parse(source).getroot()


def _local_tag(element: ET.Element) -> str:
    return element.tag.rpartition("}")[-1]


def parse_sitemap(source: str) -> list[str]:
    root = _load_root(source)

    if _local_tag(root) == "sitemapindex":
        urls = []
        for sitemap in root.findall("{*}sitemap"):
            loc = sitemap.find("{*}loc")
            if loc is not None and loc.text:
                urls.extend(parse_sitemap(loc.text))
        return urls

    urls = []
    for url in root.findall("{*}url"):
        loc = url.find("{*}loc")
        if loc is not None and loc.text:
            urls.append(loc.text)

    return urls
