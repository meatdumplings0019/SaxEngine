﻿import os

if __name__ == '__main__':
    os.system("pyinstaller -F run.py -n SaxEngine -w --icon ./icon.ico --add-data InAssets;InAssets")