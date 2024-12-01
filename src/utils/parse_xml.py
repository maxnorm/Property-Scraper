import xml.etree.ElementTree as ET

def parse_xml(file_path):
    """
    Parse an XML file and return a list of URLs.
    :param file_path:  Path to the XML file
    :return: List of URLs <loc> tags
    """
    tree = ET.parse(file_path)
    root = tree.getroot()

    namespace = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}

    urls = [url.text for url in root.findall('.//ns:loc', namespace)]
    fr_urls = [url for url in urls if '/fr/' in url]
    return fr_urls
