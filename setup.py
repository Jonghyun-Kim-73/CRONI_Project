import sys
import os
from cx_Freeze import setup, Executable


ROOT_PATH = os.path.dirname(os.path.abspath(__file__))

files = ['AIDA_Interface_brief_ver/DB/', 'AIDA_Interface_brief_ver/interface_image/']

target = Executable(
    script='AIDA_Interface_brief_ver/main.py',
    base='Win32GUI',
)


setup(
    name="AIDAA",
    version='1.0',
    author='DaeilLee',
    options={'build_exe': {'include_files': files}},
    executables=[target]
)

