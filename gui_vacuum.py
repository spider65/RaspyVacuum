import PySimpleGUI as sg
import sys
import time
from gpiozero import LED
from signal import pause

sg.theme("LightBlue1")
layout = [

            [sg.Text('Vacuum Control by Tiranno', size=(25, 1), justification='center', font=("Helvetica", 15))],
            [
                sg.Frame(layout=([[
                sg.Text(text="OFF",key="pompa", font=("orbitron", 10, 'bold'),background_color="white",text_color='red', size=(60,1), justification='center'),
                ]]), title="STATO MACCHINA",font=("orbitron", 10), pad=(1, 1)),
            ],
            [
                sg.Frame(layout=([[
                    sg.Button(("STOP POMPA"),key="stop",disabled=True, size=(12,4),font=("orbitron", 15), button_color=("white","red")),
                ]]), title="POMPA",font=("orbitron", 12), pad=(5, 5)),
                sg.Frame(layout=([[
                    sg.Button('PREWARM', key="on-warm-pump", disabled=False, size=(12, 4),font=("orbitron", 15), tooltip="accende la pompa per riscaldamento")
                ]]), title="PREWARM", font=("orbitron", 12), pad=(5,5)),
                sg.Frame(layout=([[
                    sg.Button(("SHUTDOWN"),key="shutdown", size=(12,4), font=("orbitron", 15), button_color=("red","white")),
                ]]), title="SISTEMA",font=("orbitron", 12), pad=(5, 5)),
            ],
            [
                sg.Frame(layout=([[
                sg.Slider(range =(1,120), default_value=5, orientation='horizontal', key="vacuum-time", size=(30,20),font=("orbitron", 12),tooltip='imposta il tempo di vuoto'),
                sg.ProgressBar(120, orientation='h', size=(35,25), key='progressbar_vac', bar_color=("red","white"))
                ]]), title="DURATA VUOTO", font=("orbitron",12),pad=(3, 2)),
            ],
            [
                sg.Frame(layout=([[
                    sg.Slider(range =(1,120), default_value=5, orientation='horizontal', key="soldier-time", size=(30,20), font=("orbitron", 12),tooltip='imposta il tempo di sigillatura'),
                    sg.ProgressBar(120, orientation='h', size=(35,25), key='progressbar_sig', bar_color=("red","white"))
                ]]), title="DURATA SIGILLATURA",font=("orbitron", 12), pad=(3, 2)),
            ],
            [
                sg.Frame(layout=([[
                    sg.Slider(range =(1,120), default_value=15, orientation='horizontal', key="warm-pump-time", size=(30, 20),font=("orbitron", 12),tooltip='imposta il tempo di preriscaldamento'),
                    sg.ProgressBar(120, orientation='h', size=(35,25), key='progressbar_pre', bar_color=("red","white"))
                ]]), title="PRERISCALDAMENTO",font=("orbitron", 12), pad=(3,1)),
            ],

    ]

win = sg.Window('Vaccum control By Tiranno', layout,size=(800,480), resizable = False, auto_size_buttons=True, margins=(20,0), no_titlebar=True, element_justification="center", grab_anywhere = True)
progress_bar_vac = win['progressbar_vac']
progress_bar_sig = win['progressbar_sig']
progress_bar_pre = win['progressbar_pre']
stato_pompa = win['pompa']
