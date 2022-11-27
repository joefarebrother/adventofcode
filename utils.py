# pylint: disable=unused-wildcard-import
from functools import *
from misc_utils import *
from input_utils import *
from geom import *
from grid import Grid
from graph import AbGraph, FGraph, DGraph
import re
import itertools as it
from dataclasses import dataclass

import sys
if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)
