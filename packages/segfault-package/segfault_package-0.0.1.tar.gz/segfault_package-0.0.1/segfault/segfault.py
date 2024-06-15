import ctypes
import os

# Загрузка библиотеки
lib_path = os.path.join(os.path.dirname(__file__), '..', 'libsegfault.so')
lib = ctypes.CDLL(lib_path)

def cause_segfault():
    lib.cause_segfault()