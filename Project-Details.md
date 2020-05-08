# Project Details

This program contains new programs which are created to integrate cloudmesh
and tensorflow and manage TF utilities. Thare are object detection utilities
from tensorflow which are used to perform object detection on video.

3 main programs:

* cloudmesh/secchi/command/secchi.py - Main program to integrate cloudmesh with
  other TF programes

* cloudmesh/secchi/video.py - This class manages file operations on video file
  like upload, delete, remove files etc.

* cloudmesh/secchi/tensorflow/predict.py - Uses openCV and TF to manipulate 
  video frame and apply predcitions on video.

## Details about prediction

### Tensorflow Utilities (include source)

/annotations/label_map.pbtxt - This file is updated for disc item. Since it is
just one item which needs to be detected, this file has one item as disc.

/config/ssd_inception_v2_coco.config - This is the config file for fine tuning
training and prediction. This file provides training configurations e.g. batch 
size, optimizer, Feature extractor, box predictoe, loss etc.(source) 

/trained-inference-graphs - This directory contains trained model files which 
are used to run prediction. These are checkpoint files created after training
is completed.

/utils_tf - This directory contains object detection utilities required to run
prediction. (source) 

### 

## Steps to train on new videos

### Installation of prerequisites

Trainging requires installation for few softwares which are used by tensorflow.

```
cms secchi run --setup
```

This command install tensorflow models in .cloudmesh/secchi/models and protobuf 
in .cloudmesh/secchi/Protobuf directory in users home directory.

Add path '.cloudmesh/secchi/Protobuf' to path environment variable.

In new terminal, cd into directory '.cloudmesh/secchi/models/research' and run command:

For Linux:

```
# From within .cloudmesh/secchi/models/research/
protoc object_detection/protos/*.proto --python_out=.
```

For windows, command is:

```
# From within .cloudmesh/secchi/models/research/
for /f %i in ('dir /b object_detection\protos\*.proto') do protoc object_detection\protos\%i --python_out=.
```

Installation of tensorflow models and utilities, run command:


```
# From within .cloudmesh/secchi/models/research/
pip install .
```

Add '.cloudmesh/secchi/models/research/slim' variable to PYTHONPATH.

Installation of pre-trained model is required to train secchi image on top of it
for better performance of model. Current model is trained on 'ssd_inception_v2_coco'
model which can be downloaded from this [link](http://download.tensorflow.org/models/object_detection/ssd_inception_v2_coco_2018_01_28.tar.gz) 

Unzip the files and pace them under '.cloudmesh/secchi/pre-trained-model' directory.

### Get input video

### Create frame and annoatate images. (use program abc.py)

video class has a method imageCapture to create frame from video and save it 
in directory. It takes video location as input parameter and generates multiple
image files in output directory.

Once images are created, annotation of disc on each file can be achieved by 
LabelImg tool. This tool creates a corresponding xml file for each image with
annotation details about disc.

Annotated xml file must have same name as image file and must be stored in the
same directory.

### Partition dataset

Location of directory of image and annotated xml files can be partitioned into
training and validation set by using below commands. 

```
cms secchi create partitiondataset [INPUTDIR] [--ratio=0.2]
``` 

Here INPUTDIR is the directory with image and corresponding annotation files.

### generate_tf_record 

Run the command to generate TF record for the images.

```
cms secchi prep --training
```

This command creates two record files, one for training, test.record, and one for 
validation, train.record under '.cloudmesh/secchi/annotations' directory.

### Update config file

Config file can be downloaded from [here](https://github.com/tensorflow/models/blob/master/research/object_detection/samples/configs/ssd_inception_v2_coco.config).

Once downloaded, it requires update to ensure model executes training properly.

```
model {
    ssd {
        num_classes: 1 # Set this to 1 as we have just one class.
        box_coder {
            faster_rcnn_box_coder {
                y_scale: 10.0
                x_scale: 10.0
                height_scale: 5.0
                width_scale: 5.0
            }
        }
```

```
train_config: {
    batch_size: 12 # Increase/Decrease this value depending on the available memory (Higher values require more memory and vice-versa)
    optimizer {
        rms_prop_optimizer: {
            learning_rate: {
                exponential_decay_learning_rate {
                    initial_learning_rate: 0.004
                    decay_steps: 800720
                    decay_factor: 0.95
                }
            }
            momentum_optimizer_value: 0.9
            decay: 0.9
            epsilon: 1.0
        }

```

```
fine_tune_checkpoint: "pre-trained-model/model.ckpt" # Path to extracted files of pre-trained
```

```
train_input_reader: {
    tf_record_input_reader {
        input_path: "annotations/train.record" # Path to training TFRecord file
    }
    label_map_path: "annotations/label_map.pbtxt" # Path to label map file
}

```

```
eval_config: {
    
    num_examples: 8000 	# Set this to the number of images in ].cloudmesh\secchi\images\train'
    # Note: The below line limits the evaluation process to 10 evaluations.
    # Remove the below line to evaluate indefinitely.
    max_evals: 10
}
```

```
eval_input_reader: {
    tf_record_input_reader {
        input_path: "annotations/test.record" # Path to testing TFRecord
    }
    label_map_path: "annotations/label_map.pbtxt" # Path to label map file
    shuffle: false
    num_readers: 1
}
```

### Train model on images

To start training, run command:

```
cms secchi run --training
```

### Save model.ckpt checkpoitnt file for prediction

While the evaluation process is running, it will periodically (every 300 
sec by default) check and use the latest training/model.ckpt-* checkpoint 
files to evaluate the performance of the model.

Once we acieve desired loss, we can choose the latest checkpoint file and
use it in prediction.

