######## Video Object Detection Using Tensorflow-trained Classifier #########
#
# Author: Divyanshu Mishra
# Date: 3/20/2020
# Description:
# This program uses a TensorFlow-trained classifier to perform object detection.
# It loads the classifier and uses it to perform object detection on a video.
# It draws boxes, scores, and labels around the objects of interest in each
# frame of the video.

## Some of the code is copied from Google's example at
## https://github.com/tensorflow/models/blob/master/research/object_detection/object_detection_tutorial.ipynb

## and some is copied from Dat Tran's example at
## https://github.com/datitran/object_detector_app/blob/master/object_detection_app.py

## There are modifications made to this program for requirement.

# Import packages
import os
import cv2
import numpy as np
import tensorflow as tf
import sys
import matplotlib.pyplot as plt
from cloudmesh.common.util import path_expand


# This is needed since the notebook is stored in the object_detection folder.
#sys.path.append("")

# Import utilites
#from object_detection.utils import label_map_util
#from utils_tf import label_map_util
from cloudmesh.secchi.tensorflow.utils_tf import label_map_util
from cloudmesh.secchi.tensorflow.utils_tf import visualization_utils as vis_util
#from object_detection.utils import visualization_utils as vis_util


class Predict:
    # Name of the directory containing the object detection module we're using
    MODEL_NAME = 'trained-inference-graphs'
    #VIDEO_NAME = 'Yi-Site1.mp4'
    # Grab path to current working directory
    ABS_PATH = os.path.abspath(__file__)
    CWD_PATH = os.path.dirname(ABS_PATH)
    VIDEO_PATH = path_expand("~/.cloudmesh/secchi")


    # Path to frozen detection graph .pb file, which contains the model that is used
    # for object detection.
    PATH_TO_CKPT = os.path.join(CWD_PATH,MODEL_NAME,'frozen_inference_graph.pb')
    # PATH_TO_CKPT = "C:\\Users\\dmall\\cm\\TensorFlow\\workspace\\training_demo" \
    #                "\\trained-inference-graphs\\output_inference_graph_v1.pb"
    # Path to label map file
    #PATH_TO_LABELS = os.path.join(CWD_PATH,'training','labelmap.pbtxt')
    PATH_TO_LABELS = os.path.join(CWD_PATH,'annotations','label_map.pbtxt')



    # Number of classes the object detector can identify
    NUM_CLASSES = 1
    scaling_factorx = 0.5
    scaling_factory = 0.5
    SCORES = []
    COUNTER = 0
    TIME_STAMP = []

    def __init__(self, video):
        self.VIDEO_NAME = video

    def run(self):
        # Load the label map.
        # Label maps map indices to category names, so that when our convolution
        # network predicts `5`, we know that this corresponds to `king`.
        # Here we use internal utility functions, but anything that returns a
        # dictionary mapping integers to appropriate string labels would be fine
        label_map = label_map_util.load_labelmap(self.PATH_TO_LABELS)
        categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=self.NUM_CLASSES,
                                                                    use_display_name=True)
        category_index = label_map_util.create_category_index(categories)

        # Load the Tensorflow model into memory.
        # Path to video
        #PATH_TO_VIDEO = os.path.join(self.CWD_PATH, self.VIDEO_NAME)
        PATH_TO_VIDEO = os.path.join(self.VIDEO_PATH, self.VIDEO_NAME)

        detection_graph = tf.Graph()
        with detection_graph.as_default():
            od_graph_def = tf.compat.v1.GraphDef()
            with tf.io.gfile.GFile(self.PATH_TO_CKPT, 'rb') as fid:
                serialized_graph = fid.read()
                od_graph_def.ParseFromString(serialized_graph)
                tf.import_graph_def(od_graph_def, name='')

            sess = tf.compat.v1.Session(graph=detection_graph)

        # Define input and output tensors (i.e. data) for the object detection classifier

        # Input tensor is the image
        image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')

        # Output tensors are the detection boxes, scores, and classes
        # Each box represents a part of the image where a particular object was detected
        detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')

        # Each score represents level of confidence for each of the objects.
        # The score is shown on the result image, together with the class label.
        detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
        detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')

        # Number of objects detected
        num_detections = detection_graph.get_tensor_by_name('num_detections:0')

        # Open video file
        video = cv2.VideoCapture(PATH_TO_VIDEO)

        while(video.isOpened()):

            # Acquire frame and expand frame dimensions to have shape: [1, None, None, 3]
            # i.e. a single-column array, where each item in the column has the pixel RGB value
            ret, frame = video.read()
            time_stamp = video.get(cv2.CAP_PROP_POS_MSEC)
            #print(time_stamp)
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_expanded = np.expand_dims(frame_rgb, axis=0)

            # Perform the actual detection by running the model with the image as input
            (boxes, scores, classes, num) = sess.run(
                [detection_boxes, detection_scores, detection_classes, num_detections],
                feed_dict={image_tensor: frame_expanded})
            # draw a plot
            #print("Boxs:", boxes)
            #print("scores:",scores[0][0])
            #print("classes:",classes)
            #print("num:", num)
            # Draw the results of the detection (aka 'visulaize the results')
            vis_util.visualize_boxes_and_labels_on_image_array(
                frame,
                np.squeeze(boxes),
                np.squeeze(classes).astype(np.int32),
                np.squeeze(scores),
                category_index,
                use_normalized_coordinates=True,
                line_thickness=8,
                min_score_thresh=0.60)

            self.overlay_text(str(f"file:{self.VIDEO_NAME}"), frame, (100, 50), 1)
            self.overlay_text(str(f"time: {round(time_stamp/1000,2)}s"),frame,(100,100),1)
            #cv2.putText(frame,str(f"TimeStamp: {round(time_stamp/1000,2)}s"),(1600,1000),cv2.FONT_HERSHEY_PLAIN,1,(0,140,255),3)
            #resize = cv2.resize(frame, None, fx=self.scaling_factorx, fy=self.scaling_factory, interpolation=cv2.INTER_AREA)
            resize = cv2.resize(frame, (2000,1800), interpolation=cv2.INTER_AREA)
            # All the results have been drawn on the frame, so it's time to display it.
            cv2.imshow('Object detector', frame)
            # Code for variable used in plot.
            self.SCORES.append(scores[0][0])
            self.TIME_STAMP.append(round(time_stamp/1000, 1))
            #self.COUNTER.append()

            # Press 'q' to quit
            if cv2.waitKey(1) == ord('q'):
                break
            if video.get(cv2.CAP_PROP_POS_FRAMES) == video.get(cv2.CAP_PROP_FRAME_COUNT):
                # If the number of captured frames is equal to the total number of frames,
                # we stop
                break
        # Clean up
        # plt.plot(boxes,scores)
        # print("SCORES LIST: ",self.SCORES)
        # print("Time Stamp: ", self.TIME_STAMP)
        video.release()
        cv2.destroyAllWindows()

    def plot(self):

        print("test plot")
        #plt.plot(range(1, len(self.SCORES), 25), self.SCORES[::25])
        # plt.plot(self.TIME_STAMP[::25], self.SCORES[::25])
        # plt.xlabel("Time Stamp in seconds")
        # plt.ylabel(" Prediction Score %")
        # plt.savefig("mygraph.png")


        fig, ax = plt.subplots()
        plt.plot(self.TIME_STAMP[::25], self.SCORES[::25],marker=".")
        ax.set(title='Sacchi Disk Detection', xlabel='Time Stamp in second', ylabel='Prediction Score %')
        if os.path.isfile("sacchi.png"):
            print("File Exists: Deleting....")
            os.remove("sacchi.png")
            print(os.path.isfile("sacchi.png"))
        
        fig.savefig('secchi.png', transparent=False, dpi=80, bbox_inches="tight")
        #     delete file
        #     dave file
        print("File Saved")
        plt.close()
        #plt.show()

    def overlay_text(self,txt, img, ll, fscale=1):
        """Use OpenCV to overlay text"""
        font = cv2.FONT_HERSHEY_DUPLEX
        bottomLeftCornerOfText = ll
        fontScale = fscale
        fontColor = (0, 150, 255)  # (0,140,255) # BGR
        lineType = 2

        cv2.putText(img, txt,
                    bottomLeftCornerOfText,
                    font,
                    fontScale,
                    fontColor,
                    lineType)

if __name__=="__main__":
    print("predict.py")
    p = Predict('YDXJ0042.mp4')
    p.run()
    p.plot()