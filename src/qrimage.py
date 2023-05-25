import os, sys
import argparse
import qrcode
import qrcode.image.pil
import uuid
import json

from pathlib import Path
from enum import Enum
from types import SimpleNamespace

class qrerror(Enum):
    M = 0
    L = 1
    Q = 3
    H = 4

class QRImage:
    def __init__(self, directory: str):

        if(not directory):
            directory = "./"

        self.directory = directory
        self.qr = qrcode.QRCode()
        self.setup(1, qrerror.M, 10, 4)
    
    @property
    def directory(self) -> str:
        return self.__directory

    @directory.setter
    def directory(self, value) -> str:
        if(not value):
            self.__directory = "./"
        else:
            self.__directory = value
            
    @property
    def version(self) -> str:
        return self.qr.version
    
    @property
    def error_correction(self) -> int:
        return self.qr.error_correction

    @property
    def box_size(self) -> int:
        return self.qr.box_size
    
    @property
    def border(self) -> int:
        return self.qr.border

    def setup(self, version: int, error_correction: qrerror, box_size: int, border: int) -> None:
        self.qr.version = version
        self.qr.box_size = box_size
        self.qr.border = border
        self.qr.error_correction = self.error_correct(error_correction)

    def create(self, data: str, filename: str = str(), fit: bool=True) -> qrcode.image.pil.Image:
        self.qr.add_data(data)
        self.qr.make(fit)
        
        if(not filename):
            filename = str(uuid.uuid4()) + ".png"

        img = self.qr.make_image()
        img.save(os.path.join(self.directory, filename))

        return img

    def clear(self) -> None:
        self.qr.clear()

    def error_correct(self, mode: qrerror) -> qrerror:
        return {
            qrerror.L: qrcode.ERROR_CORRECT_L,
            qrerror.M: qrcode.ERROR_CORRECT_M,
            qrerror.Q: qrcode.ERROR_CORRECT_Q,
            qrerror.H: qrcode.ERROR_CORRECT_H,
        }[mode]


def qrimage_main(argv):
    filename = Path(__file__).name

    argumentParser = argparse.ArgumentParser()
    argumentParser.add_argument("-f", "--folder", required=False, help="Temporary image storage path")
    argumentParser.add_argument("-o", "--output", required=False, help="Image output filename")
    argumentParser.add_argument("-i", "--input", required=True, help="Data for QR-Code generation")
    argumentParser.add_argument("-s", "--setup", required=False, help="JSON configuration file")
    argumentParser.add_argument("-v", "--verbose", action="store_true", help="Show whats going on")

    args = argumentParser.parse_args()

    if(args.verbose):
        print(filename, "args=%s" % args)

    if(args.folder):
        os.makedirs(args.folder, exist_ok=True)

    qrimage = QRImage(args.folder)
    setupjson: any

    if(args.setup):
        if(os.path.exists(args.setup)):
            with open(args.setup, "rb")as fp:
                setupjson = json.loads(fp.read(), object_hook=lambda d: SimpleNamespace(**d))

            qrimage.setup(setupjson.version, qrerror(setupjson.error_correction), setupjson.box_size, setupjson.border)

    if(args.setup and hasattr(setupjson, 'fit')):
        qrimage.create(data=args.input, filename=args.output, fit=setupjson.fit)
    else:
        qrimage.create(data=args.input, filename=args.output)
        
if __name__ == "__main__":
   qrimage_main(sys.argv[1:])