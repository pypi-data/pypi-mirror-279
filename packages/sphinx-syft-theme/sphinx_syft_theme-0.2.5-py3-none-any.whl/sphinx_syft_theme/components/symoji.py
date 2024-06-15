import re
from docutils import nodes
from sphinx.transforms import SphinxTransform
from docutils import nodes
from docutils.utils import new_document
from sphinx.util.docutils import LoggingReporter

SHORTCODE_TO_UNICODE = {
    '|:man_technologist:|': '👨‍💻',
    '|:man_technologist_dark_skin_tone:|': '👨🏿‍💻',
    '|:man_technologist_light_skin_tone:|': '👨🏻‍💻',
    '|:man_technologist_medium_dark_skin_tone:|': '👨🏾‍💻',
    '|:man_technologist_medium_light_skin_tone:|': '👨🏼‍💻',
    '|:man_technologist_medium_skin_tone:|': '👨🏽‍💻',
    '|:woman_technologist:|': '👩‍💻',
    '|:woman_technologist_dark_skin_tone:|': '👩🏿‍💻',
    '|:woman_technologist_light_skin_tone:|': '👩🏻‍💻',
    '|:woman_technologist_medium_dark_skin_tone:|': '👩🏾‍💻',
    '|:woman_technologist_medium_light_skin_tone:|': '👩🏼‍💻',
    '|:woman_technologist_medium_skin_tone:|': '👩🏽‍💻',
}

 # Add custom images
SHORTCODE_TO_IMAGE = {
    '|:openmined1:|': '_static/images/openmined1.png',
    '|:openmined2:|': '_static/images/openmined2.gif',
    '|:openmined4:|': '_static/images/openmined4.svg',
}

def convert_shortcodes_to_emojis(text):
    pattern = re.compile(r'(\|\:\w+?\:\|)')
    return pattern.sub(lambda match: SHORTCODE_TO_UNICODE.get(match.group(1), match.group(1)), text)

def recursive_convert_shortcodes_to_emojis(item):
    if isinstance(item, str):
        return convert_shortcodes_to_emojis(item)
    elif isinstance(item, list):
        return [recursive_convert_shortcodes_to_emojis(sub_item) for sub_item in item]
    elif isinstance(item, dict):
        return {key: recursive_convert_shortcodes_to_emojis(value) for key, value in item.items()}
    return item

# Define  
def convert_shortcodes_to_nodes(text):
    pattern = re.compile(r'(\|\:\w+?\:\|)')
    parts = pattern.split(text)
    result = []

    for part in parts:
        if part in SHORTCODE_TO_UNICODE:
            result.append(nodes.Text(SHORTCODE_TO_UNICODE[part]))
        elif part in SHORTCODE_TO_IMAGE:
            image_node = nodes.image(uri=SHORTCODE_TO_IMAGE[part], alt=part, classes=['custom-emoji'])
            result.append(image_node)
        else:
            result.append(nodes.Text(part))
    
    return result

def recursive_convert_shortcodes_to_emojis(node):
    if isinstance(node, nodes.Text):
        new_nodes = convert_shortcodes_to_nodes(node.astext())
        node.parent.replace(node, new_nodes)
    elif isinstance(node, nodes.Element):
        for child in node.children:
            recursive_convert_shortcodes_to_emojis(child)

# Define symoji class
class Symoji(SphinxTransform):
    default_priority = 211

    def apply(self):
        recursive_convert_shortcodes_to_emojis(self.document)
