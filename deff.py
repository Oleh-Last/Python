import errno
import os

##Creating a folder at the root of the program
def make_sure_path_exists(path):
    try: os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

##Фуfunction that translates from cm to pixel
def cm_in_px(cm):
    global px
    px = int(cm) * 38
    return px
