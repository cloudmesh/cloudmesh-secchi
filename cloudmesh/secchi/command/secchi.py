from __future__ import print_function

from cloudmesh.shell.command import command
from cloudmesh.shell.command import PluginCommand
from cloudmesh.secchi.video import Video
from cloudmesh.common.util import path_expand, banner
from cloudmesh.common.debug import VERBOSE
from cloudmesh.shell.command import map_parameters
from cloudmesh.common.console import Console

import os
from pathlib import Path


class SecchiCommand(PluginCommand):

    # noinspection PyUnusedLocal
    @command
    def do_secchi(self, args, arguments):
        """
        ::

          Usage:
                secchi upload [FILE] [--training] [--validate] [--predict][--setfilelimit=100]
                secchi run [--setup] [--predict] [--training][--resize=0.5]
                secchi remove [VIDEO][--training][--validate][--predict]
                secchi show graph 
                secchi list file [--predict] [--training]
                secchi create partitiondataset [INPUTDIR] [--ratio=0.2]
                secchi delete partitiondataset
                secchi prep --training
                secchi set [--predict] [--filesize=100]

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
        #   cms secchi list file --predict
        #   cms secchi run --predict
        #   cms secchi run --predict --resize=0.5
        #   cms secchi show graph

        map_parameters(arguments,
                       'training',
                       'validate',
                       'predict',
                       'ratio',
                       'resize',
                       'setfilelimit',
                       'steps',
                       'setup')

        VERBOSE(arguments)

        ############################################################
        #           MODEL PREDICTION CODE                          #
        ############################################################

        #file_size = 500
        
        if arguments.upload and arguments.predict:

            # validate extension and file size. Max size=125 MB
            # upload video file in for prediction.
            banner("Upload file for prediction")
            file = path_expand(arguments.FILE)
            if arguments.setfilelimit:
                file_size = int(arguments.setfilelimit)
            else:
                file_size = 500 # Default size limit

            try:
                size = os.path.getsize(file) / (1024 * 1024)

                if size > file_size:
                    
                    Console.error(f"Size limit {file_size}MB exceeds. End upload")
                    print("")
                    print("********************")
                    print("Suggested command:")
                    print(
                        """
                        Default size limit is 500MB.To increase file size limit, run: 
                        
                        cms secchi upload --predict --setfilelimit=800

                        This command will set file size - 800MB.
                        """
                        )
                # validate extension:
                else:
                    v = Video()

                    if(v.validateFileFormat(file, 'predict')):
                        # valid format
                        print("format is valid")
                        v.upload(file)
                        print("File uploaded successfully")
                        print("")
                        print("********************")
                        print("Suggested command:")
                        print(
                            """
                            To run prediction: command - 
                            cms secchi run --predict
                            """)
                        print(
                            """To remove uploaded file: command - 
                            cms secchi remove --predict
                            """)

                    else:
                        Console.error("File format is not valid.")
                        v = Video()
                        formats = v.getValidFormat()
                        print(f"Valid formats: {formats}")


            except FileNotFoundError:
                Console.error(f"File is not found at {file}. Please validate and try again.")


        elif arguments.list and arguments.file:
            if arguments.predict:
                banner("List all uploaded file for prediction")
                v = Video()
                v.listsVideo()
            elif arguments.training:
                banner("List all uploaded file for training")
            
            elif arguments.validate:
                banner("List all uploaded file for validation")

        elif arguments.run and arguments.predict:
            
            banner("Run Prediction")
            # check if video file exists in src location
            v = Video()
            file = v.getVideoFile()
            
            if(file is not None):
                from cloudmesh.secchi.tensorflow.predict import Predict
                if arguments.resize:            
                    resize_scale = float(arguments.resize)
                    p = Predict(file, resize_scale)

                else:    
                    p = Predict(file)

                p.run()
                p.plot()
                print("********************")
                print("Suggested command:")
                print(
                    """
                    To adjust frame size use predict command :                     
                    cms secchi run --predict --resize=0.5
                    """)

                print(
                    """
                    To view graph run command :                     
                    cms secchi show graph
                    """)


            else:
                Console.error("No Video file found.")    
                print("")
                print("********************")
                print("Suggested command:")
                print(
                    """
                    To upload file for prediction: run -                    
                    cms secchi upload '~/Desktop/file.mp4' --predict
                    """)

        elif arguments.remove and arguments.predict:
            banner("Delete uploaded file for prediction")
            video = arguments.FILE
            v = Video()
            v.removeFile(video)
            print("")
            print("********************")
            print("Suggested command:")
            print(
                """
                To upload file for prediction: run command - 
                cms secchi upload '~/Desktop/file.mp4' --predict
                """)

        elif arguments.show and arguments.graph:
            banner("Displaying graph")

            p = Path(os.path.abspath(__file__))
            path = p.parent.parent.parent.parent
            print(path)
            file = os.path.join(path, 'image/secchi.png')

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
