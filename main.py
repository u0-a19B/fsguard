import os
import hashlib
import sys
import json
import time

file_hashed: dict[str,str] = {}
dir_hashed: dict[str,str] = {}


def Parser(file):
    try:
        f = open(file, 'r')
        data = f.read()
        f.close()
        js = json.loads(data)
        return js['f'], js['d']
    except json.decoder.JSONDecodeError:
        return None, None
    except KeyError:
        return None, None
    except FileNotFoundError:
        print(f"No such file {file}")
        sys.exit(-1)

class Walker:

    def __init__(self, base):
        self.base = base
        self.hash_buffer: str = ""

    def file_wrapper(self):
        for root, dirs, files in os.walk(self.base):
            for file in files:
                self.hash_dir(os.path.join(root, file))

    def hash_dir(self, f):
        self.hash_buffer += Walker.hash_file(f)

    @staticmethod
    def hash_file(file):
        try:
            with open(file, 'rb') as data:
                return hashlib.md5(data.read()).hexdigest()
        except FileNotFoundError:
            print(f"No such file {file}")
            sys.exit(-1)

    @staticmethod
    def hash_string(h):
        return hashlib.md5(h).hexdigest()

X = 0

def hash_init():
    files, dirs = Parser(sys.argv[1])
    if files == None:
        print("Config decode error")
        sys.exit(-2)
    for f in files:
        file_hashed[f] = Walker.hash_file(f)
    for d in dirs: 
        wlk = Walker(d)
        wlk.file_wrapper()
        dir_hashed[d] = hashlib.md5(wlk.hash_buffer.encode()).hexdigest()


def file_check(f_hashed) -> None:
    for k, v in f_hashed.items():
        new_hash = Walker.hash_file(k)
        # print(f"Check status : old {v}, new {new_hash}")
        if new_hash != v:
            print(f"file changed :{k}")

def dir_check(d_hashed) -> None:
    for k, v in d_hashed.items():
        wlk = Walker(k)
        wlk.file_wrapper()
        new_hash = hashlib.md5(wlk.hash_buffer.encode()).hexdigest()
        # print(f"Check status : old {v}, new {new_hash}")
        if new_hash != v:
            print(f"Dir changed :{k}")
        print(f"Dir status old {v}, new {new_hash}")
# print(Walker.hash_file('main.py'))
# hash_dir()
# print(Walker.hash_string(hash_buffer.encode()))
# print(Parser(sys.argv[1]))
hash_init()

while 1:
    file_check(file_hashed)
    dir_check(dir_hashed)
    time.sleep(3)
