import sys
import time
import config
from gpiozero import LED
from signal import pause
import gui_vacuum
import vacuum_status1
from subprocess import call

gv=gui_vacuum
vs=vacuum_status
start_mock=""
vt=10
st=5

def done():
    while True:
        event, values= gv.win.Read(timeout=0.1)
        value=values
        vt=value['vacuum-time']
        st=value['soldier-time']
        wt=value['warm-pump-time']
        if event == 'on-warm-pump':
            print ("riscaldamento pompa ")
            prewarm(wt)
        if event =="stop":
            print("dovrebbe fermare la fase di vuoto in qualunque punto del ciclo ")
        if event =="shutdown":
            print ("spegimento raspberry")
            sudo_halt()
    #return vt, st

def vacuum_on(): #vacuum_time,soldier_time):
    vt1=vt
    st1=st
    if vs.vacuum_valve.value == 0 and vs.vacuum_coil.value == 0:
        print("inizio vuoto - accensione pompa")
    else:
        print("anomalia valvole vuoto")
    #st=soldier_time #solenoid_vacuum.ON = LED(12) #pseudo
        vs.vacuum_valve_on() #solenoid_vacuum.ON = LED(12) #pseudo
        vs.vacuum_coil_on()#coil_actuator_pomp.ON = LED(15) #pseudo
    if vs.vacuum_valve.value ==1 and vs.vacuum_coil.value ==1:
        for i in reversed(range(1, int(vt1))):
            gv.progress_bar_vac.UpdateBar(i-1)
            time.sleep(1 - vt % 1) # sleep until a whole second boundary
            sys.stderr.write('\r%4d' % i)
    print ("fine vuoto - spegnimento pompa") #DISATTIVAZIONE SOLENOIDE ELETTROVALVOLA RITEGNO E SOLENOIDE TELERUTTORE POMPA con ritardo
    vs.vacuum_valve_off() #solenoid_vacuum.OFF = LED(12) #pseudo
    if vs.vacuum_valve.value ==0:
        print ("fine vuoto - spegnimento pompa")
    time.sleep(1)
    vs.vacuum_coil_off()
    if vs.vacuum_coil.value ==0:
         #coil_actuator_pomp.OFF = LED(15) #pseudo
        soldier_on(st1)

vs.micro_cop.when_pressed=vacuum_on

def soldier_on(soldier_time):
    print ("inizio sigillatura, accensione saldatore")  #ATTIVAZIONE SOLENOIDE SISTEMA SALDATURA + SOLENOIDE BOBINA TRAFORMATORE RESISTENZE
    vs.soldier_valve_on() #solenoid_soldier.ON = LED(11)
    vs.soldier_coil_on()
    if vs.soldier_valve.value ==1 and vs.soldier_coil.value ==1:  #coil_actuator_soldier.ON = LED(18) #pseudo
        for i in reversed(range(1, int(soldier_time))):
            gv.progress_bar_sig.UpdateBar(i-1)
            time.sleep(1 - soldier_time % 1) # sleep until a whole second boundary
            sys.stderr.write('\r%4d' % i)
    else:
        print ("anomalia sezione saldatura")    #time.sleep(soldier_time)
    vs.soldier_coil_off()
    if vs.soldier_coil.value ==0: #coil_actuator_soldier.OFF = LED(18) #pseudo
        time.sleep(2)
    vs.soldier_valve_off()
    if vs.soldier_valve.value ==0: #soldier_valve.OFF = LED(12) #pseudo
        print("fine sigillatura, spegimento saldatore") #DISATTIVAZIONE SOLENOIDE SISTEMA SALDATURA + SOLENOIDE BOBINA TRAFORMATORE RESISTENZE

    ### QUESTA PARTE DI METODO POTREBBE NON ESSERE NECESSARIA
    print ("apertura valvola vuoto") #ATTIVAZIONE SOLENOIDE ELETTROVALVOLA DI RITEGNO
    vs.vacuum_valve_on() #solenoid_vacuum.ON = LED(12) #pseudo
    vs.soldier_valve_off() #soldier_valve.OFF = LED(12) #pseudo
    time.sleep(1)
    vs.vacuum_valve_off() #solenoid_vacuum.OFF = LED(12) #pseudo

def prewarm(prewarm_time):
    #gv.win["status-vacuum"].Update("preriscaldamento effettuato")
    vs.vacuum_coil_on()
    if vs.vacuum_coil.value == 1: #coil_actuator_pomp.ON = LED(15) #pseudo
        for i in reversed(range(1, int(prewarm_time))):
            gv.progress_bar_pre.UpdateBar(i-1)
            time.sleep(1 - prewarm_time % 1) # sleep until a whole second boundary
            sys.stderr.write('\r%4d' % i)
        #time.sleep(prewarm_time)
    vs.vacuum_coil_off()
    if vs.vacuum_coil.value == 0:
        #coil_actuator_pomp.OFF = LED(15) #pseudo
        print ("preriscaldamento terminata")
    else:
        print ("anomalia")
def sudo_halt():
    call("sudo nohup shutdown -h now", shell=True)

done()
