import os
from xml.dom.minidom import parseString
from xml.etree.ElementTree import Element, SubElement, tostring, ElementTree
from datetime import datetime

def generate_rss_feed(aggregated_items, config, output_path):
    # Create the root element with namespaces
    rss = Element('rss', version='2.0', nsmap={'atom': 'http://www.w3.org/2005/Atom'})
    channel = SubElement(rss, 'channel')

    # Add channel metadata
    title = SubElement(channel, 'title')
    title.text = config.get('feed_title', 'UglyFeed RSS')

    link = SubElement(channel, 'link')
    link.text = config.get('feed_link', 'https://github.com/fabriziosalmi/UglyFeed')

    description = SubElement(channel, 'description')
    description.text = config.get('feed_description', 'A dynamically generated feed using UglyFeed.')

    language = SubElement(channel, 'language')
    language.text = config.get('feed_language', 'en')

    self_link = SubElement(channel, '{http://www.w3.org/2005/Atom}link', href=config.get('feed_self_link', ''), rel='self', type='application/rss+xml')
    
    aggregation_date = SubElement(channel, 'lastBuildDate')
    aggregation_date.text = datetime.now().strftime("%a, %d %b %Y %H:%M:%S %z")

    # Add each group as an item
    for group in aggregated_items:
        item = SubElement(channel, 'item')

        item_title = SubElement(item, 'title')
        item_title.text = group[0]['title']

        item_description = SubElement(item, 'description')
        item_description.text = ' '.join([article['content'] for article in group])

        item_link = SubElement(item, 'link')
        item_link.text = group[0].get('link', 'https://github.com/fabriziosalmi/UglyFeed')

        pub_date = SubElement(item, 'pubDate')
        pub_date.text = datetime.now().strftime("%a, %d %b %Y %H:%M:%S %z")

    # Convert to string
    rough_string = tostring(rss, 'utf-8')
    reparsed = parseString(rough_string)
    pretty_string = reparsed.toprettyxml(indent="  ")

    # Ensure the output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Write to file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(pretty_string)

    print(f"RSS feed successfully generated and saved to {output_path}")

