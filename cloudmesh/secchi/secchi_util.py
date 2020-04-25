import os
from sys import platform
from pathlib import Path
from io import BytesIO
from urllib.request import urlopen
from zipfile import ZipFile
from cloudmesh.common.util import path_expand
import glob
from cloudmesh.common.util import Shell

def download(url):

    # print(f"CWD: {os.getcwd()}")
    # current_dir = os.getcwd()
    # print(f"ABS PATH: {os.path.dirname(__file__)}")
    p = Path(os.path.dirname(__file__))
    #tf_dir = os.path.join(p,'tensorflow')
    temp = path_expand("~/.cloudmesh/secchi")
    # os.chdir(tf_dir)


    files = glob.glob(f'{temp}/model*')
    #os.system(f'git clone {url}')
    # check if file already exists.
    print(f"Files: {files}")
    fileExists = False

    for file in files:
        if os.path.isdir(file):
            print("File already exists")
            fileExists = True
    
    if not fileExists:
        print("Downloading files.....")
        with urlopen(url) as zipresp:
            with ZipFile(BytesIO(zipresp.read())) as zfile:
                zfile.extractall(temp)
        print("Downloading Ends.....")        

    # Delete all other folders except research
    # Delete all other folders within research except object-detection.

    for name in glob.glob(f'{temp}/models*'):
        temp_dir = os.path.dirname(name)
        dest = os.path.join(temp_dir,'model')
        os.rename(name,dest)
    
def compile():

    raise NotImplementedError
    #os.cwd()
    # then change it.
    #os.chdir()
    #Shell.pip()


def install():

    
    current_dir = os.getcwd()
    temp = path_expand("~/.cloudmesh/secchi/model/research/")
    temp_model = path_expand("~/.cloudmesh/secchi/model/")
    os.chdir(temp)

    if platform == "linux" or platform == "linux2" or platform == "darwin":
        # linux
        str = "protoc object_detection/protos/*.proto --python_out=."
        os.system(str)

        # Add research/slim to your PYTHONPATH
        # From within tensorflow/models/research/
        os.system("export PYTHONPATH=$PYTHONPATH:temp/slim/")
        os.system("export PYTHONPATH=$PYTHONPATH:temp_model")

    elif platform == "win32":
        str = "for /f %i in ('dir /b object_detection\protos\*.proto') do protoc object_detection\protos\%i --python_out=."
        os.system(str)

    #os.system("pip install .")  
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

    #2.
    # pip install pip -U
    # change directory to models/research and run
    # pip install .

if __name__ == '__main__':
    url = 'https://github.com/tensorflow/models/archive/r1.13.0.zip'
    #download(url)
    #install()