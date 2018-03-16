import os
from zipfile import ZipFile
from uuid import uuid4
from xml.dom.minidom import parseString
from xml.etree.ElementTree import Element, SubElement, tostring
from random import randrange


def prettify(elem):
    rough_string = tostring(elem, 'unicode')
    reparsed = parseString(rough_string)
    return reparsed.toprettyxml()


def build_random_xml():
    root = Element('root')
    name_params = {'name': 'id', 'value': str(uuid4())}
    SubElement(root, 'var', name_params)
    level_params = {'name': 'level', 'value': str(randrange(100))}
    SubElement(root, 'var', level_params)
    items = SubElement(root, 'objects')
    for i in range(randrange(10)):
        SubElement(items, 'object', {'name': str(uuid4())})
    return prettify(root)


def create_zip(zip_name, zip_num):
    with open(zip_name, 'wb') as f:
        with ZipFile(f, 'w') as zip_file:
            for i in range(1, 101):
                filename = '{}_{}.xml'.format(zip_num, i)
                with open(filename, 'w') as xml_file:
                    xml_file.writelines(build_random_xml())
                zip_file.write(xml_file.name)
                os.remove(xml_file.name)
