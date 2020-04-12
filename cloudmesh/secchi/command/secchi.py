from __future__ import print_function

from cloudmesh import shell
from cloudmesh.shell.command import command
from cloudmesh.shell.command import PluginCommand
from cloudmesh.secchi.video import Video
from cloudmesh.secchi.api.manager import Manager
from cloudmesh.common.console import Console
from cloudmesh.common.util import path_expand, banner
from pprint import pprint
from cloudmesh.common.debug import VERBOSE
from cloudmesh.shell.command import map_parameters
import os
from pathlib import Path

# from.cloudmesh.secchi.tensorflow.predict import predict
#from src.predict import Predict


class SecchiCommand(PluginCommand):

    # noinspection PyUnusedLocal
    @command
    def do_secchi(self, args, arguments):
        """
        ::

          Usage:
                secchi upload [FILE][--training][--validate][--predict]
                secchi list input [--training][--validate][--predict]
                sechhi delete VIDEOS
                secchi server start
                secchi server stop
                secchi server status
                secchi labelImg install
                secchi labelImg run
                secchi captureImage
                secchi run [--predict][--training]
                secchi remove [VIDEO][--training][--validate][--predict]
                secchi show graph

          This command does some useful things.

          Arguments:
              upload   To upload training, validation, prediction files.
              list      To list out all the files
              delete
              server
              start
              stop

          Options:
              FILE          a file or directory name to upload
              input         input files.
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
                       'predict')

        VERBOSE(arguments)

        if arguments.upload and arguments.training:
            # upload training image set to training folder
            print ("training")
        elif arguments.upload and arguments.validate:
            # upload validation image set to validation folder
            print("validation")
        elif arguments.upload and arguments.predict:
            # validate extension and file size. Max size=125 MB
            # upload video file in for prediction.
            file = path_expand(arguments.FILE)
            size = os.path.getsize(file)/(1024*1024)
            if size > 100:
                print("Size limit 100MB exceeds. End upload")
            # validate extension:
            else:
                v = Video("~/.cloudmesh/secchi")
                if(v.validateFileFormat(file,'predict')):
                    # valid format
                    print("format is valid")
                    v.upload(file)

        elif arguments.captureImage:
            print("capture image from videos for training purpose")

        elif arguments.list and arguments.input:
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
            path = p.parent.parent
            file = os.path.join(path, 'tensorflow','sacchi.png')
            
            #fileObject = open(file, 'r')
            if os.path.exists(file):
              os.system(file)
            else:
              print("File doesn't exists")

        return ""


