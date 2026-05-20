import feedparser
import requests
from xml.etree import ElementTree as ET
from datetime import datetime, timezone
import os

FEED_URL = "https://www.ilpost.it/feed"

# === CONFIGURA QUI LE TUE CATEGORIE ===
WHITELIST = [
    "Italia",
    "Mondo",
    "Politica",
    "Tecnologia",
    "Internet",
    "Scienza",
    "Cultura",
    "Economia",
    "Sport",
    "Libri",
    "Consumismi",
]
# ======================================

WHITELIST_LOWER = {c.lower() for c in WHITELIST}

def fetch_and_filter():
    resp = requests.get(FEED_URL, timeout=20, headers={"User-Agent": "Mozilla/5.0"})
    resp.raise_for_status()
    feed = feedparser.parse(resp.text)

    rss = ET.Element("rss", version="2.0")
    rss.set("xmlns:content", "http://purl.org/rss/1.0/modules/content/")
    rss.set("xmlns:dc", "http://purl.org/dc/elements/1.1/")
    rss.set("xmlns:atom", "http://www.w3.org/2005/Atom")

    channel = ET.SubElement(rss, "channel")
    ET.SubElement(channel, "title").text = "Il Post [filtrato]"
    ET.SubElement(channel, "link").text = "https://www.ilpost.it"
    ET.SubElement(channel, "description").text = f"Feed filtrato — categorie: {', '.join(WHITELIST)}"
    ET.SubElement(channel, "language").text = "it-IT"
    ET.SubElement(channel, "lastBuildDate").text = datetime.now(timezone.utc).strftime(
        "%a, %d %b %Y %H:%M:%S +0000"
    )

    included = 0
    skipped = 0

    for entry in feed.entries:
        tags = entry.get("tags", [])
        categories = {t.get("term", "").lower() for t in tags}

        if not categories.intersection(WHITELIST_LOWER):
            skipped += 1
            continue

        item = ET.SubElement(channel, "item")
        ET.SubElement(item, "title").text = entry.get("title", "")
        ET.SubElement(item, "link").text = entry.get("link", "")
        ET.SubElement(item, "pubDate").text = entry.get("published", "")
        ET.SubElement(item, "guid", isPermaLink="true").text = entry.get("id", entry.get("link", ""))

        for tag in tags:
            term = tag.get("term", "")
            if term:
                ET.SubElement(item, "category").text = term

        desc = entry.get("summary", "")
        if desc:
            ET.SubElement(item, "description").text = desc

        included += 1

    print(f"Inclusi: {included} | Scartati: {skipped}")

    tree = ET.ElementTree(rss)
    ET.indent(tree, space="  ")
    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "feed.xml")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        tree.write(f, encoding="unicode")
    print(f"Feed salvato in: {output_path}")


if __name__ == "__main__":
    fetch_and_filter()
