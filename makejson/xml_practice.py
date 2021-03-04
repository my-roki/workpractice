# from xml.etree import ElementTree
#
# with open("blackolive_xml.xml",'r') as f:
#     str_xml = f.read()
#
# # print(str_xml)
# root_element = ElementTree.fromstring(str_xml) # 문자열에서 XML을 파싱합니다
#
# file = []
# iter_element = root_element.iter(tag="annotations") # anotations태그 iterator를 가져옵니다
#
# # print(iter_element)
#
#
#
# for element in iter_element:  # annotations 태그를 순회합니다
#     a = {}
#     a['type'] = "bbox"
#     a['copyright'] =  "seadronix corp."
#     a['date'] = element.find("dumped").text
#     file.append(a)  # 동물리스트에 동물정보를 저장합니다
#     print(annotations)  # 결과를 출력한다

import json
import xml.etree.ElementTree as ET

tree = ET.parse('blackolive_data/blackolive_xml(1).xml')
root = tree.getroot()

img_cnt = root.findall("image")
print(len(img_cnt))
#
# box_cnt = root.findall("image")[0]
# print(len(box_cnt))
#
# image = root.findall("image")[0].attrib
# print(image)
# print(len(image))
#
# box = root.findall("image")[0].findall("box")[0].attrib
# print(box)
# print(len(box))
#
# for i in range(0,len(img_cnt)):
#     image = root.findall("image")[i].attrib
#     del image['id']
#     print(image)


for i in range(0, len(img_cnt)):  # image 에 들어갈 value 값
    image = root.findall("image")[i].attrib
    del image['id']
    image['file_name'] = image.pop('name')
    image['width'] = image.pop('width')
    image['height'] = image.pop('height')
    # print(image)

    file = []
    box_cnt = root.findall("image")[i]
    for j in range(0, len(box_cnt)):  # annotations 에 들어갈 value 값
        box = root.findall("image")[i].findall("box")[j].attrib
        box['id'] = j  # xml에서 작업 결과 순서
        box['category_id'] = i + 1  # image 순서 번호
        box['xmin'] = box.pop('xtl')
        box['ymin'] = box.pop('ytl')
        box['width'] = float(box.get('xbr')) - float(box.get('xmin'))
        box['height'] = float(box.get('ybr')) - float(box.get('ymin'))
        del box['label'], box['occluded'], box['z_order'], box['xbr'], box['ybr']  # 필요없는 항목 삭제

        file.insert(j, box)
        # print(box)

    result = {}
    result['type'] = "bbox"
    result['copyright'] = "seadronix corp."
    result['date'] = root.find("meta").findtext("dumped")
    result['verification'] = "false"
    result['image'] = root.findall("image")[i].attrib
    result['annotations'] = file

    print(result)

# box = [x.find("box").attrib for x in image]
# print(json.dumps(box, indent="\t"))


# a.find("box").text
#
# box = [x.find("box").attrib for x in a]
#
# print(json.dumps(box, indent="\t"))


# b = root.find("meta").findtext("dumped")
# print(b)
