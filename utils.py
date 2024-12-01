# pylint: disable=unused-import
from collections import defaultdict, Counter, deque
import re
import itertools
import sys
from dataclasses import dataclass, field
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

import resource

def memory_limit(mb):
    """Limit max memory usage to half."""
    soft, hard = resource.getrlimit(resource.RLIMIT_AS)
    avail = (int(get_memory_kb() * 1024 * 0.7))
    lim = mb*1024*1024
    if avail < lim:
        print(f"==== Limiting to {round(avail/1024/1024, 1)} MB====")
        lim = avail
    resource.setrlimit(resource.RLIMIT_AS, (lim, hard))

def get_memory_kb():
    with open('/proc/meminfo', 'r') as mem:
        free_memory = 0
        for i in mem:
            sline = i.split()
            if str(sline[0]) in ('MemFree:'): # 'Buffers:', 'Cached:'
                free_memory += int(sline[1])
    return free_memory  # KiB


memory_limit(500)