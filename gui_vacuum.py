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
                    sg.Slider(range =(1,120), default_value=5, orientation='horizontal', key="vacuum-time", size=(20, 15),tooltip='imposta il tempo di vuoto')
                ]]), title="DURATA VUOTO", pad=(3, 1)), sg.Button(("Start"),key="start", size=(2,1)),sg.Button((""),key="stop", button_color=("white","red"), image_filename="/home/raniero/RaspyVacuum/RaspyVacuum/stop.png", image_size=(110,110))
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
                ]]), title="STATO", pad=(3, 0)),

                sg.Frame(layout=([[
                    sg.Text('', key="time-to-end", size=(6, 1), tooltip="visualizza il tempo rimenente")
                ]]), title="Tempo rimanente", pad=(3, 1)),
            ],
    ]

win = sg.Window('Vaccum control By Tiranno', layout,[480,320])

def update():
    win["off-pump"].Update(disabled=False)
    print ("pure qui")
    win["status-vacuum"].Update("IN VUOTO")
    print("e acnche qui")
