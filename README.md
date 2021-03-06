# Advent of Code
My solutions to [Advent of Code](https://adventofcode.com).
At the moment, I'm mostly trying to go fast, and then improve/cleanup the code later.

My solutions can be found in `day(n).py` files; and my original versions can be found in the commit history.
Previous years are in their own folder.
My inputs aren't included.

`mistakes.txt` documents the mistakes I make each day.

## Dependencies
- Python >= 3.9
- `pip install attrdict`

## Utility scripts
- `aocfetch [day] [year]` - Downloads your input. Requires env var `AOC_KEY` to be set to your session cookie, which can be found via the network tools of your browser.
- `submit part ans [day] [year]` - Submits an answer. Also requires `AOC_KEY`.