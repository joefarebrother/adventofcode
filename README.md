# Advent of Code
My solutions to [Advent of Code](https://adventofcode.com).
At the moment, I'm mostly trying to go fast, and then improve/cleanup the code later.

My solutions can be found in `day(n).py` files or `day(n).ipynb`; and my original versions can be found in the commit history if I've refactored them afterwards.

Previous years are in their own folder.
My inputs aren't included.

`mistakes.txt` documents the mistakes I make each day.

## Dependencies
- Python >= 3.9
- `pip install attrdict`
- `sudo apt install inotify-tools` (for the autotester) 

## Utility scripts
- `aocfetch [day] [year]` - Downloads your input. Requires env var `AOC_KEY` to be set to your session cookie, which can be found via the network tools of your browser.
- `submit part ans [day] [year]` - Submits an answer. Also requires `AOC_KEY`.
- `autotest.py [year/day] [day]` - Automatically runs solution file against example data, then submits the output for the real data when the test passes. See `--help` for more info.