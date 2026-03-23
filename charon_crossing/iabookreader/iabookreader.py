import sys
from uuid import uuid4

from lxml import etree
import json

class IABookReaderMetadata:
    def __init__(self, xml_file):
        self.xml_file = xml_file
        self.root = self.__read_xml()
        self.description = self.get_description()
        self.year = self.get_year()
        self.identifier = self.get_identifier()
        self.related_item = self.get_related_item()

    def __read_xml(self):
        tree = etree.parse(self.xml_file)
        return tree

    def get_description(self):
        items = self.root.xpath('//li/text()')
        all_values = [i.strip() for i in items]
        all_values.append(
            "Digitized Yearbook Collection is funded through the generosity of the Class of 1949. To support the Digitization Project, please contact Adelle Hedleston '88 at adelle-h@library.tamu.edu or (979)862-4574."
        )
        return all_values

    def get_year(self):
        return self.root.xpath('//year/text()')[0]

    def get_title(self):
        return self.root.xpath('//title/text()')[0]

    def get_identifier(self):
        return self.root.xpath('//identifier/text()')[0]

    def get_related_item(self):
        return self.root.xpath('//bookrecord/text()')[0]

    def get_rights(self):
        if int(self.year) < 1930:
            return "http://rightsstatements.org/vocab/NoC-US/1.0/"
        else:
            return "http://rightsstatements.org/vocab/InC/1.0/"

    def get_rights_details(self):
        if int(self.year) < 1930:
            return "No Copyright - United States"
        else:
            return "In Copyright"

    def build(self):
        return {
            "image": "",
            "label": f"{self.year} {self.get_title()}",
            "identifier": [
                {
                    "value": self.identifier,
                    "authority": "local"
                }
            ],
            "node_uuid": str(uuid4()),
            "format": "reformatted digital",
            "type": "Book",
            "title_alternative": self.get_title(),
            "digital_publisher": "Texas A&M University Libraries",
            "rights": self.get_rights(),
            "language": "eng",
            "ismemberof": "e777b54b-d183-467a-a57d-adbe9a9037bf",
            "description": self.description,
            "related_item": self.get_related_item(),
            "date_issued": self.get_year(),
            "content_type": ["Text", "StillImage"]
        }


if __name__ == "__main__":
    metadata = IABookReaderMetadata("/Users/mark.baggett/tamu-dc-labs/ia-bookreader-metadata/yb1976/yb1976_meta.xml")
    print(metadata.build())