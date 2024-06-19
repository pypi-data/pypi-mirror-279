#!/usr/bin/python3
# -*- coding: utf-8 - *-

# Copyright (c) 2020 Romeet Chhabra

# Permission is hereby granted, free of charge, to any person obtatomlng a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


__author__ = "Romeet Chhabra"
__copyright__ = "Copyright 2020, Romeet Chhabra"
__license__ = "MIT"

import argparse
import os
import shutil
import site
import sys
import time
from configparser import ConfigParser
from pathlib import Path
from stat import filemode


# https://en.wikipedia.org/wiki/ANSI_escape_code
def _print_format_table():
    for style in range(9):
        for fg in range(30, 40):
            s1 = ''
            for bg in range(40, 50):
                fmt = ';'.join([str(style), str(fg), str(bg)])
                s1 += f'\x1b[{fmt}m {fmt} \x1b[0m'
            print(s1)
        print('\n')


def get_config():
    config = ConfigParser()
    config.read([
                os.path.join(sys.prefix, 'colorls/config/colorls.toml'),
                os.path.join(site.USER_BASE, 'colorls/config/colorls.toml'),
                os.path.expanduser('~/.config/colorls/colorls.toml'),
                os.path.expanduser('~/.colorls.toml'),
                os.path.join(Path(__file__).parent.absolute(), 'config/colorls.toml'),
                ], encoding='utf8')
    return dict(config['FORMATTING']), dict(config['ICONS']), dict(config['ALIASES']), dict(config['SUFFIXES'])


ANSI, ICONS, ALIAS, SUFFIX = get_config()


if sys.platform.startswith('linux') or sys.platform.startswith('darwin'):
    from pwd import getpwuid
    from grp import getgrgid
    UID_SUPPORT = True
else:
    UID_SUPPORT = False


METRIC_PREFIXES = ['b', 'K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y']
METRIC_MULTIPLE = 1024.
SI_MULTIPLE = 1000.


def get_human_readable_size(size, base=METRIC_MULTIPLE):
    for pre in METRIC_PREFIXES:
        if size < base:
            return f"{size:4.0f}{pre}"
        size /= base


def get_keys(path):
    n, ext = path.stem.lower(), path.suffix.lower()
    if ext == '':
        ext = n             # Replace ext with n if ext empty
    if ext.startswith('.'):
        ext = ext[1:]       # Remove leading period

    if path.is_symlink():
        key1 = "link"
    elif path.is_dir():
        key1 = "dir"
    elif path.is_mount():
        key1 = "mount"
    elif n.startswith('.'):
        key1 = "hidden"
    elif path.is_file():
        key1 = "file"
        if filemode(os.stat(path).st_mode)[3] == 'x':
            key1 = "exec"
    else:
        key1 = "none"

    if ext in ALIAS:
        if ALIAS[ext] in ANSI:
            key1 = ALIAS[ext]
        key2 = ALIAS[ext]
    else:
        key2 = key1
    return key1.lower(), key2.lower()


def print_tree_listing(path, level=0, inode=False, suff=False,
                       format_override=None, display_icons=True):
    tree_str = "   |   " * level + "   " + "---"
    print(tree_str, end="")
    print_short_listing(path, inode=inode, expand=True, suff=suff,
                        format_override=format_override,
                        display_icons=display_icons, end='\n')


def print_long_listing(path, is_numeric=False, use_si=False, inode=False, timefmt=None, 
                       suff=False, format_override=None, display_icons=True):
    try:
        st = path.stat()
        size = st.st_size
        sz = get_human_readable_size(size, SI_MULTIPLE if use_si else METRIC_MULTIPLE)
        mtime = time.localtime(st.st_mtime)
        if timefmt:
            mtime = time.strftime(timefmt, mtime)
        else:
            mtime = time.strftime(f"%b %-d {'%H:%M' if time.strftime('%Y') == time.strftime('%Y', mtime) else ' %Y'}", mtime)
        mode = os.path.stat.filemode(st.st_mode)
        ug_string = ""
        if UID_SUPPORT:
            uid = getpwuid(st.st_uid).pw_name if not is_numeric else str(st.st_uid)
            gid = getgrgid(st.st_gid).gr_name if not is_numeric else str(st.st_gid)
            ug_string = f"{uid:4} {gid:4}"
        hln = st.st_nlink

        ino = f"{path.stat().st_ino : 10d} " if inode else ""

        print(f"{ino}{mode} {hln:3} {ug_string} {sz} {mtime} ", end="")
        print_short_listing(path, expand=True, suff=suff,
                            format_override=format_override,
                            display_icons=display_icons, end='\n')
    except FileNotFoundError:
        ...


def print_short_listing(path, inode=False, expand=False, suff=False,
                        format_override=None, sep_len=None, display_icons=True,
                        end=''):
    fmt, ico = format_override if format_override else get_keys(path)
    name = path.name + (SUFFIX.get(fmt, '') if suff else '')
    ino = f"{path.stat().st_ino : 10d}" if inode else ""
    sep_len = sep_len if sep_len else len(name)
    icon_str = f" {ICONS.get(ico, '')}  " if display_icons else ""
    if expand and path.is_symlink():
        name += " -> " + str(path.resolve())
    print(f"{ino}\x1b[{ANSI[fmt]}m{icon_str}{name:<{sep_len}}\x1b[0m", end=end)


def process_dir(directory, args, level=0, size=None):
    end = '\n' if vars(args)['1'] else ''
    contents = list()

    try:
        p = Path(directory)
        if p.exists():
            if p.is_dir():
                if args.header and level == 0:
                    print()
                    print_short_listing(p.absolute(), inode=args.inode,
                                    format_override=('this', 'this'),
                                    display_icons=args.x, end=':\n')
                contents = list(p.iterdir())
                if args.ignore:
                    remove_list = list(p.glob(args.ignore))
                    contents = [c for c in contents if c not in remove_list]
            elif p.is_file():
                contents = [p]
        else:
            print(f"lx: {p}: No such file or directory")
            sys.exit(1)
    except Exception as e:
        print(e, file=sys.stderr)
        if level == 0:
            sys.exit(1)

    if args.directory:
        entries = [x for x in contents if x.is_dir()]
    elif args.file:
        entries = [x for x in contents if x.is_file()]
    else:
        entries = contents

    if not args.unsorted:
        entries = sorted(entries)

    # Since the single line printing is row based, the longest entry is needed
    # to ensure no overlap Additional padding of 3 added to length for better
    # differentiation between entries (aesthetic choice)
    longest_entry = (max([len(str(x.name)) for x in entries])
                     if len(entries) > 0 else 0) + 3
    if longest_entry and size:
        # Additional padding when calculating number of entries
        # Padding of 4 to account for icons as used in print_short_listing
        # (<space><icon><space><space>) Padding of 11 to account for inode
        # printing (<inode aligned to 10 units><space>)
        max_items = (
                size[0] //
                (longest_entry +
                    (4 if not args.x else 0) +
                    (11 if args.inode else 0)
                )
        )
    else:
        # If size of terminal or size of file list can not determined, default
        # to one item per line
        max_items = 0

    run = 0
    subdirs = []
    for path in entries:
        if path.is_dir():
            subdirs.append(path)
        if (not args.all) and path.name.startswith('.'):
            if path.is_dir():
                subdirs.remove(path)
            continue
        if args.ignore_backups and path.name.endswith('~'):
            continue
        if args.long or args.numeric_uid_gid:
            print_long_listing(path, is_numeric=args.numeric_uid_gid,
                               use_si=args.si, inode=args.inode,
                               suff=args.classify, display_icons=args.x)
        elif args.tree and args.tree > 0:
            print_tree_listing(path, level=level, inode=args.inode,
                               suff=args.classify, display_icons=args.x)
            if path.is_dir() and level < args.tree - 1:
                process_dir(path, args, level=level + 1, size=size)
        else:
            print_short_listing(path, inode=args.inode, sep_len=longest_entry,
                                suff=args.classify, display_icons=args.x, end=end)
            run += 1
            if run >= max_items:
                print()
                run = 0

    if args.recursive and not args.tree:
        for sub in subdirs:
            print()
            if not args.header:
                print_short_listing(sub.absolute(), inode=args.inode,
                                format_override=('this', 'this'),
                                display_icons=args.x, end=':\n')
            process_dir(sub, args, size=size)


def main():
    parser = argparse.ArgumentParser(
        description=("Pure Python implementation of `ls` command. "
                     "Only a subset of available arguments are implemented"),
        epilog=("Feature Requests/Bugs should be reported at "
                "https://gitlab.com/compilation-error/colorls/-/issues")
    )

    parser.add_argument("-1", action="store_true", default=False,
                        help="list items on individual lines")
    parser.add_argument("-a", "--all", action="store_true", default=False,
                        help="do not ignore entries starting with .")
    parser.add_argument("-B", "--ignore-backups", action="store_true", default=False,
                        help="do not list implied entries ending with ~")
    parser.add_argument("-d", "--directory", action="store_true", default=False,
                        help="list directories themselves, not their contents")
    parser.add_argument("-f", "--file", action="store_true", default=False,
                        help="list files only, not directories")
    parser.add_argument("-F", "--classify", action="store_true", default=False,
                        help="append indicator (one of */=>@|) to entries")
    parser.add_argument("-i", "--inode", action="store_true", default=False,
                        help="display inode number")
    parser.add_argument("-I", "--ignore", metavar="PATTERN",
                        help="do not list implied entries matching shell PATTERN")
    parser.add_argument("-l", "--long", action="store_true", default=False,
                        help="use a long listing format")
    parser.add_argument("-n", "--numeric-uid-gid", action="store_true", default=False,
                        help="like -l, but list numeric user and group IDs")
    parser.add_argument("-R", "--recursive", action="store_true", default=False,
                        help='list subdirectories recursively')
    parser.add_argument("-t", "--tree", metavar="DEPTH", type=int, nargs='?', const=3,
                        help="max tree depth")
    parser.add_argument("--version", action="store_true", default=False,
                        help="display current version number and exit")
    parser.add_argument("--si", action="store_true", default=False,
                        help="display file size in SI units")
    parser.add_argument("-U", "--unsorted", action="store_true", default=False,
                        help="do not sort; list entries in directory order")
    parser.add_argument("-H", "--header", action="store_true", default=False,
                        help="do not display header")
    parser.add_argument("-x", action="store_false", default=True,
                        help="do not display icons")
    parser.add_argument("FILE", default=".", nargs=argparse.REMAINDER,
                        help="List information about the FILE(s).")
    args = parser.parse_args()

    if args is None:
        sys.exit(2)

    if args.version:
        from . import __version__
        print("color-ls version " + __version__)
        sys.exit(0)

    if not args.FILE:
        args.FILE = ["."]

    if len(args.FILE) > 1:
        args.header = True

    term_size = shutil.get_terminal_size()
    for FILE in args.FILE:
        process_dir(FILE, args, size=term_size)
        print()

    return 0


if __name__ == '__main__':
    sys.exit(main())


# vim: ts=4 sts=4 sw=4 et syntax=python:
