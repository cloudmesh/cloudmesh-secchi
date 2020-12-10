import os
import io
import pandas as pd
import tensorflow as tf
import sys

sys.path.append("../../models/research")

from PIL import Image
from cloudmesh.secchi.tensorflow.utils_tf import dataset_util
from collections import namedtuple, OrderedDict
from cloudmesh.common.util import path_expand


class GenTF:

    def __init__(self, str):

        if str == 'train':
            self.csv_input = os.path.join(path_expand('~/.cloudmesh/secchi/annotations'), 'train_labels.csv')
        else:
            self.csv_input = os.path.join(path_expand('~/.cloudmesh/secchi/annotations'), 'test_labels.csv')

        self.img_path = os.path.join(path_expand('~/.cloudmesh/secchi/images'), str)
        self.output_path = os.path.join(path_expand('~/.cloudmesh/secchi/annotations'), f"{str}.record")

        self.label = 'disc'

    def create(self):

        writer = tf.io.TFRecordWriter(self.output_path)
        print("csv_input: ", self.csv_input)
        examples = pd.read_csv(self.csv_input)
        grouped = self.split(examples, 'filename')
        for group in grouped:
            tf_example = self.create_tf_example(group, self.img_path)
            writer.write(tf_example.SerializeToString())

        writer.close()
        print('Successfully created the TFRecords: {}'.format(self.output_path))

    def class_text_to_int(self, row_label):

        if row_label == self.label:  # 'ship':
            return 1
        else:
            None

    def split(self, df, group):
        data = namedtuple('data', ['filename', 'object'])
        gb = df.groupby(group)
        return [data(filename, gb.get_group(x)) for filename, x in zip(gb.groups.keys(), gb.groups)]

    def create_tf_example(self, group, path):
        with tf.io.gfile.GFile(os.path.join(path, '{}'.format(group.filename)), 'rb') as fid:
            encoded_jpg = fid.read()
        encoded_jpg_io = io.BytesIO(encoded_jpg)
        image = Image.open(encoded_jpg_io)
        width, height = image.size

        filename = group.filename.encode('utf8')
        image_format = b'jpg'
        xmins = []
        xmaxs = []
        ymins = []
        ymaxs = []
        classes_text = []
        classes = []

        for index, row in group.object.iterrows():
            xmins.append(row['xmin'] / width)
            xmaxs.append(row['xmax'] / width)
            ymins.append(row['ymin'] / height)
            ymaxs.append(row['ymax'] / height)
            classes_text.append(row['class'].encode('utf8'))
            classes.append(self.class_text_to_int(row['class']))

        tf_example = tf.train.Example(features=tf.train.Features(feature={
            'image/height': dataset_util.int64_feature(height),
            'image/width': dataset_util.int64_feature(width),
            'image/filename': dataset_util.bytes_feature(filename),
            'image/source_id': dataset_util.bytes_feature(filename),
            'image/encoded': dataset_util.bytes_feature(encoded_jpg),
            'image/format': dataset_util.bytes_feature(image_format),
            'image/object/bbox/xmin': dataset_util.float_list_feature(xmins),
            'image/object/bbox/xmax': dataset_util.float_list_feature(xmaxs),
            'image/object/bbox/ymin': dataset_util.float_list_feature(ymins),
            'image/object/bbox/ymax': dataset_util.float_list_feature(ymaxs),
            'image/object/class/text': dataset_util.bytes_list_feature(classes_text),
            'image/object/class/label': dataset_util.int64_list_feature(classes),
        }))
        return tf_example
