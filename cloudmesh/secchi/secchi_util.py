import os
from sys import platform
from pathlib import Path
from io import BytesIO
from urllib.request import urlopen
from zipfile import ZipFile
from cloudmesh.common.util import path_expand
import glob
from cloudmesh.common.Shell import Shell


def download(url, name, new_dir=None):

    p = Path(os.path.dirname(__file__))
    temp = path_expand("~/.cloudmesh/secchi")
    # os.chdir(tf_dir)

    files = glob.glob(f'{temp}/{name}*')
    #os.system(f'git clone {url}')
    # check if file already exists.
    print(f"Files: {files}")
    fileExists = False

    for file in files:
        if os.path.isdir(file):
            print("File already exists")
            fileExists = True

    if not fileExists:
        p = os.path.join(temp, new_dir)
        if new_dir is not None:
            Shell.mkdir(p)

        print("Downloading files.....")
        with urlopen(url) as zipresp:
            with ZipFile(BytesIO(zipresp.read())) as zfile:
                zfile.extractall(p)
        print("Downloading Ends.....")

    # Delete all other folders except research
    # Delete all other folders within research except object-detection.


def rename(src, trg):
    temp = path_expand("~/.cloudmesh/secchi")

    for name in glob.glob(f'{temp}/{src}*'):
        temp_dir = os.path.dirname(name)
        dest = os.path.join(temp_dir, trg)
        os.rename(name, dest)


def compile():

    raise NotImplementedError
    # os.cwd()
    # then change it.
    # os.chdir()
    # Shell.pip()


def update_env_variable(var, str):
    # steps to update path variable for all os.
    if platform == "linux" or platform == "linux2" or platform == "darwin":
        pass
    elif platform == "win32":
        pass


def install():

    current_dir = os.getcwd()
    temp_rsch = path_expand("~/.cloudmesh/secchi/model/research/")
    temp_model = path_expand("~/.cloudmesh/secchi/model/")
    # open a new terminal.
    # Add '~/.cloudmesh/secchi/Protobuf/' to PATH Variable.
    # os.system(f"export PATH=$PATH:{temp}/")

    os.chdir(temp_rsch)

    if platform == "linux" or platform == "linux2" or platform == "darwin":
        # linux
        str = "sudo chmod +x protoc object_detection/protos/*.proto --python_out=."
        os.system(str)

        # Add research/slim to your PYTHONPATH
        # From within tensorflow/models/research/
        # os.system("export PYTHONPATH=$PYTHONPATH:temp/slim/")
        # os.system("export PYTHONPATH=$PYTHONPATH:temp_model")
        slim = os.path.join(temp_rsch, 'slim')
        update_env_variable('PYTHONPATH', slim)
        update_env_variable('PYTHONPATH', temp_model)

    elif platform == "win32":
        str = "for /f %i in ('dir /b object_detection\protos\*.proto') do protoc object_detection\protos\%i --python_out=."
        os.system(str)

    Shell.pip("install", ".")
    os.chdir(current_dir)

    #raise NotImplementedError
    # 1.
    # os.cwd()
    # then change it.
    # os.chdir()
    # From within TensorFlow/models/research/
    # protoc object_detection/protos/*.proto --python_out=. THis command is system specific
    # for windows -
    # From within TensorFlow/models/research/
    # for /f %i in ('dir /b object_detection\protos\*.proto') do protoc object_detection\protos\%i --python_out=.

    # 2.
    # pip install pip -U
    # change directory to models/research and run
    # pip install .


if __name__ == '__main__':
    url = 'https://github.com/tensorflow/models/archive/r1.13.0.zip'
    # download(url)
    # install()
