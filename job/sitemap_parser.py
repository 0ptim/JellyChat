import requests
from lxml import etree


def get_urls(url):
    loc_list = []

    # Fetch the XML content
    response = requests.get(url)

    if response.status_code == 200:
        xml_content = response.content

        # Parse the XML content
        root = etree.fromstring(xml_content)

        # Extract the <loc> values
        loc_tags = root.findall(
            ".//{http://www.sitemaps.org/schemas/sitemap/0.9}loc")
        for tag in loc_tags:
            loc_list.append(tag.text)

    return loc_list
