# Lantern
A super handy 🖐️ CLI script to manage Leetcode solutions and neatly keep them arranged in directories with a navigable index.

For an example, [check this repository](https://github.com/ab1nv/leetcode) where I use lantern to keep a track of my Leetcode solutions.

## Installing
This script was tested on Python 3.13. Older versions should work perfectly fine though. Open an issue if any problem arises.

Also, you need to have [uv]((https://docs.astral.sh/uv/getting-started/installation/)) installed on your machine. I will add other options in the future.
```
git clone https://github.com/ab1nv/lantern.git
cd lantern
uv pip install -e
```
there you go, lantern is installed! 🎉

## Running
1. To use lantern, rename `example.config.py` to `config.py` and populate the required values.
2. Run `lantern` in the directory you assigned in `config.PATH` variable.

## Planned Features

- [ ] Java Support
- [ ] Stats (Total Questions Solved, Language Stats, etc.)
- [ ] Test Runner (currently in development.)
- [ ] Video instruction for installing and running the tool.

PRs are always welcome.
