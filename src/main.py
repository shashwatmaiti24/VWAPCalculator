from os.path import dirname, realpath, join
from sys import argv
from time import time
from reader import read_itch

if __name__ == '__main__':
    if len(argv) > 1:
        file_path = argv[1]
    else:
        script_dir = dirname(realpath(__file__))
        relative_path = "../data/01302019.NASDAQ_ITCH50.bin"
        file_path = join(script_dir, relative_path)

    start = time()
    read_itch(file_path)
    print('Used time:',int(time()-start))
