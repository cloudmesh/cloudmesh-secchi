# To run model

## Prerequisite

* Python 3.6
* Tensorflow 1.14
* Pillow
* lxml
* matplotlib
* opencv
* cython

## Installation

Activate python virtual environment before installation.

```
pip install cloudmesh-cmd5
pip install cloudmesh-sys
cms sys command generate secchi
git pull https://github.com/cloudmesh/cloudmesh-secchi.git

```

## Command line execution

### Training an image dataset

#### Image Dataset and annotation file

* Create annotaion xml file for all the images using labelImg. Image file name 
  and corresponding xml file name must be same.

* All image and xml file must be placed in one folder.

#### Partition dataset into test and train

* Run command to split dataset into test and train. Default ration is 10%.

```   

# cms secchi create partitiondataset [INPUT_IMAGE_DIR] [--ratio=0.2]
cms secchi partitiondataset '~\Desktop\Img' --ratio=0.2

```

#### Prepare training data

* This step converts image file and  xml files into TFRecord which is uses in 
  training.


```

secchi prep --training

```

#### Download pretrained model(In Progress)


#### Start model training(In Progress) 


### Prediction


#### Upload video file to src folder through cms command for prediction

```
cms secchi upload '~/Desktop/file.mp4' --predict
```

#### Run predict through cms command

```
cms secchi run --predict
```

To quit press 'q'

#### Get the graph output

```

cms secchi show graph

```

#### Predict Screen and Graph

Example of prediction video and graph is shown:

![Output Graph](image/mygraph.png) 

![Predictor Output Image](image/Predictor_Image.png)