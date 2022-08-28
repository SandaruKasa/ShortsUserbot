import logging
import os

from . import client

logging.basicConfig(
    handlers=[
        logging.StreamHandler(),
    ],
    level=os.getenv("LOGLEVEL", logging.getLevelName(logging.INFO)).upper(),
    format="[%(asctime)s.%(msecs)03d] [%(name)s] [%(levelname)s]: %(message)s",
    datefmt=r"%Y-%m-%dT%H-%M-%S",
)
client.run()
