#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Main source for console command

    The music notation file converter from LovelyComposer jsonl to MSX basic mml.

   Todo:
    * GUI front end
    * Tempo option
"""

import os
import sys
import argparse
import lcutils as lu

def main():
    """Main function for console command

        Checks caller source whether standard input, and enables variable arguments.
        In case of the piping lcfile argument can be omitted.
        Use [-h] option to see the usage.

        Args:
            lcfile (str): Source LovelyCompoer music file name with path to convert
            basfile (str): Target MSX basic mml file name as the output
            start (int): Start line number for MSX basic list
            step (int): Steps of line interval for MSX basic list
            notelen (int): Designated basic note length in MSX music macro language

        Examples:
            python lc2msxmml.py --start 10 --step 10 --notelen 32 01.jsonl music01.bas
            echo .\02.jsonl | python lc2msxmml.py music02.bas
        
        Note:
            Accept [-h][--help] option to see the usage.
    """

    ap = argparse.ArgumentParser()

    if sys.stdin.isatty():
        ap.add_argument('lcfile', help='set LovelyComposer music file name', type=str)
    ap.add_argument('basfile', help='set target file name', type=str)
    ap.add_argument('--start', help='set start line number for target file', type=int)
    ap.add_argument('--step', help='set number of line steps for target file', type=int)
    ap.add_argument('--notelen', help='set number of note length for target file (1-64: default[32])', type=int)

    args = ap.parse_args()

    lcfile = args.lcfile if hasattr(args, 'lcfile') else input().strip()

    if os.path.isfile(lcfile) and not os.path.isdir(args.basfile):
        start = args.start if args.start else 10
        step = args.step if args.step else 10
        notelen = args.notelen if args.notelen else 32

        with open(args.basfile, 'w', encoding='ascii') as f_out:
            mb = lu.basic()
            song = mb.generate(lcfile, start, step, notelen)

            for mml in song:
                f_out.write(mml)
    else:
        print('Invalid LovelyComposer file name given as {0}.'.format(lcfile))

if __name__ == '__main__':
    main()
