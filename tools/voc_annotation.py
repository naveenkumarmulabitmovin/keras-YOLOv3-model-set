#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import os, argparse
from os import getcwd

sets=[('2007', 'train'), ('2007', 'val'), ('2007', 'test'), ('2012', 'train'), ('2012', 'val')]
classes = ["aeroplane", "bicycle", "bird", "boat", "bottle", "bus", "car", "cat", "chair", "cow", "diningtable", "dog", "horse", "motorbike", "person", "pottedplant", "sheep", "sofa", "train", "tvmonitor"]


def convert_annotation(dataset_path, year, image_id, list_file):
    in_file = open('%s/VOC%s/Annotations/%s.xml'%(dataset_path, year, image_id))
    tree=ET.parse(in_file)
    root = tree.getroot()

    for obj in root.iter('object'):
        difficult = obj.find('difficult').text
        cls = obj.find('name').text
        if cls not in classes or int(difficult)==1:
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (int(xmlbox.find('xmin').text), int(xmlbox.find('ymin').text), int(xmlbox.find('xmax').text), int(xmlbox.find('ymax').text))
        list_file.write(" " + ",".join([str(a) for a in b]) + ',' + str(cls_id))


parser = argparse.ArgumentParser()
parser.add_argument('--dataset_path', type=str, help='path to PascalVOC dataset, default is ./VOCdevkit', default=getcwd()+'/VOCdevkit')
parser.add_argument('--output_path', type=str,  help='output path for generated annotation txt files, default is ./', default='./')
args = parser.parse_args()

for year, image_set in sets:
    image_ids = open('%s/VOC%s/ImageSets/Main/%s.txt'%(args.dataset_path, year, image_set)).read().strip().split()
    list_file = open('%s/%s_%s.txt'%(args.output_path, year, image_set), 'w')
    for image_id in image_ids:
        list_file.write('%s/VOC%s/JPEGImages/%s.jpg'%(args.dataset_path, year, image_id))
        convert_annotation(args.dataset_path, year, image_id, list_file)
        list_file.write('\n')
    list_file.close()