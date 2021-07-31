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
vacuum_valve_on=""
vacuum_valve_off=""
vacuum_coil_on=""
vacuum_coil_off=""
soldier_valve_on=""
soldier_valve_off=""
soldier_coil_on=""
soldier_coil_off=""

def start():
    start=input()
    if start == "m":
        print("mock")
        from gpiozero import Device
        from gpiozero.pins.mock import MockFactory
        import prova_mock
        pm=prova_mock

        if Device.pin_factory is not None:
            Device.pin_factory.reset()
        Device.pin_factory = MockFactory()
        vacuum_valve_on=pm.vacuum_valve_on()
        vacuum_valve_off=pm.vacuum_valve_off()
        vacuum_coil_on=pm.vacuum_coil_on()
        vacuum_coil_off=pm.vacuum_coil_off()
        soldier_valve_on=pm.soldier_valve_on()
        soldier_valve_off=pm.soldier_valve_off()
        soldier_coil_on=pm.soldier_coil_on()
        soldier_coil_off=pm.soldier_coil_off()

        done()

    if start == "w":
        work()
        print ("start work")
        start =input()
        vacuum_valve_on=vs.vacuum_valve_on()
        vacuum_valve_off=vs.vacuum_valve_off()
        vacuum_coil_on=vs.vacuum_coil_on()
        vacuum_coil_off=vs.vacuum_coil_off()
        soldier_valve_on=vs.soldier_valve_on()
        soldier_valve_off=vs.soldier_valve_off()
        soldier_coil_on=vs.soldier_coil_on()
        soldier_coil_off=vs.soldier_coil_off()
        done()

def done():
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
            print("dovrebbe ferrmare la fase di vuoto in qualunque putno sia")

def vacuum_on(vacuum_time,soldier_time):
    gv.win["status-vacuum"].Update("vuoto terminato")
    print("inizio vuoto")
    st=soldier_time#solenoid_vacuum.ON = LED(12) #pseudo
    vacuum_valve_on
    #coil_actuator_pomp.ON = LED(15) #pseudo
    vacuum_coil_on
    while vacuum_time :
        print(vacuum_time)
        print("in fase di sottovuoto") #ATTIVAZIONE SOLENOIDE ELETTROVALVOLA RITEGNO E SOLENOIDE TELERUTTORE POMPA
        #solenoid_vacuum.ON = LED(12) #pseudo
        time.sleep(1)
        vacuum_time  -= 1
    print ("spegnimento pompa") #DISATTIVAZIONE SOLENOIDE ELETTROVALVOLA RITEGNO E SOLENOIDE TELERUTTORE POMPA con ritardo
    #solenoid_vacuum.OFF = LED(12) #pseudo
    time.sleep(0.5)
    #coil_actuator_pomp.OFF = LED(15) #pseudo
    vacuum_coil_off
    soldier_on(st)

def soldier_on(soldier_time):
    gv.win["status-vacuum"].Update("sigillatura terminata")
    print ("solenoid_vacuum.on")  #ATTIVAZIONE SOLENOIDE SISTEMA SALDATURA + SOLENOIDE BOBINA TRAFORMATORE RESISTENZE
    #coil_actuator_soldier.ON = LED(18) #pseudo
    soldier_valve_on
    #solenoid_soldier.ON = LED(11) #pseudo
    soldier_coil_on
    while soldier_time:
        print (soldier_time)
        print("in fase di sigillatura")
        time.sleep(1)
        soldier_time -= 1

    print("solenoid_soldier.off()") #DISATTIVAZIONE SOLENOIDE SISTEMA SALDATURA + SOLENOIDE BOBINA TRAFORMATORE RESISTENZE
    #coil_actuator_soldier.OFF = LED(18) #pseudo
    soldier_coil_off
    print ("sigillatura terminata")
    ### QUESTA PARTE DI METODO POTREBBE NON ESSERE NECESSARIA
    time.sleep(1)
    print ("apertura valvola vuoto") #ATTIVAZIONE SOLENOIDE ELETTROVALVOLA DI RITEGNO
    #solenoid_vacuum.ON = LED(12) #pseudo
    soldier_valve_off
    #time.sleep(1)
    #solenoid_vacuum.OFF = LED(12) #pseudo
    #time.sleep(5)

def prewarm(prewarm_time):
    gv.win["status-vacuum"].Update("preriscaldamento effettuato")
    print("in fase di preriscaldamento") #ATTIVAZIONE SOLENOIDE TELERUTTORE POMPA
    vacuum_coil_on
    #coil_actuator_pomp.ON = LED(15) #pseudo
    while prewarm_time:
        print("in fase di preriscaldamento")
        print (prewarm_time)
        time.sleep(1)
        prewarm_time -= 1
        vacuum_coil_off
    print ("preriscaldamento terminata") #DISATTIVAZIONE SOLENOIDE TELERUTTORE POMPA
    #coil_actuator_pomp.OFF = LED(15) #pseudo
    #pm.vacuum_coil_off()


start()
