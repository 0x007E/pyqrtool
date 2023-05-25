[![Version: 0.0.1](https://img.shields.io/badge/Version-0.0.1%20Beta-orange.svg)](https://github.com/0x007e) [![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
# Small Python QR-Image generator

This python script can be used with command line or as import from another script.

## Parameter

For additional information call:

``` bash
python ./pyqrtool.py -h
```

| Short | Expand    | Description        |
|-------|-----------|--------------------|
| -h    | --help    | Help menu          |
| -i    | --input   | QR-Payload         |
| -o    | --output  | Output *.png file  |
| -s    | --setup   | [Configuration](./src/qrimage.setup.json) |
| -k    | --folder  | Output folder      |

## CLI-Usage

``` bash
# Without setup
python ./qrimage.py -f ./temp -i https://github.com/0x007e -o Test.png

# With setup
python ./qrimage.py -f ./temp -i https://github.com/0x007e -s ./qrimage.setup.json -o Test.png

# The QR-Code png image should be created in temp/Test.png
```

## Python usage

``` python
qrimage: QRImage = QRImage("./temp")

# Call of setup is for standard configuration not necessary
qrimage.setup(1, qrerror.L, 20, 10)

qrimage.create("https://github.com/0x007e", filename="Test.png")
```
