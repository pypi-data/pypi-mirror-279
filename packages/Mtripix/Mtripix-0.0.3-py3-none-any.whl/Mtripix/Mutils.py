import json
import numpy as np
import xml.etree.ElementTree as ET

class _Mtrans_():
    def __init(self):
        super().__init__()

    def is_contain_chinese(self, path):
        for char in path:
            if '\u4e00' <= char <= '\u9fff':
                return True
        return False
    def is_elements_all_num(self, lst):
        for elem in lst:
            if type(elem) not in [int]:
                return False
        return True
    def is_elements_all_str(self, lst):
        for elem in lst:
            if type(elem) not in [str]:
                return False
        return True
    def labels2dict(self, labels, idxs):
        assert (type(labels) == list or type(labels) == tuple), "labels必须为数组或列表格式"
        assert (type(idxs) == list or type(idxs) == tuple), "idxs必须为列表或数组格式"
        if (len(labels) != len(idxs)):
            print("标签名称和标签个数不对应！请检查。\n")
            exit()
        if (len(set(labels)) != len(labels)):
            print("标签名称有重复！请检查。\n")
            exit()
        if (len(set(idxs)) != len(idxs)):
            print("标签有重复！请检查。\n")
            exit()
        names = {}
        self.is_elements_all_num(idxs)
        self.is_elements_all_str(labels)
        for i in range(len(labels)):
            names[labels[i]] = idxs[i]
        return names
    def xyxy2xywh(self, xmin, ymin, xmax, ymax):
        """
        转换单个框到yolo格式
        """
        w = xmax - xmin
        h = ymax - ymin
        x = (xmin + xmax) / 2.0
        y = (ymin + ymax) / 2.0
        return (x, y, w, h)
    def xyxy2xywhn(self, xmin, ymin, xmax, ymax, W, H):
        """
        转换单个框到yolo格式
        """
        dw = 1. / W
        dh = 1. / H
        w = (xmax - xmin) * dw
        h = (ymax - ymin) * dh
        x = (xmin + xmax) * dw / 2.0
        y = (ymin + ymax) * dh / 2.0
        return (x, y, w, h)
    def xywh2xyxy(self, x_center, y_center, w, h, W, H):
        """
        转换单个框到yolo格式
        """
        x_center *= W
        y_center *= H
        w *= W
        h *= H
        xmin, xmax = int(x_center - W/2.), int(x_center + W/2.)
        ymin, ymax = int(y_center - H / 2.), int(y_center + H / 2.)
        return (xmin, ymin, xmax, ymax)
    def rotate(self, cx, cy, w, h, angle):
        angle = -angle  # 这里是图像坐标
        points = [[cx - w / 2, cy - h / 2], [cx + w / 2, cy - h / 2],
                  [cx + w / 2, cy + h / 2], [cx - w / 2, cy + h / 2]]
        newpoints = []
        if angle < 0:  # 逆时针
            angle = -angle
            for point in points:
                x, y = point
                newx = round((x - cx) * np.cos(angle) - (y - cy) * np.sin(angle) + cx, 1)
                newy = round((x - cx) * np.sin(angle) + (y - cy) * np.cos(angle) + cy, 1)
                newpoints.append([newx, newy])
        else:
            for point in points:
                x, y = point
                newx = round((x - cx) * np.cos(angle) + (y - cy) * np.sin(angle) + cx, 1)
                newy = round((y - cy) * np.cos(angle) - (x - cx) * np.sin(angle) + cy, 1)
                newpoints.append([newx, newy])
        return newpoints
    def xml2yolo(self,path_xml, path_txt, namedict):
        """
        :param path_xml: xml 标注文件地址
        :param path_txt: 保存的yolo格式文件地址
        :param namelist: 标签的名字与对应的label_id组成的字典
        """
        txt = open(path_txt, 'w')
        tree = ET.parse(path_xml)
        root = tree.getroot()
        size = root.find('size')
        W = int(size.find('width').text)
        H = int(size.find('height').text)
        if (W < 1 or H < 1):
            print("检查xml格式，标注错误，检查xml文件中width与height大小！！！\n")
            exit()
        for obj in root.iter('object'):
            cls = obj.find('name').text
            if cls not in namedict.keys():
                continue
            else:
                label = str(namedict[cls])
                xmlbox = obj.find('bndbox')
                xmin, xmax, ymin, ymax = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text),
                                          float(xmlbox.find('ymin').text), float(xmlbox.find('ymax').text))
                x, y, w, h = self.xyxy2xywhn(xmin, ymin, xmax, ymax, W, H)
                txt.write(label + " " + str(x) + " " + str(y) + " " + str(w) + " " + str(h) + "\n")
        txt.close()
        return 0
    def json2yolo(self, path_json, path_txt, namedict, mode="detection"):
        """
        :param path_xml: xml 标注文件地址
        :param path_txt: 保存的yolo格式文件地址
        :param namelist: 标签的名字与对应的label_id组成的字典
        """
        txt = open(path_txt, 'w')
        f = open(path_json, 'r')
        data = json.load(f)
        f.close()
        H = int(data["imageHeight"])
        W = int(data["imageWidth"])
        if (W < 1 or H < 1):
            print("检查xml格式，标注错误，检查xml文件中width与height大小！！！\n")
            txt.close()
            exit()
        shapes = data["shapes"]
        if mode == "segmentation":
            for shape in shapes:
                points = shape["points"]
                if shape["label"] in namedict.keys():
                    label = str(namedict[shape["label"]])
                    txt.write(label)
                    for point in points:
                        x = float(point[0]) / W
                        y = float(point[1]) / H
                        txt.write(" " + str(x) + " " + str(y))
                    txt.write("\n")
        elif mode == "detection":
            for shape in shapes:
                points = shape["points"]
                if shape["label"] in namedict.keys():
                    label = str(namedict[shape["label"]])
                    txt.write(label)
                    x_ = []
                    y_ = []
                    for point in points:
                        x_.append(float(point[0]))
                        y_.append(float(point[1]))
                    x_max, x_min = max(x_), min(x_)
                    y_max, y_min = max(y_), min(y_)
                    x, y, w, h = self.xyxy2xywhn(x_min, y_min, x_max, y_max, W, H)
                    txt.write(" " + str(x) + " " + str(y) + " " + str(w) + " " + str(h))
                    txt.write("\n")
        else:
            print("\n不存在当前的转换类型： " + mode)
            txt.close()
            exit()
        txt.close()
        return 0
    def xml2dota(self, path_xml, path_txt):
        """
        :param path_xml: xml 标注文件地址
        :param path_txt: 保存的yolo格式文件地址
        """
        txt = open(path_txt, 'w')
        tree = ET.parse(path_xml)
        root = tree.getroot()
        size = root.find('size')
        W = int(size.find('width').text)
        H = int(size.find('height').text)
        if (W < 1 or H < 1):
            print("检查xml格式，标注错误，检查xml文件中width与height大小！！！\n")
            txt.close()
            exit()
        for obj in root.iter('object'):
            difficult = obj.find('difficult').text
            if (obj.find('type').text == 'robndbox'):
                cls = obj.find('name').text
                xmlbox = obj.find('robndbox')
                cx, cy, w, h, angle = (float(xmlbox.find('cx').text), float(xmlbox.find('cy').text),
                                       float(xmlbox.find('w').text), float(xmlbox.find('h').text),
                                       float(xmlbox.find('angle').text))
                newpoints = self.rotate(cx, cy, w, h, angle)  # 计算旋转后的4个点坐标
            elif (obj.find('type').text == 'bndbox'):
                cls = obj.find('name').text
                xmlbox = obj.find('bndbox')
                xmin, ymin, xmax, ymax = (float(xmlbox.find('xmin').text), float(xmlbox.find('ymin').text),
                                          float(xmlbox.find('xmax').text), float(xmlbox.find('ymax').text))
                cx, cy, w, h = self.xyxy2xywh(xmin, ymin, xmax, ymax)
                newpoints = self.rotate(cx, cy, w, h, 0)  # 计算旋转后的4个点坐标
            newpoints = np.array(newpoints)
            newpoints = newpoints.astype(int)
            line = ''
            for point in newpoints:
                line += str(point[0]) + ' ' + str(point[1]) + ' '
            line += cls + ' ' + difficult +'\n'
            txt.write(line)
        txt.close()
        return 0
    def xml2yoloobb(self, path_xml, path_txt, namedict):
        """
        :param path_xml: xml 标注文件地址
        :param path_txt: 保存的yolo格式文件地址
        """
        txt = open(path_txt, 'w')
        tree = ET.parse(path_xml)
        root = tree.getroot()
        size = root.find('size')
        W = int(size.find('width').text)
        H = int(size.find('height').text)
        if (W < 1 or H < 1):
            print("检查xml格式，标注错误，检查xml文件中width与height大小！！！\n")
            txt.close()
            exit()
        for obj in root.iter('object'):
            cls = obj.find('name').text
            if cls not in namedict.keys():
                continue
            if (obj.find('type').text == 'robndbox'):
                xmlbox = obj.find('robndbox')
                cx, cy, w, h, angle = (float(xmlbox.find('cx').text), float(xmlbox.find('cy').text),
                                       float(xmlbox.find('w').text), float(xmlbox.find('h').text),
                                       float(xmlbox.find('angle').text))
                newpoints = self.rotate(cx, cy, w, h, angle)  # 计算旋转后的4个点坐标
            elif (obj.find('type').text == 'bndbox'):
                xmlbox = obj.find('bndbox')
                xmin, ymin, xmax, ymax = (float(xmlbox.find('xmin').text), float(xmlbox.find('ymin').text),
                                          float(xmlbox.find('xmax').text), float(xmlbox.find('ymax').text))
                cx, cy, w, h = self.xyxy2xywh(xmin, ymin, xmax, ymax)
                newpoints = self.rotate(cx, cy, w, h, 0)  # 计算旋转后的4个点坐标
            newpoints = np.array(newpoints)
            newpoints = newpoints.astype(int)
            line = str(namedict[cls]) + " "
            for point in newpoints:
                line += str(point[0]/W) + ' ' + str(point[1]/H) + ' '
            line += '\n'
            txt.write(line)
        txt.close()
        return 0





Mtrans = _Mtrans_()

