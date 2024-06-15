import re
from docutils import nodes
from sphinx.transforms import SphinxTransform

 # Add custom images
# SHORTCODE_TO_IMAGE = {
#     '|:openmined1:|': '_static/images/openmined1.png',
#     '|:openmined2:|': '_static/images/openmined2.gif',
#     '|:openmined3:|': '_static/images/openmined3.gif',
#     '|:openmined4:|': '_static/images/openmined4.svg',
# }

def convert_shortcodes_in_text(text, shortcode_to_image):
    pattern = re.compile(r'(\|\:\w+?\:\|)')
    parts = pattern.split(text)
    result = []

    for part in parts:
        if part in shortcode_to_image:
            image_node = nodes.image(uri=shortcode_to_image[part], alt=part, classes=['custom-emoji'])
            result.append(image_node)
        else:
            result.append(nodes.Text(part))
    
    return result

def convert_shortcodes_to_nodes(node, shortcode_to_image):
    if isinstance(node, nodes.Text):
        new_nodes = convert_shortcodes_in_text(node.astext(), shortcode_to_image)
        for new_node in new_nodes:
            node.parent.insert(node.parent.index(node), new_node)
        node.parent.remove(node)
    elif isinstance(node, nodes.Element):
        for child in list(node.children):  # Use a copy of the list for safe iteration
            convert_shortcodes_to_nodes(child, shortcode_to_image)

class Persona(SphinxTransform):
    default_priority = 211

    def apply(self):
        # Retrieve the custom shortcode to image mapping from the configuration
        shortcode_to_image = self.app.config.html_theme_options.get('custom_shortcode_to_image', {})
        convert_shortcodes_to_nodes(self.document, shortcode_to_image)
