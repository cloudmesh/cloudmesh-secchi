import os
import cv2
import shutil
from pathlib import Path
from cloudmesh.common.util import path_expand
import glob
from cloudmesh.common.Shell import Shell

class Video:

#Video.__filename__
# directory = os.path.dirname(Vido.__filename__

    valid_extn = ["MP4", "AVI"]

    def __init__(self, dest="~/.cloudmesh/secchi"):
        # if none put it
        # in cwd/dest
        self.dest = path_expand(dest)
        # dir_path = os.path.dirname(path)
        Shell.mkdir(dest)
        # print("dest Path:", self.dest)

    def train(self, video):

        raise NotImplementedError

        # pop up LabelImag
        os.sysmem()

    def analyse(self):
        raise NotImplementedError

    def getValidFormat(self):
        return self.valid_extn

    def upload(self, filepath=None, kind="analyse"):
        file = os.path.basename(filepath)
        try:
            shutil.copy(filepath, self.dest)
        except FileNotFoundError:
            print("File is not found")

    def list(self, name=None):
        # lists videos and tells us info about them in json format
        # is training
        # images
        # size
        # non = all, if name only that
        # use glob.glob in teh des dir

        # list all files in input folder

        raise NotImplementedError

    def download(self, url, name=None):
        # python requests to download
        # put the file into dest under name, if name is not specified put it in
        # what if file already exists?
        raise NotImplementedError

    def imageCapture(self,input_dir):

        scaling_factorx = 0.5
        scaling_factory = 0.5
        input_archive = 'input_archive/'    # Provide input directory here.
        path = 'output/image/'              # Provide output directory here.
        files = os.listdir(input_dir)

        for file in files:

            name = file.split(".")

            # cap = cv2.VideoCapture(file)
            cap = cv2.VideoCapture(os.path.join(input_dir, file))

            i = 0
            while (True):
                # Capture frame-by-frame
                ret, frame = cap.read()

                # exit loop after capturing every video file
                if frame is None:
                    break
                # changing frame to gray scale.
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                # resizing frame
                resize = cv2.resize(gray, None, fx=scaling_factorx, fy=scaling_factory, interpolation=cv2.INTER_AREA)

                # saving every 100th frame

                if i % 100 == 0:
                    # cv2.imwrite('Img' + str(i) + '.jpg', gray,)
                    cv2.imwrite(os.path.join(path, (name[0] + "_" + str(i // 100) + '.jpg')), gray)
                i += 1
                # Display the resulting frame
                cv2.imshow('frame', resize)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

            # When everything done, release the capture
            cap.release()

        cv2.destroyAllWindows()
        self.move_to_archive(files, input_dir, input_archive)

    def move_to_archive(self, files, input_dir, dest):

        for file in files:
            shutil.move(input_dir + file, dest)

    def validateFileFormat(self, file, str='notPredict'):
        filename = os.path.basename(file)
        if str == 'predict':

            extn = filename.split(".")[1]
            if extn.upper() in self.valid_extn:
                return True
            else:
                return False
        else:
            extn = filename.split(".")[-1]
            if extn is None:
                # Its a folder path
                return True
            else:
                # It's not a folder path
                return False

    def getVideoFile(self):
        files = os.listdir(self.dest)

        for file in files:
            extn = file.split(".")[-1].upper()
            if extn in self.valid_extn:
                print(file)
                return file

        #print("No video file exists")
        return None

    def removeFile(self,file=None):

        if file is None:
            #remove all video file
            files = os.listdir(self.dest)
            for file in files:
                extn = file.split('.')[-1].upper()
                if extn in self.valid_extn:
                    os.remove(os.path.join(self.dest, file))
                    print(f"{file} is removed")
        else:

            os.remove(os.path.join(self.dest,file))
            print(f"{file} is removed.")
            
    def listsVideo(self):

        os.chdir(self.dest)
        for extn in self.valid_extn:
            for file in glob.glob(f"*.{extn}"):
                print(file)


if __name__== "__main__":
    #print(__import__("Video"))
    v= Video()
    #v.upload()
    v.getVideoFile()


