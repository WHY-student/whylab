import os
import json
import xml.etree.ElementTree as ET
from tqdm import tqdm


def create_dior_xml(json_file, output_dir):
    # 读取 labelme JSON 文件
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 提取图像信息
    image_name = data['imagePath']
    image_width = data['imageWidth']
    image_height = data['imageHeight']

    # 创建 XML 的根节点
    annotation = ET.Element('annotation')

    # 添加 folder 和 filename
    folder = ET.SubElement(annotation, 'folder')
    folder.text = 'DIOR'
    filename = ET.SubElement(annotation, 'filename')
    filename.text = image_name

    # 添加 size 信息
    size = ET.SubElement(annotation, 'size')
    width = ET.SubElement(size, 'width')
    width.text = str(image_width)
    height = ET.SubElement(size, 'height')
    height.text = str(image_height)
    depth = ET.SubElement(size, 'depth')
    depth.text = '3'  # 假设为 RGB 图像

    # 遍历标注对象
    for shape in data['shapes']:
        label = shape['label']
        points = shape['points']

        # 计算边界框
        xmin = int(min(point[0] for point in points))
        ymin = int(min(point[1] for point in points))
        xmax = int(max(point[0] for point in points))
        ymax = int(max(point[1] for point in points))

        # 创建 object 节点
        obj = ET.SubElement(annotation, 'object')
        name = ET.SubElement(obj, 'name')
        name.text = label
        pose = ET.SubElement(obj, 'pose')
        pose.text = 'Unspecified'
        truncated = ET.SubElement(obj, 'truncated')
        truncated.text = '0'
        difficult = ET.SubElement(obj, 'difficult')
        difficult.text = '0'

        # 添加 bndbox 信息
        bndbox = ET.SubElement(obj, 'bndbox')
        ET.SubElement(bndbox, 'xmin').text = str(xmin)
        ET.SubElement(bndbox, 'ymin').text = str(ymin)
        ET.SubElement(bndbox, 'xmax').text = str(xmax)
        ET.SubElement(bndbox, 'ymax').text = str(ymax)

    # 保存为 XML 文件
    tree = ET.ElementTree(annotation)
    output_file = os.path.join(output_dir, os.path.splitext(os.path.basename(json_file))[0] + '.xml')
    tree.write(output_file, encoding='utf-8', xml_declaration=True)
    # print(f"Saved XML to {output_file}")

def labelme2xml(input_json_dir: str, output_xml_dir: str):
    """
    input_json_dir: 需要修改的json文件的目录
    output_xml_dir: xml文件输出的目录
    """
    os.makedirs(output_xml_dir, exist_ok=True)
    for json_file in tqdm(os.listdir(input_json_dir)):
        if json_file.endswith('.json'):
            create_dior_xml(os.path.join(input_json_dir, json_file), output_xml_dir)
