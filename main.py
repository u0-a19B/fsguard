import os

class Walker:
    def __init__(self, base):
        self.base = base

    def file_wrapper(self, handler):
        def wrapper(*args, **kwargs):
            for root, dirs, files in os.walk(self.base):
                for file in files:
                    handler(os.path.join(root, file))
        return wrapper

wlk = Walker('.')

X = 0

@wlk.file_wrapper
def test(x):
    print(x)


test()

