#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""MSX mml conversion engine module

    The music notation conversion module from LovelyComposer jsonl to MSX basic mml.

   Todo:
    * MGS file type conversion
    * Extended MSX basic (MSX-MUSIC) mml
    * Volume macro designation by the each note
    * Simple tone reflection functionality in case of MGS/ext-basic mml
    * Note coupling functionality (to be considered)
"""

import json
from enum import Enum

class MMLVALS(Enum):
    """Constants in MUSIC macro language common

    Args:
        SCALES (tuple[int]): Scale macro
        REST (str): Rest macro
        OCTAVE (str): Octave macro
        NUMSCALE (int): The number of single octave
    """
    SCALES = ('C','C+','D','D+','E','F','F+','G','G+','A','A+','B','')
    REST = 'R'
    OCTAVE = 'O'
    LEVEL= 'N'
    NUMSCALE = 12

class LCVALS(Enum):
    """Constants in LovelyComposer world

    Args:
        MINNUM (int): Minimum note scale number
        MAXNUM (int): Maximum note scale number
        NOISEID (tuple[int]): Noise tone IDs
        CH (str): LC jsonl channel label
        SL (str): LC jsonl sound list label
        VL (str): LC jsonl voice list label
        PN (str): LC jsonl label for number of play notes per single page
        N (str): LC jsonl note level label
        ID (str): LC jsonl note ID label
        LCVO (str): LC jsonl LCVoice tag label
    """
    MINNUM = 24
    MAXNUM = 107
    NOISEID = (3, 7, 15, 33)
    CH = 'channels'
    SL = 'sl'
    VL = 'vl'
    PN = 'play_notes'
    N = 'n'
    ID = 'id'
    LCVO = '__LCVoice__'

class MSXVALS(Enum):
    """Constants in MSX mml world

    Args:
        SMASK (int): Register mask for sound
        NMASK (int): Register mask for noise
        ALLMASK (int): Whole mixer register mask
        LINENOTES (int): Number of notes in single line per one channel
        CHANNELS (int): Capable channels, intended for PSG
        DEFLINE (int): Default number of start line
        DEFSTEP (int): Default number of line step
        DEFLEN (int): Default note length
        DEFTEMPO (int): Default tempo
        DEFVOLUME (int): Default volume
    """
    SMASK = 0b000001
    NMASK = 0b001000
    ALLMASK = 0b111111
    LINENOTES = 8
    CHANNELS = 3
    DEFLINE = 10
    DEFSTEP = 10
    DEFLEN = 16
    DEFTEMPO = 140
    DEFVOLUME = 12

class Basic:
    """Conversion features for MSX basic mml

        Constraints
            * For PSG conversion it does not support application of tone.
            * Assign note scale to MSX mml O1-O7 (O8 is not used).
            * Assign same volume level for all channels.
            * Currently it is not supported coupling of note duration.
              This is in some meaning reflecting original LC spec as is.
    """
    def __init__(self):
        """Initialization
        """
        self.lcsong = {}
        self.notes = []
        self.mml = []
        self._line = MSXVALS.DEFLINE.value
        self._step = MSXVALS.DEFSTEP.value
        self._mixer = MSXVALS.ALLMASK.value
        self._notelen = MSXVALS.DEFLEN.value
        self._tempo = MSXVALS.DEFTEMPO.value
        self._volume = MSXVALS.DEFVOLUME.value
        self._extend = False
        self._nmacro = False
    
    def clear(self):
        """Set all members to default
        """
        self.lcsong.clear()
        self.notes.clear()
        self.mml.clear()
        self._line = MSXVALS.DEFLINE.value
        self._step = MSXVALS.DEFSTEP.value
        self._mixer = MSXVALS.ALLMASK.value
        self._notelen = MSXVALS.DEFLEN.value
        self._tempo = MSXVALS.DEFTEMPO.value
        self._volume = MSXVALS.DEFVOLUME.value
        self._extend = False
        self._nmacro = False

    def read(self, lcfile):
        """Read LovelyComposer single song as the dictionary object.

            The data shall be stored to self.lcsong[].

        Args:
            lcfile (str): The path of LovelyComposer source file
        """
        self.lcsong.clear()
        with open (lcfile, 'r', encoding='utf-8') as f:
            #Ignore first line because of LC file header
            f.readline()
            self.lcsong = json.load(f)

    def configure(self, \
        start: int=MSXVALS.DEFLINE.value, \
        step: int=MSXVALS.DEFSTEP.value, \
        notelen: int=MSXVALS.DEFLEN.value, \
        tempo: int=MSXVALS.DEFTEMPO.value, \
        volume: int=MSXVALS.DEFVOLUME.value, \
        extend: bool=False, \
        nmacro: bool=False, \
        ):
        """Configure conversion parameters

            * Unless call either clear() or configure() method these parameters shall be maintained.

        Args:
            start (int): Start line number for MSX basic list
            step (int): Steps of line interval for MSX basic list
            notelen (int): Designated basic note length in MSX music macro language
            tempo (int): Designated tempo in MSX music macro language
            volume (int): Designated volume for all channel in MSX music macro language
            extend (bool): Use exnteded basic for play syntax

        Returns:
            list[str]: Entire playable MSX mml as the conversion result
        """
        self._line = start
        self._step = step
        self._notelen = notelen
        self._tempo = tempo
        self._volume = volume
        self._extend = extend
        self._nmacro = nmacro

    def num2macro(self, num):
        """Conversion from LC num item to MML notation macro

        Args:
            num (int): LovelyComposer 'n' item

        Returns:
            tuple[str]: macro[octave or rest], value[note length or octave level] and scale char(s)
        """
        macro = MMLVALS.REST.value
        value = str(self._notelen)
        index = MMLVALS.NUMSCALE.value

        if type(num) == int:
            if self._nmacro:
                value = str(int(num - LCVALS.MINNUM.value))
                macro = MMLVALS.LEVEL.value
            else:
                value = str(int((num - LCVALS.MINNUM.value)/MMLVALS.NUMSCALE.value)+1)
                macro = MMLVALS.OCTAVE.value
                index = (num-MMLVALS.NUMSCALE.value)%MMLVALS.NUMSCALE.value
        scale = MMLVALS.SCALES.value[index]

        return macro, value, scale

    def lc2mml(self, lcsong={}):
        """Core function converting LovelyComposer song data to MSX MML list by the channel sort

            The result mml shall be stored to self.notes[] by the channel.
            This function just converts LC notes to simple MSX notes.

        Args:
            lcsong[dict]: LC song data dictionary except of jsonl header context.
        """
        if any(lcsong):
            self.lcsong = lcsong

        self.notes.clear()

        smask = MSXVALS.SMASK.value
        nmask = MSXVALS.NMASK.value

        channels = self.lcsong[LCVALS.CH.value][LCVALS.CH.value]

        for c in range(MSXVALS.CHANNELS.value):
            voicelist = channels[c][LCVALS.SL.value]
            barstrs = []
            comparison = ''

            for b in range(len(voicelist)):
                bar = voicelist[b][LCVALS.VL.value]
                barstr = []

                for n in range(voicelist[b][LCVALS.PN.value]):
                    note = bar[n]

                    if note[LCVALS.LCVO.value]:
                        macro, value, scale = self.num2macro(note[LCVALS.N.value])

                        #Secure last octave level to save octave macro usage
                        if macro == MMLVALS.OCTAVE.value:
                            if value == comparison:
                                macro = ''
                                value = ''
                            else:
                                comparison = value

                        barstr.append('{0}{1}{2}'.format(macro, value, scale))

                        #Evaluate single note for mixing register one by one as auto detection
                        if note[LCVALS.ID.value] != None:
                            if note[LCVALS.ID.value] in LCVALS.NOISEID.value:
                                self._mixer &= ~nmask
                            else:
                                self._mixer &= ~smask
                        
                        #Separate mml by 8 notes because of MSX BASIC line constraints
                        if n % MSXVALS.LINENOTES.value == MSXVALS.LINENOTES.value-1:
                            barstrs.append(''.join(barstr))
                            barstr.clear()

                if len(barstr) > 0:
                    barstrs.append(''.join(barstr))
                    barstr.clear()

            smask <<= 1
            nmask <<= 1

            self.notes.append(barstrs)

    def generate(self):
        """The series of conversion

            * Call conversion core function.
            * 'SOUND' for mixing, 'PLAY' syntaxes and line numbers are added.

        Args:
            lcfile (str): The path of LovelyComposer source file

        Returns:
            list[str]: Entire playable MSX mml as the conversion result
        """
        self.mml.clear()

        self.lc2mml()

        row = self._line

        #Append initial settings
        if self._extend:
            self.mml.append('{0} _MUSIC\n'.format(row))
            row += self._step
        self.mml.append('{0} SOUND7,&B{1}\n'.format(row, format(self._mixer, '06b')))
        row += self._step
        play = 'PLAY#0,' if self._extend else 'PLAY'
        self.mml.append('{0} {1}\"T{2}V{3}L{4}\",\"T{2}V{3}L{4}\",\"T{2}V{3}L{4}\"\n'.format( \
            row, play, self._tempo, self._volume, self._notelen))
        row += self._step

        #Append actual notes by sorting 1 bar from the list of 3 channels
        _line = []
        for n in range(len(self.notes[0])):
            for m in range(MSXVALS.CHANNELS.value):
                _line.append('\"{0}\"'.format(self.notes[m][n]))
            self.mml.append('{0} {1}{2}\n'.format(row, play, ','.join(_line)))
            _line.clear()
            row += self._step

        return self.mml