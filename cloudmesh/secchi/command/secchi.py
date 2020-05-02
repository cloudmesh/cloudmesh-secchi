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
                secchi upload [FILE] [--training] [--validate] [--predict]
                secchi run [--setup] [--predict] [--training][--resize=0.5]
                secchi remove [VIDEO][--training][--validate][--predict]
                secchi show graph 
                secchi list file [--predict] [--training]
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
              FILE  a file or directory name to upload

          Options:
              --training    command is used for training
              --validate    command is used for validation set
              --predict     command is used for prediction


        """
        # command examples:
        #   cms secchi upload '~\Desktop\Yi-Site1.mp4' --predict
        #   cms secchi remove --predict
        #   cms secchi run --predict
        #   cms secchi run --predict --resize=0.5
        #   cms secchi show graph

        map_parameters(arguments,
                       'training',
                       'validate',
                       'predict',
                       'ratio',
                       'resize',
                       'steps',
                       'setup')

        VERBOSE(arguments)

        ############################################################
        #           MODEL PREDICTION CODE                          #
        ############################################################

        file_size = 500
        
        if arguments.upload and arguments.predict:

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

        elif arguments.list and arguments.file:
            if arguments.predict:
                print("list all input video")
                v = Video()
                v.listsVideo()
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
            
            resize_scale = float(arguments.resize)
            
            if(file is not None):
                
                if resize_scale:
                    p = Predict(file, resize_scale)        
                else:    
                    p = Predict(file)
                p.run()
                p.plot()

        
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
        
        ############################################################
        #           MODEL TRAINING CODE                            #
        ############################################################
        elif arguments.upload and arguments.training:
            # upload training image set to training folder
            print("training")

        elif arguments.run and arguments.setup:
            import cloudmesh.secchi.secchi_util as util

            url_model = 'https://github.com/tensorflow/models/archive/r1.13.0.zip'
            url_protobuf = "https://github.com/protocolbuffers/protobuf/releases/download/v3.11.4/protoc-3.11.4-linux-x86_64.zip"
            print("run setup")

            # Downlaod Model utilities
            util.download(url_model, 'model')
            util.rename('models', 'model')

            #
            util.download(url_protobuf, 'Proto', new_dir='Protobuf')
            util.rename('protoc-', 'Protobuf')
            util.install()        

        elif arguments.run and arguments.training:
            from cloudmesh.secchi.tensorflow.model_main import train_run
            print("run training")

            # if arguments.steps:
            #     #t = Train(arguments.steps)
            #     train_run()
            # else:
            #     #t = Train()
            #     train_run()
            #     print("Inside run and training condition")
            # tf.app.run(t.main())
            # t.main()
            p = Path(os.path.abspath(__file__))
            path = p.parent.parent
            train_file = os.path.join(path, 'tensorflow', 'model_main.py')
            str = f'python {train_file} --alsologtostderr'
            os.system(str)

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
