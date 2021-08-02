import PySimpleGUI as sg
import config
import sys
import time
import config
from gpiozero import LED
from signal import pause

sg.theme("DarkAmber")
layout = [

            [sg.Text('Vacuum Control by Tiranno', font=("orbitron", 12),size=(25, 1), justification='center')],
            [
                sg.Frame(layout=([[
                    sg.Button(("Start"),key="start", size=(2,1)),sg.Button((""),key="stop", button_color=("white","red"), image_filename="/home/raniero/RaspyVacuum/RaspyVacuum/stop.png", image_size=(80,80)),
                ]]), title="pompa", pad=(3, 1)),
                sg.Frame(layout=([[
                    sg.Button('On', key="on-warm-pump", disabled=False, size=(6, 5), tooltip="accende la pompa per riscaldamento")
                ]]), title="prewarm", pad=(3,1))
            ],
            [
                sg.Frame(layout=([[
                sg.Slider(range =(1,120), default_value=5, orientation='horizontal', key="vacuum-time", size=(20, 15),tooltip='imposta il tempo di vuoto'),
                sg.ProgressBar(120, orientation='h', size=(10, 10), key='progressbar_vac')
                ]]), title="DURATA VUOTO", font=("orbitron", 8),pad=(3, 1)),
            ],
            [
                sg.Frame(layout=([[
                    sg.Slider(range =(1,120), default_value=5, orientation='horizontal', key="soldier-time", size=(20, 15), tooltip='imposta il tempo di sigillatura'),
                    sg.ProgressBar(120, orientation='h', size=(10,10), key='progressbar_sig')
                ]]), title="DURATA SIGILLATURA",font=("orbitron", 8), pad=(3, 1)),
            ],
            [
                sg.Frame(layout=([[
                    sg.Slider(range =(1,120), default_value=5, orientation='horizontal', key="warm-pump-time", size=(20, 15),tooltip='imposta il tempo di preriscaldamento'),
                    sg.ProgressBar(120, orientation='h', size=(10, 10), key='progressbar_pre')
                ]]), title="PRERISCALDAMENTO",font=("orbitron", 8), pad=(3, 1)),
            ],

    ]

win = sg.Window('Vaccum control By Tiranno', layout,[[]], resizable = False, auto_size_buttons=True, margins=(2,2), no_titlebar=True)
progress_bar_vac = win['progressbar_vac']
progress_bar_sig = win['progressbar_sig']
progress_bar_pre = win['progressbar_pre']
