import sys
import time
import config
from gpiozero import LED
from signal import pause
import gui_vacuum
import vacuum_status


gv=gui_vacuum
vs=vacuum_status
start_mock=""

from gpiozero import Device
from gpiozero.pins.mock import MockFactory
import prova_mock
pm=prova_mock
"""start=input()
if start == "p":
    pm.micro.when_pressed=pm.micro_cop_on"""

def done():
    #start=input()
    #if start == "p":
        #pm.micro.when_pressed=pm.micro_cop_on

    while True:
        event, values= gv.win.Read(timeout=0.1)
        value=values
        vt=value['vacuum-time']
        st=value['soldier-time']
        wt=value['warm-pump-time']
        if event=="start": #questo evento va sostituito con lo when_pressed del coperchio
            vacuum_on(vt,st)
        if event == 'on-warm-pump':
            print ("riscaldamento pompa ")
            prewarm(wt)
        if event =="stop":
            print("dovrebbe fermare la fase di vuoto in qualunque punto del ciclo ")

def vacuum_on(vacuum_time,soldier_time):
    if pm.vacuum_valve.value and pm.vacuum_coil.value ==0:
        print("inizio vuoto - accensione pompa")
    else:
        print("anomalia")
    st=soldier_time #solenoid_vacuum.ON = LED(12) #pseudo
    pm.vacuum_valve_on() #solenoid_vacuum.ON = LED(12) #pseudo
    pm.vacuum_coil_on()#coil_actuator_pomp.ON = LED(15) #pseudo
    if pm.vacuum_valve.value and pm.vacuum_coil.value ==1:
        for i in reversed(range(1, int(vacuum_time))):
            gv.progress_bar_vac.UpdateBar((i-1) + 1)
            time.sleep(1 - vacuum_time % 1) # sleep until a whole second boundary
            sys.stderr.write('\r%4d' % i)
    print ("fine vuoto - spegnimento pompa") #DISATTIVAZIONE SOLENOIDE ELETTROVALVOLA RITEGNO E SOLENOIDE TELERUTTORE POMPA con ritardo
    pm.vacuum_valve_off() #solenoid_vacuum.OFF = LED(12) #pseudo
    if pm.vacuum_valve.value ==0:
        print ("fine vuoto - spegnimento pompa")
    time.sleep(1)
    pm.vacuum_coil_off()
    if pm.vacuum_coil.value ==0:
         #coil_actuator_pomp.OFF = LED(15) #pseudo
        soldier_on(st)

def soldier_on(soldier_time):
    print ("inizio sigillatura, accensione saldatore")  #ATTIVAZIONE SOLENOIDE SISTEMA SALDATURA + SOLENOIDE BOBINA TRAFORMATORE RESISTENZE
    pm.soldier_valve_on() #solenoid_soldier.ON = LED(11)
    pm.soldier_coil_on()
    if pm.soldier_valve.value and pm.soldier_coil.value ==1:  #coil_actuator_soldier.ON = LED(18) #pseudo
        for i in reversed(range(1, int(soldier_time))):
            gv.progress_bar_sig.UpdateBar((i-1) + 1)
            time.sleep(1 - soldier_time % 1) # sleep until a whole second boundary
            sys.stderr.write('\r%4d' % i)
    else:
        print ("anomalia sezione saldatura")    #time.sleep(soldier_time)
    pm.soldier_coil_off()
    if pm.soldier_coil.value ==0: #coil_actuator_soldier.OFF = LED(18) #pseudo
        time.sleep(2)
    pm.soldier_valve_off()
    if pm.soldier_valve.value ==0: #soldier_valve.OFF = LED(12) #pseudo
        print("fine sigillatura, spegimento saldatore") #DISATTIVAZIONE SOLENOIDE SISTEMA SALDATURA + SOLENOIDE BOBINA TRAFORMATORE RESISTENZE

    ### QUESTA PARTE DI METODO POTREBBE NON ESSERE NECESSARIA
    print ("apertura valvola vuoto") #ATTIVAZIONE SOLENOIDE ELETTROVALVOLA DI RITEGNO
    pm.vacuum_valve_on() #solenoid_vacuum.ON = LED(12) #pseudo
    pm.soldier_valve_off() #soldier_valve.OFF = LED(12) #pseudo
    time.sleep(1)
    pm.vacuum_valve_off() #solenoid_vacuum.OFF = LED(12) #pseudo

def prewarm(prewarm_time):
    #gv.win["status-vacuum"].Update("preriscaldamento effettuato")
    pm.vacuum_coil_on()
    if pm.vacuum_coil.value == 1: #coil_actuator_pomp.ON = LED(15) #pseudo
        for i in reversed(range(1, int(prewarm_time))):
            gv.progress_bar_pre.UpdateBar((i-1) + 1)
            time.sleep(1 - prewarm_time % 1) # sleep until a whole second boundary
            sys.stderr.write('\r%4d' % i)
        #time.sleep(prewarm_time)
    pm.vacuum_coil_off()
    if pm.vacuum_coil.value == 0:
        #coil_actuator_pomp.OFF = LED(15) #pseudo
        print ("preriscaldamento terminata")
    else:
        print ("anomalia")

done()
#start()
