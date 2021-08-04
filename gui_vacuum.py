import PySimpleGUI as sg
import config
import sys
import time
import config
from gpiozero import LED
from signal import pause

sg.theme("DarkAmber")
layout = [

            [sg.Text('Vacuum Control by Tiranno', size=(25, 1), justification='center', font=("Helvetica", 15))],
            [
                sg.Frame(layout=([[

                    sg.Button(("STOP POMPA"),key="start", size=(12,5),font=("orbitron", 15), button_color=("white","red")),
                ]]), title="POMPA",font=("orbitron", 12), pad=(5, 5)),
                sg.Frame(layout=([[
                    sg.Button('PREWARM', key="on-warm-pump", disabled=False, size=(12, 5),font=("orbitron", 15), tooltip="accende la pompa per riscaldamento")
                ]]), title="PREWARM", font=("orbitron", 12), pad=(5,5)),
                sg.Frame(layout=([[
                    sg.Button(("SHUTDOWN"),key="shutdown", size=(12,5), font=("orbitron", 15), button_color=("red","white")),
                ]]), title="SISTEMA",font=("orbitron", 12), pad=(5, 5)),
            ],
            [
                sg.Frame(layout=([[
                sg.Slider(range =(1,120), default_value=5, orientation='horizontal', key="vacuum-time", size=(30,30),font=("orbitron", 12),tooltip='imposta il tempo di vuoto'),
                sg.ProgressBar(120, orientation='h', size=(35,30), key='progressbar_vac', bar_color=("red","white"))
                ]]), title="DURATA VUOTO", font=("orbitron",12),pad=(3, 2)),
            ],
            [
                sg.Frame(layout=([[
                    sg.Slider(range =(1,120), default_value=20, orientation='horizontal', key="soldier-time", size=(30,30), font=("orbitron", 12),tooltip='imposta il tempo di sigillatura'),
                    sg.ProgressBar(120, orientation='h', size=(35,30), key='progressbar_sig', bar_color=("red","white"))
                ]]), title="DURATA SIGILLATURA",font=("orbitron", 12), pad=(3, 2)),
            ],
            [
                sg.Frame(layout=([[
                    sg.Slider(range =(1,120), default_value=30, orientation='horizontal', key="warm-pump-time", size=(30, 30),font=("orbitron", 12),tooltip='imposta il tempo di preriscaldamento'),
                    sg.ProgressBar(120, orientation='h', size=(35,30), key='progressbar_pre', bar_color=("red","white"))
                ]]), title="PRERISCALDAMENTO",font=("orbitron", 12), pad=(3,1)),
            ],

                    sg.Slider(range =(1,120), default_value=5, orientation='horizontal', key="vacuum-time", size=(20, 15),tooltip='imposta il tempo di vuoto')
                ]]), title="DURATA VUOTO", pad=(3, 1)), sg.Button(("Start"),key="start", size=(2,1)),sg.Button((""),key="stop", button_color=("white","red"))
            ],
            [
                sg.Frame(layout=([[
                    sg.Slider(range =(1,120), default_value=5, orientation='horizontal', key="soldier-time", size=(20, 15), tooltip='imposta il tempo di sigillatura')
                ]]), title="DURATA SIGILLATURA", pad=(3, 1)),
            ],
            [
                sg.Frame(layout=([[
                    sg.Button('On', key="on-warm-pump", disabled=False, size=(3, 1), tooltip="accende la pompa per riscaldamento"),
                    #sg.Button('Off', key="off-warm-pump", disabled=True, size=(3, 1), tooltip="spegne la pompa per riscaldamento"),
                    sg.Slider(range =(1,120), default_value=5, orientation='horizontal', key="warm-pump-time", size=(20, 15),tooltip='imposta il tempo di preriscaldamento')
                ]]), title="PRERISCALDAMENTO", pad=(3, 1)),
            ],
            [
                sg.Frame(layout=([[
                    sg.Text('PRONTA', key="status-vacuum", size=(25, 1), tooltip="descrive lo stato del sistema")
                ]]), title="STATO", pad=(3, 0))

                sg.Frame(layout=([[
                    sg.Text('', key="time-to-end", size=(6, 1), tooltip="visualizza il tempo rimenente")
                ]]), title="Tempo rimanente", pad=(3, 1)),
            ],
    ]

win = sg.Window('Vaccum control By Tiranno', layout,size=(800,480), resizable = False, auto_size_buttons=True, margins=(20,0), no_titlebar=True, element_justification="center", grab_anywhere = True)
progress_bar_vac = win['progressbar_vac']
progress_bar_sig = win['progressbar_sig']
progress_bar_pre = win['progressbar_pre']