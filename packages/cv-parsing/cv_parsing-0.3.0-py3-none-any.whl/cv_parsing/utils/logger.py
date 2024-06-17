import os
import logging
import time
import tempfile


# Get temporary directory

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = CURRENT_DIR.split('src')[0]
OUT_DIR = os.path.join(ROOT_DIR, 'out')

timestamp = time.strftime("%Y%m%d-%H%M%S")


def load_logger(path=os.path.join(OUT_DIR, f'cv_{timestamp}.log')):
    logging.basicConfig(level=logging.INFO, filename=path,
                        filemode='w', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


if os.path.exists(OUT_DIR):
    load_logger()
else:
    fp = tempfile.NamedTemporaryFile(delete=False)
    load_logger(fp.name)
