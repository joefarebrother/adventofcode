# pylint: disable=unused-import
from collections import defaultdict, Counter, deque
import re
import itertools
import sys
from dataclasses import dataclass
from copy import copy, deepcopy
from functools import *
from misc_utils import *
from input_utils import *
from geom import *
from grid import Grid
from graph import AbGraph, FGraph, DGraph

it = itertools

if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)
