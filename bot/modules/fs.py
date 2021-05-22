import json
import os
from config import *
import shutil


def touch(file):
    if not os.path.exists(file):
        with open(file, 'x'):
            pass


def fs_read(file):
    if os.path.exists(file):
        with open(file) as f:
            result = json.load(f)
        return result
    else:
        raise FileNotFoundError(f'{file} Not Found')


def fs_update(file, obj):
    try:
        with open(file, 'w') as f:
            json.dump(obj, f, indent=2)
    except FileNotFoundError:
        return False
    return True


def fs_create(file, obj):
    if not os.path.exists(file):
        with open(file, 'w') as f:
            json.dump(obj, f, indent=2)


def fs_unlink(file):
    if os.path.exists(file):
        os.unlink(file)


def init():
    if not os.path.exists(DOWNLOADS_DIR):
        os.mkdir(DOWNLOADS_DIR)
    if not os.path.exists(USERS_DIR):
        os.mkdir(USERS_DIR)


def clean_all():
    if not os.path.exists(DOWNLOADS_DIR):
        shutil.rmtree(DOWNLOADS_DIR)
    if not os.path.exists(USERS_DIR):
        shutil.rmtree(USERS_DIR)
