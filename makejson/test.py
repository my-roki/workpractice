import json
import xmltodict

with open(r'blackolive_data/blackolive_xml.xml', 'r') as f:
    xmlString = f.read()

print("xml input (blackolive_xml.xml):")
print(xmlString)

jsonString = json.dumps(xmltodict.parse(xmlString), indent=4)

print("\nJSON output(output.json):")
print(jsonString)

with open("xml_to_json.json", 'w') as f:
    f.write(jsonString)


with open('xml_to_json.json', 'r') as f:
    jsonString = f.read()

print('JSON input (xml_to_json.json):')
print(jsonString)

xmlString = xmltodict.unparse(json.loads(jsonString), pretty=True)

print('\nXML output(json_to_xml.xml):')
print(xmlString)

with open('json_to_xml.xml', 'w') as f:
    f.write(xmlString)
