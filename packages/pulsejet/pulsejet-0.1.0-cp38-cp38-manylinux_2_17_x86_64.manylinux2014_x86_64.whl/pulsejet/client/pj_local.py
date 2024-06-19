import logging
from typing import (
    Any,
    Dict,
    Generator,
    Iterable,
    List,
    Mapping,
    Optional,
    Sequence,
    Tuple,
    Union,
)
from ..client.pj_base import *
from ..pulsejet import *

class PulsejetLocal(PulsejetBase):
    def __init__(self, options: Options) -> None:
        self.options = options
        logging.info(f"PulseJet™ DB - Launching database in the background with in-memory config.")
        launch(self.options)
        logging.info(f"PulseJet™ DB - Database has been launched.")
