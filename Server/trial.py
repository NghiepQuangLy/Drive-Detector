import sys
from xml.etree import ElementTree as ET

html = ET.Element('html')
body = ET.Element('body')
html.append(body)
div = ET.Element('div', attrib={'class': 'foo'})
body.append(div)
span = ET.Element('span', attrib={'class': 'bar'})
div.append(span)
span.text = "Hello World"


ET.ElementTree(html).write(sys.stdout, encoding='utf8',
                           method='html')
