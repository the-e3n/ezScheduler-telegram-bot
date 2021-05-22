from requests import get
from config import DOWNLOADS_DIR
import os


def download(ep):
    dest = os.path.join(DOWNLOADS_DIR, ep['file_name'])
    if ep['torrent']:
        with open(dest, 'wb') as f:
            f.write(get(ep['torrent']).content)
        return dest

