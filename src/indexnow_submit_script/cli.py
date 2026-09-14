import argparse
import os
import xml.etree.ElementTree as ET

import httpx
from dotenv import load_dotenv

from .indexnow import submit_urls
from .sitemap import is_url, parse_sitemap


def main() -> None:
    load_dotenv()

    parser = argparse.ArgumentParser(description="Submit URLs to IndexNow.")
    parser.add_argument("sitemap", help="Path or URL to a sitemap .xml file")
    parser.add_argument(
        "--host",
        default=os.environ.get("INDEXNOW_HOST"),
        required=not os.environ.get("INDEXNOW_HOST"),
        help="Host name to submit, e.g. example.com (env: INDEXNOW_HOST)",
    )
    parser.add_argument(
        "--key",
        default=os.environ.get("INDEXNOW_KEY"),
        required=not os.environ.get("INDEXNOW_KEY"),
        help="IndexNow API key (env: INDEXNOW_KEY)",
    )
    parser.add_argument("--endpoint", default="indexnow", choices=["indexnow", "bing"])
    args = parser.parse_args()

    if not is_url(args.sitemap) and not args.sitemap.lower().endswith(".xml"):
        print("only .xml sitemap files or urls are supported.")
        return

    print("loading sitemap:", args.sitemap)
    try:
        urls_to_submit = parse_sitemap(args.sitemap)
    except (ET.ParseError, httpx.HTTPError, OSError) as exc:
        print("failed to load sitemap:", exc)
        return

    if len(urls_to_submit) == 0:
        print("empty url list.")
        return

    print("urls find:", len(urls_to_submit))
    print("urls:", urls_to_submit)

    try:
        submit_urls(args.host, args.key, urls_to_submit, endpoint=args.endpoint)
    except httpx.HTTPError as exc:
        print("failed to submit urls:", exc)
