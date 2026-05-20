import requests
from xml.etree import ElementTree as ET
import os

FEED_URL = "https://www.ilpost.it/feed"
FEED_SELF_URL = "https://michilillo.github.io/ilpost-filtered/feed.xml"

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
    "Storie/Idee",
]
# ======================================

WHITELIST_LOWER = {c.lower() for c in WHITELIST}

NS = {
    "content": "http://purl.org/rss/1.0/modules/content/",
    "dc": "http://purl.org/dc/elements/1.1/",
    "atom": "http://www.w3.org/2005/Atom",
}

def fetch_and_filter():
    resp = requests.get(
        FEED_URL,
        timeout=20,
        headers={"User-Agent": "Mozilla/5.0"}
    )

    resp.raise_for_status()

    # Parsa XML originale
    root = ET.fromstring(resp.content)

    channel_in = root.find("channel")

    if channel_in is None:
        raise RuntimeError(
            "Feed non valido: elemento <channel> non trovato"
        )

    # Costruzione nuovo feed RSS
    rss_out = ET.Element("rss", version="2.0")

    rss_out.set("xmlns:content", NS["content"])
    rss_out.set("xmlns:dc", NS["dc"])
    rss_out.set("xmlns:atom", NS["atom"])

    channel_out = ET.SubElement(rss_out, "channel")

    ET.SubElement(
        channel_out,
        "title"
    ).text = "Il Post [filtrato]"

    ET.SubElement(
        channel_out,
        "link"
    ).text = "https://www.ilpost.it"

    ET.SubElement(
        channel_out,
        "description"
    ).text = (
        f"Feed filtrato — categorie: {', '.join(WHITELIST)}"
    )

    ET.SubElement(
        channel_out,
        "language"
    ).text = "it-IT"

    # Self reference RSS
    atom_link = ET.SubElement(
        channel_out,
        "{http://www.w3.org/2005/Atom}link"
    )

    atom_link.set("href", FEED_SELF_URL)
    atom_link.set("rel", "self")
    atom_link.set("type", "application/rss+xml")

    included = 0
    skipped = 0

    for item_in in channel_in.findall("item"):

        # Legge tutte le categorie
        categories = set()

        for child in item_in:
            if child.tag.endswith("category"):

                category_text = (
                    (child.text or "")
                    .strip()
                    .lower()
                )

                if category_text:
                    categories.add(category_text)

        # Tiene articoli con almeno una categoria valida
        if not categories.intersection(WHITELIST_LOWER):
            skipped += 1
            continue

        item_out = ET.SubElement(channel_out, "item")

        def cp(tag, dest_tag=None):
            el = item_in.find(tag)

            if el is not None and el.text:
                ET.SubElement(
                    item_out,
                    dest_tag or tag
                ).text = el.text.strip()

        cp("title")
        cp("link")
        cp("pubDate")
        cp("description")

        guid_el = item_in.find("guid")

        if guid_el is not None:
            g = ET.SubElement(item_out, "guid")

            g.text = (guid_el.text or "").strip()

            g.set(
                "isPermaLink",
                guid_el.get("isPermaLink", "false")
            )

        # Copia categorie
        for cat_el in item_in.findall("category"):
            if cat_el.text:
                ET.SubElement(
                    item_out,
                    "category"
                ).text = cat_el.text.strip()

        # dc:creator opzionale
        creator = item_in.find(
            f"{{{NS['dc']}}}creator"
        )

        if creator is not None and creator.text:
            dc_el = ET.SubElement(
                item_out,
                "dc:creator"
            )

            dc_el.text = creator.text.strip()

        included += 1

    print(f"Inclusi: {included} | Scartati: {skipped}")

    tree = ET.ElementTree(rss_out)

    ET.indent(tree, space="  ")

    output_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "feed.xml"
    )

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(
            '<?xml version="1.0" encoding="UTF-8"?>\n'
        )

        tree.write(f, encoding="unicode")

    print(f"Feed salvato in: {output_path}")

if __name__ == "__main__":
    fetch_and_filter()
