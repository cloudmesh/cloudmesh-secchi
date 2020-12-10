""" usage: partition_dataset.py [-h] [-i IMAGEDIR] [-o OUTPUTDIR] [-r RATIO] [-x]

Partition dataset of images into training and testing sets

optional arguments:
  -h, --help            show this help message and exit
  -i IMAGEDIR, --imageDir IMAGEDIR
                        Path to the folder where the image dataset is stored. If not specified, the CWD will be used.
  -o OUTPUTDIR, --outputDir OUTPUTDIR
                        Path to the output folder where the train and test dirs should be created. Defaults to the same directory as IMAGEDIR.
  -r RATIO, --ratio RATIO
                        The ratio of the number of test images over the total number of images. The default is 0.1.
  -x, --xml             Set this flag if you want the xml annotation files to be processed and copied over.
"""
import os
import re
import shutil
from PIL import Image
from shutil import copyfile
import argparse
import glob
import math
import random
import xml.etree.ElementTree as ET

from cloudmesh.common.Shell import Shell
from cloudmesh.common.util import path_expand


def iterate_dir(source, dest, ratio, copy_xml=True):
    print("ratio: ", type(ratio))
    train_dir = os.path.join(dest, 'train')
    test_dir = os.path.join(dest, 'test')

    if not os.path.exists(train_dir):
        os.makedirs(train_dir)
    if not os.path.exists(test_dir):
        os.makedirs(test_dir)

    images = [f for f in os.listdir(source)
              if re.search(r'([a-zA-Z0-9\s_\\.\-\(\):])+(.jpg|.jpeg|.png)$', f)]

    num_images = len(images)
    print("num_images", num_images)
    num_test_images = math.ceil(ratio * num_images)

    for i in range(num_test_images):
        idx = random.randint(0, len(images) - 1)
        filename = images[idx]
        copyfile(os.path.join(source, filename),
                 os.path.join(test_dir, filename))
        if copy_xml:
            xml_filename = os.path.splitext(filename)[0] + '.xml'
            copyfile(os.path.join(source, xml_filename),
                     os.path.join(test_dir, xml_filename))
        images.remove(images[idx])

    for filename in images:
        copyfile(os.path.join(source, filename),
                 os.path.join(train_dir, filename))
        if copy_xml:
            xml_filename = os.path.splitext(filename)[0] + '.xml'
            copyfile(os.path.join(source, xml_filename),
                     os.path.join(train_dir, xml_filename))


class PartitionDataset:
    outputDir = path_expand('~/.cloudmesh/secchi/images')

    def __init__(self, inputDir=None, ratio=0.1):
        self.imageDir = inputDir
        self.ratio = ratio

    def run(self):
        if not os.path.exists(self.outputDir):
            Shell.mkdir(self.outputDir)
        iterate_dir(self.imageDir, self.outputDir, self.ratio)

    def delete(self):
        Shell.rmdir(self.outputDir)
