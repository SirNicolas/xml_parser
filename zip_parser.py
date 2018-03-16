import os
from zipfile import ZipFile
import xml.etree.ElementTree as etree


def parse_zip(zip_name, remove_zip=False):
    header_data = []
    body_data = []
    with ZipFile(zip_name, 'r') as file:
        for name in file.namelist():
            xml_id = None
            xml_level = None
            f = file.open(name)
            root = etree.fromstring(f.read())
            for child in root.iter('var'):
                if child.attrib['name'] == 'id':
                    xml_id = child.attrib['value']
                else:
                    xml_level = child.attrib['value']
            header_data.append((xml_id, xml_level))
            for child in root.iter('object'):
                body_data.append((xml_id, child.attrib['name']))

    if remove_zip:
        os.remove(zip_name)

    return header_data, body_data
