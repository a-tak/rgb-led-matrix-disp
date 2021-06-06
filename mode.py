#!/usr/bin/env python3
# coding: UTF-8
# Mode object
from enum import Enum
from logging import getLogger, StreamHandler, DEBUG
logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)

class Mode(Enum):
    CLOCK = 1
    DATE = 2
    TEMP = 3
    MEIGEN = 4

# Main function
if __name__ == "__main__":
    main_obj = Mode()
    

