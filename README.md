# Advent of Code
My solutions to [Advent of Code](https://adventofcode.com).
At the moment, I'm mostly trying to go fast, and then improve/cleanup the code later.

My solutions can be found in `sol.py` files in the folder for the relevant year; and my original versions can be found in the commit history if I've refactored them afterwards.

My inputs aren't included.

`mistakes.txt` documents the mistakes I make each day.

## Dependencies
- Python >= 3.10
- `pip install -e .`  (or put this dir on pythonpath)
- `pip install sympy` (just used for one solution)
- Linux specific for autotester:
- - `sudo apt install inotify-tools` 
- Mac specific for autotester:
- - `brew install fswatch` 
- - `brew install coreutils` 
- - `alias timeout=gtimeout` 

## Utility scripts
- `autotest.py [year/day] [day]` - Automatically runs solution file against example data, then submits the output for the real data when the test passes. See `--help` for more info.
- `test_all.py [year]` - Automatically tuns `autotest.py` on every day for a given year, or all years if none given.