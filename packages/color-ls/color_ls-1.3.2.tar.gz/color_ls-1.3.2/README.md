# colorls

Pure Python implementation of ls command with colors and icons. Inspired from [colorls](https://github.com/athityakumar/colorls). Requires [Nerd Fonts](https://github.com/ryanoasis/nerd-fonts/blob/master/readme.md) for icon/glyphs.

## Installation
`pip install color-ls`
However, since this is intended to run as an executable and not a library, it is preferable to use a tool such as [pipx](https://github.com/pypa/pipx)
`pipx install color-ls`

## Usage
```
usage: lx [-h] [-1] [-a] [-B] [-d] [-f] [-F] [-i] [-I PATTERN] [-l] [-n] [-R]
          [-t [DEPTH]] [--version] [--si] [-U] [-H] [-x]
          ...

Pure Python implementation of `ls` command. Only a subset of available
arguments are implemented

positional arguments:
  FILE                  List information about the FILE(s).

options:
  -h, --help            show this help message and exit
  -1                    list items on individual lines
  -a, --all             do not ignore entries starting with .
  -B, --ignore-backups  do not list implied entries ending with ~
  -d, --directory       list directories themselves, not their contents
  -f, --file            list files only, not directories
  -F, --classify        append indicator (one of */=>@|) to entries
  -i, --inode           display inode number
  -I PATTERN, --ignore PATTERN
                        do not list implied entries matching shell PATTERN
  -l, --long            use a long listing format
  -n, --numeric-uid-gid
                        like -l, but list numeric user and group IDs
  -R, --recursive       list subdirectories recursively
  -t [DEPTH], --tree [DEPTH]
                        max tree depth
  --version             display current version number and exit
  --si                  display file size in SI units
  -U, --unsorted        do not sort; list entries in directory order
  -H, --header          do not display header
  -x                    do not display icons

Feature Requests/Bugs should be reported at https://gitlab.com/compilation-
error/colorls/-/issues
```
## Requirements
- Python 3.8 or higher
- Nerd Fonts

## License
MIT
