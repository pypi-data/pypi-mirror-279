import logging
import logging.config
import os
from pathlib import Path

import coloredlogs
import yaml


def setup(path=None, colored=False):
    if not path or not os.path.exists(path):
        print('Using default configs')
        path = Path(__file__).with_name('config.yaml')
        with open(path, 'rt') as f:
            try:
                config = yaml.safe_load(f.read())
                logging.config.dictConfig(config)
                if colored:
                    coloredlogs.install()
            except Exception as e:
                print('Error in Logging Configuration')
                raise e

