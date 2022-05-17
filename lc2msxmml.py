#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Main source for console command

    The music notation file converter from LovelyComposer jsonl to MSX basic mml.
    Checks caller source whether standard input, and enables variable arguments.
    In case of the piping lcfile argument can be omitted.
    Use [-h] option to see the usage.

    Examples:
        [By console]
        python lc2msxmml.py --start 10 --step 10 --notelen 32 01.jsonl music01.bas
        echo .\02.jsonl | python lc2msxmml.py music02.bas
        [By GUI]
        python lc2msxmml.py
    Note:
        Accept [-h][--help] option to see the usage.
"""

import os
import sys
import argparse
import dearpygui.dearpygui as dpg
from lcutils import Basic
from lcutils import MSXVALS as mv

song = []

def jsonl_callback(sender, app_data):
    """Callback function serving for jsonl selector

    Args:
        sender: caller dearpygui object
        app_data: dearpygui file_diaglog app_data

    Returns:
        None
    """
    if os.path.isfile(app_data['file_path_name']):
        dpg.set_value('jsonl', app_data['file_path_name'])
        dpg.configure_item('convert', enabled=True)
    else:
        dpg.configure_item('convert', enabled=False)


def gen_callback(sender, app_data):
    """Callback function serving for conversion kicker

    Args:
        sender: caller dearpygui object
        app_data: dearpygui button child app_data

    Returns:
        None
    """
    global song
    mb = Basic()
    mb.configure(start = dpg.get_value('startline'), \
        step = dpg.get_value('step'), \
        notelen = dpg.get_value('notelen'), \
        tempo = dpg.get_value('tempo'), \
        volume = dpg.get_value('volume'), \
        extend = dpg.get_value('extend'))
    song = mb.generate(dpg.get_value('jsonl'))
    dpg.set_value('status', ''.join(song))


def bas_callback(sender, app_data):
    """Callback function serving for bas selector

    Args:
        sender: caller dearpygui object
        app_data: dearpygui file_diaglog app_data

    Returns:
        None
    """
    global song
    if not os.path.isdir(app_data['file_path_name']):
        dpg.set_value('bas', app_data['file_path_name'])
        with open(app_data['file_path_name'], 'w', encoding='ascii') as f_out:
            for mml in song:
                f_out.write(mml)


ap = argparse.ArgumentParser()

if sys.stdin.isatty():
    ap.add_argument('lcfile', nargs='?', default='', help='set LovelyComposer music file name', type=str)
ap.add_argument('basfile', nargs='?', default='', help='set target file name', type=str)
ap.add_argument('-s','--start', help='set start line number for target file (1-: default[{0}])'.format(mv.DEFLINE.value), type=int)
ap.add_argument('-p','--step', help='set number of line steps for target file (1-: default[{0}])'.format(mv.DEFSTEP.value), type=int)
ap.add_argument('-l','--notelen', help='set number of note length for target file (1-64: default[{0}])'.format(mv.DEFLEN.value), type=int)
ap.add_argument('-t','--tempo', help='set mml tempo (32-255: default[{0}])'.format(mv.DEFTEMPO.value), type=int)
ap.add_argument('-v','--volume', help='set mml volume (0-15: default[{0}])'.format(mv.DEFVOLUME.value), type=int)
ap.add_argument('-e','--extend', help='use extended basic', action='store_true')

args = ap.parse_args()

lcfile = args.lcfile if hasattr(args, 'lcfile') else input().strip()
basfile = args.basfile

if lcfile == '':

    dpg.create_context()
    dpg.create_viewport(title='lc2msxmml', width=800, height=600)
    dpg.setup_dearpygui()

    with dpg.file_dialog( \
        label='Select LovelyComposer jsonl File', \
        directory_selector=False, \
        show=False, \
        callback=jsonl_callback, \
        file_count=1, \
        tag="jsonl_dialog_tag", \
        width=600, \
        height=400):
        dpg.add_file_extension(".jsonl", color=(0, 255, 0))

    with dpg.file_dialog( \
        label='Designate msx basic File', \
        default_filename='', \
        directory_selector=False, \
        show=False, \
        callback=bas_callback, \
        file_count=1, \
        tag="bas_dialog_tag", \
        width=600, \
        height=400):
        dpg.add_file_extension(".bas", color=(0, 255, 0))

    with dpg.theme() as global_theme:

        with dpg.theme_component(dpg.mvChildWindow):
            dpg.add_theme_color(dpg.mvThemeCol_ChildBg, [60, 60, 255])
            dpg.add_theme_color(dpg.mvThemeCol_TitleBg, [60, 60, 255])
            dpg.add_theme_color(dpg.mvThemeCol_CheckMark, [255, 160, 60])
            dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 5, category=dpg.mvThemeCat_Core)
            dpg.add_theme_style(dpg.mvStyleVar_ChildRounding, 5, category=dpg.mvThemeCat_Core)

        with dpg.theme_component(dpg.mvInputText):
            dpg.add_theme_color(dpg.mvThemeCol_FrameBg, [0, 0, 255])
            dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 5, category=dpg.mvThemeCat_Core)

        with dpg.theme_component(dpg.mvButton, enabled_state=True):
            dpg.add_theme_color(dpg.mvThemeCol_Text, [0, 0, 0])
            dpg.add_theme_color(dpg.mvThemeCol_Button, [0, 255, 155])

        with dpg.theme_component(dpg.mvButton, enabled_state=False):
            dpg.add_theme_color(dpg.mvThemeCol_Text, [0, 0, 0])
            dpg.add_theme_color(dpg.mvThemeCol_Button, [50, 50, 50])

    with dpg.window(label="lc2msxmml_window", tag='primary'):
        with dpg.group(horizontal=False, width=0):
            with dpg.child_window(width=770, height=36):
                with dpg.group(horizontal=True):
                    dpg.add_button(label="SELECT .jsonl", callback=lambda: dpg.show_item("jsonl_dialog_tag"), width=150, height=18)
                    dpg.add_input_text(default_value = '', readonly=True, tag='jsonl', width=595)
            with dpg.group(horizontal=True, width=0):
                with dpg.child_window(width=220, height=465):
                    dpg.add_input_int(label=' START LINE', default_value=mv.DEFLINE.value, tag='startline', width=85, \
                        min_value=1, min_clamped=True, max_value=1000, max_clamped=True, step_fast=10)
                    dpg.add_input_int(label=' STEP', default_value=mv.DEFSTEP.value, tag='step', width=85, \
                        min_value=1, min_clamped=True, max_value=1000, max_clamped=True, step_fast=10)
                    dpg.add_input_int(label=' NOTE LENGTH', default_value=mv.DEFLEN.value, tag='notelen', width=85, \
                        min_value=1, min_clamped=True, max_value=64, max_clamped=True, step_fast=5)
                    dpg.add_input_int(label=' TEMPO', default_value=mv.DEFTEMPO.value, tag='tempo', width=85, \
                        min_value=32, min_clamped=True, max_value=255, max_clamped=True, step_fast=10)
                    dpg.add_input_int(label=' VOLUME', default_value=mv.DEFVOLUME.value, tag='volume', width=85, \
                        min_value=0, min_clamped=True, max_value=15, max_clamped=True)
                    dpg.add_checkbox(label=' Use extended BASIC PLAY', tag='extend')
                    dpg.add_button(enabled=False, label="CONVERT", callback=gen_callback, width = 150, height = 20, tag='convert')
                    dpg.add_loading_indicator(show=False, tag='indicator', color=[200,0,200,255], secondary_color=[30,200,200,100])
                dpg.add_input_text(tag='status', multiline=True, tracked=True, width=540, height=465)
            with dpg.child_window(width=770, height=36):
                with dpg.group(horizontal=True):
                    dpg.add_button(label="SAVE", callback=lambda: dpg.show_item("bas_dialog_tag"), width=150, height=18)
                    dpg.add_input_text(default_value = '', readonly=True, tag='bas', width=595)

    dpg.bind_theme(global_theme)

    dpg.show_viewport()
    dpg.set_primary_window('primary', True)
    dpg.start_dearpygui()
    dpg.destroy_context()

else:
    if not os.path.isfile(lcfile):
        print('Invalid LovelyComposer file name given as {0}.'.format(lcfile))
    elif basfile == '':
        print('The MSX bas file given as empty')
    elif os.path.isdir(args.basfile):
        print('The MSX bas file given as {0}. is directory'.format(args.basfile))
    else:
        with open(args.basfile, 'w', encoding='ascii') as f_out:
            mb = Basic()
            mb.configure(start = args.start if args.start else mv.DEFLINE.value, \
                step = args.step if args.step else mv.DEFSTEP.value, \
                notelen = args.notelen if args.notelen else mv.DEFLEN.value, \
                tempo = args.tempo if args.tempo else mv.DEFTEMPO.value, \
                volume = args.volume if args.volume else mv.DEFVOLUME.value, \
                extend = args.extend)
            song = mb.generate(lcfile)

            for mml in song:
                f_out.write(mml)