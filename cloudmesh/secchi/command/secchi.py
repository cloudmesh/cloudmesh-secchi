from __future__ import print_function

from cloudmesh.shell.command import command
from cloudmesh.shell.command import PluginCommand
from cloudmesh.secchi.video import Video
from cloudmesh.common.util import path_expand
from cloudmesh.common.debug import VERBOSE
from cloudmesh.shell.command import map_parameters
import os
from pathlib import Path


class SecchiCommand(PluginCommand):

    # noinspection PyUnusedLocal
    @command
    def do_secchi(self, args, arguments):
        """
        ::

          Usage:
                secchi upload [FILE][--training] [--validate][--predict]
                secchi list input [--training] [--validate] [--predict]
                sechhi delete VIDEOS
                secchi server start
                secchi server stop
                secchi server status
                secchi run [--predict] [--training]
                secchi remove [VIDEO][--training][--validate][--predict]
                secchi show graph
                secchi create partitiondataset [INPUTDIR] [--ratio=0.2]
                secchi delete partitiondataset
                secchi prep --training

          This command does some useful things.

          Arguments:
              upload   To upload training, validation, prediction files.
              list    To list out all the files
              input  input
              delete  cc
              server  cc
              start  cc
              stop  cc
              FILE         a file or directory name to upload

          Options:
              --training    command is used for training
              --validate    command is used for validation set
              --predict     command is used for prediction

        """
        # command examples:
        #   cms secchi upload '~\Desktop\Yi-Site1.mp4' --predict
        #   cms secchi remove --predict
        #   cms secchi show graph

        map_parameters(arguments,
                       'training',
                       'validate',
                       'predict',
                       'ratio')

        VERBOSE(arguments)

        file_size = 500
        if arguments.upload and arguments.training:
            # upload training image set to training folder
            print("training")

        elif arguments.upload and arguments.predict:
            # validate extension and file size. Max size=125 MB
            # upload video file in for prediction.
            file = path_expand(arguments.FILE)
            size = os.path.getsize(file) / (1024 * 1024)
            if size > file_size:
                print(f"Size limit {file_size}MB exceeds. End upload")

            # validate extension:
            else:
                v = Video()

                if(v.validateFileFormat(file, 'predict')):
                    # valid format
                    print("format is valid")
                    v.upload(file)
                    print("File uploaded successfully")

                else:
                    print("File format is not valid")

        elif arguments["list"] and arguments.input:
            if arguments.predict:
                print("list all input video")
            elif arguments.training:
                print("List all training images")
            elif arguments.validate:
                print("list all validation images")

        elif arguments.run and arguments.predict:
            from cloudmesh.secchi.tensorflow.predict import Predict

            print("run prediction")
            # check if video file exists in src location
            v = Video()
            file = v.getVideoFile()
            if(file is not None):
                p = Predict(file)
                p.run()
                p.plot()

        elif arguments.run and arguments.training:
            print("run training")

        elif arguments.remove and arguments.predict:
            print("Delete uploaded file")
            video = arguments.FILE
            v = Video()
            v.removeFile(video)

        elif arguments.show and arguments.graph:
            p = Path(os.path.abspath(__file__))
            path = p.parent.parent.parent.parent
            print(path)
            file = os.path.join(path, 'secchi.png')

            if os.path.exists(file):
                os.system(file)
            else:
                print("File doesn't exists")

        # Code for partitioning dataset. 10-19
        elif arguments.partitiondataset and arguments.delete:
            from cloudmesh.secchi.tensorflow.preprocessing.partition_dataset import PartitionDataset

            pd = PartitionDataset()
            pd.delete()

        elif arguments.create and arguments.partitiondataset:
            from cloudmesh.secchi.tensorflow.preprocessing.partition_dataset import PartitionDataset

            inputDir = path_expand(arguments.INPUTDIR)
            if arguments.ratio:
                ratio = float(arguments.ratio)
            else:
                ratio = 0.1
            print(f"inputDir: {inputDir}, ratio: {ratio}")
            pd = PartitionDataset(inputDir, ratio)
            pd.run()

        elif arguments.prep and arguments.training:
            from cloudmesh.secchi.tensorflow.preprocessing.xml_to_csv import XmlToCSV
            from cloudmesh.secchi.tensorflow.preprocessing.generate_tfrecord import GenTF
            # converts img xml to csv
            xtc = XmlToCSV()
            xtc.xml_csv_conv()
            # converts csv to TF record
            gtf_train = GenTF('train')
            gtf_train.create()
            gtf_test = GenTF('test')
            gtf_test.create()

        return ""
