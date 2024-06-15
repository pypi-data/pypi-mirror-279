import os
import sys
import platform
import faulthandler
import ctypes


if platform.system() == 'Windows':
    lib_name = 'libsegfault.dll'
else:
    lib_name = 'libsegfault.so'

lib_path = os.path.join(os.path.dirname(__file__), '..', lib_name)

if not os.path.exists(lib_path):
    raise FileNotFoundError(f"The library file was not found at: {lib_path}")

try:
    lib = ctypes.CDLL(lib_path)
except OSError as e:
    raise OSError(f"Failed to load library: {e}")

def cause_segfault():  
    faulthandler.enable(file=sys.stderr)
    lib.cause_segfault()
