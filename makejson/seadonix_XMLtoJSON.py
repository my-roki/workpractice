import os
import json
import xml.etree.ElementTree as ET

##############################################

path_dir = r"D:\workpractice\makejson\blackolive_data"
save_dir = r"D:\workpractice\makejson\save_data"

###############################################

# print(os.listdir(path_dir))

# for m in os.listdir(path_dir):
#     print(m)

for name in os.listdir(path_dir):
    tree = ET.parse(os.path.join(path_dir, name))
    root = tree.getroot()

    img_cnt = root.findall("image")
    # print(len(img_cnt))
    for i in range(0, len(img_cnt)):  # image 에 들어갈 value 값
        image = root.findall("image")[i].attrib
        image['file_name'] = image.pop('name')
        image['width'] = float(image.pop('width'))
        image['height'] = float(image.pop('height'))
        del image['id']  # 필요없는 항목 삭제
        # print(image)

        file = []
        box_cnt = root.findall("image")[i]
        for j in range(0, len(box_cnt)):  # annotations 에 들어갈 value 값
            box = root.findall("image")[i].findall("box")[j].attrib
            box['id'] = j  # xml 파일에서 작업 결과 순서 번호
            box['category_id'] = i + 1  # image 순서 번호
            box['xmin'] = float(box.pop('xtl'))
            box['ymin'] = float(box.pop('ytl'))
            box['width'] = float(box.get('xbr')) - float(box.get('xmin'))
            box['height'] = float(box.get('ybr')) - float(box.get('ymin'))
            del box['label'], box['occluded'], box['z_order'], box['xbr'], box['ybr']  # 필요없는 항목 삭제

            file.insert(j, box)
            # print(box)

        result = {}
        result['type'] = "bbox"
        result['copyright'] = "seadronix corp."
        result['date'] = root.find("meta").findtext("dumped")
        result['verification'] = False
        result['image'] = root.findall("image")[i].attrib
        result['annotations'] = file

        with open(os.path.join(save_dir, name + str(i) + ".json"), 'w', encoding='utf-8') as make_file:
            json.dump(result, make_file, indent="\t")
    #     print(result)
    # print()