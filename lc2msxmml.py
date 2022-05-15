#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Main source for console command

    The music notation file converter from LovelyComposer jsonl to MSX basic mml.

   Todo:
    * GUI front end
"""

import os
import sys
import argparse
import lcutils as lu
from lcutils import MSXVALS as mv

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
            tempo (int): Designated tempo in MSX music macro language
            volume (int): Designated volume for all channel in MSX music macro language
            extend (bool): Use exnteded basic for play syntax

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
    ap.add_argument('-s','--start', help='set start line number for target file (1-: default[{0}])'.format(mv.DEFLINE.value), type=int)
    ap.add_argument('-p','--step', help='set number of line steps for target file (1-: default[{0}])'.format(mv.DEFSTEP.value), type=int)
    ap.add_argument('-l','--notelen', help='set number of note length for target file (1-64: default[{0}])'.format(mv.DEFLEN.value), type=int)
    ap.add_argument('-t','--tempo', help='set mml tempo (32-255: default[{0}])'.format(mv.DEFTEMPO.value), type=int)
    ap.add_argument('-v','--volume', help='set mml volume (0-15: default[{0}])'.format(mv.DEFVOLUME.value), type=int)
    ap.add_argument('-e','--extend', help='use extended basic', action='store_true')

    args = ap.parse_args()

    lcfile = args.lcfile if hasattr(args, 'lcfile') else input().strip()

    if not os.path.isfile(lcfile):
        print('Invalid LovelyComposer file name given as {0}.'.format(lcfile))
    elif not os.path.isdir(args.basfile):
        print('The MSX bas file given as {0}. is directory'.format(lcfile))
    else:
        with open(args.basfile, 'w', encoding='ascii') as f_out:
            mb = lu.basic()
            mb.configure(start = args.start if args.start else mv.DEFLINE.value, \
                step = args.step if args.step else mv.DEFSTEP.value, \
                notelen = args.notelen if args.notelen else mv.DEFLEN.value, \
                tempo = args.tempo if args.tempo else mv.DEFTEMPO.value, \
                volume = args.volume if args.volume else mv.DEFVOLUME.value, \
                extend = args.extend)
            song = mb.generate(lcfile)

            for mml in song:
                f_out.write(mml)

if __name__ == '__main__':
    main()
