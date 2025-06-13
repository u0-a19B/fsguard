import os
import hashlib
import sys
hash_buffer = ""

class Walker:
    def __init__(self, base):
        self.base = base

    def file_wrapper(self, handler):
        def wrapper(*args, **kwargs):
            for root, dirs, files in os.walk(self.base):
                for file in files:
                    handler(os.path.join(root, file))
        return wrapper

    @staticmethod
    def hash_file(file):
        try:
            with open(file, 'rb') as data:
                return hashlib.md5(data.read()).hexdigest()
        except FileNotFoundError:
            sys.exit(-1)

    @staticmethod
    def hash_string(h):
        return hashlib.md5(h).hexdigest()

wlk = Walker('/home/buggy/fsguard')

X = 0

@wlk.file_wrapper
def hash_dir(f):
    global hash_buffer
    hash_buffer += Walker.hash_file(f)

# print(Walker.hash_file('main.py'))
hash_dir()
print(Walker.hash_string(hash_buffer.encode()))
