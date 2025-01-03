import os
import json
import xml.etree.ElementTree as ET
from tqdm import tqdm

def parse_voc_xml(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    file_name = root.find('filename').text
    size = root.find('size')
    width = int(size.find('width').text)
    height = int(size.find('height').text)
    depth = int(size.find('depth').text)

    annotations = []
    for obj in root.findall('object'):
        name = obj.find('name').text
        bndbox = obj.find('bndbox')
        xmin = int(bndbox.find('xmin').text)
        ymin = int(bndbox.find('ymin').text)
        xmax = int(bndbox.find('xmax').text)
        ymax = int(bndbox.find('ymax').text)

        annotations.append({
            'category': name,
            'bbox': [xmin, ymin, xmax - xmin, ymax - ymin],
            'area': (xmax - xmin) * (ymax - ymin),
            'iscrowd': 0
        })

    return file_name, width, height, annotations

def voc2coco(voc_dir:str, save_path:str):
    """
    voc: the train/val xml dir, make sure that you split the dataset manually.
    save_path: the output path of json file.
    
    """
    categories = []
    category_set = set()
    images = []
    annotations = []
    annotation_id = 1

    xml_files = [f for f in os.listdir(voc_dir) if f.endswith('.xml')]
    for xml_file in tqdm(xml_files, desc="Processing VOC files"):
        xml_path = os.path.join(voc_dir, xml_file)
        file_name, width, height, objs = parse_voc_xml(xml_path)

        image_id = len(images) + 1
        images.append({
            'id': image_id,
            'file_name': file_name,
            'width': width,
            'height': height
        })

        for obj in objs:
            category_name = obj['category']
            if category_name not in category_set:
                category_set.add(category_name)
                categories.append({
                    'id': len(categories) + 1,
                    'name': category_name,
                    'supercategory': 'none'
                })

            category_id = next(cat['id'] for cat in categories if cat['name'] == category_name)
            annotations.append({
                'id': annotation_id,
                'image_id': image_id,
                'category_id': category_id,
                'bbox': obj['bbox'],
                'area': obj['area'],
                'iscrowd': obj['iscrowd']
            })
            annotation_id += 1

    coco_format = {
        'images': images,
        'annotations': annotations,
        'categories': categories
    }

    with open(save_path, 'w') as f:
        json.dump(coco_format, f, indent=4)

    print(f"COCO JSON saved to {save_path}")

# 使用示例
# voc_dir = 'path_to_voc_annotations'  # VOC XML 文件所在目录
# save_path = 'output_coco.json'       # 输出 COCO JSON 文件路径
# voc_to_coco(voc_dir, save_path)
