from gpiozero import Device, LED
from gpiozero import Button

from gpiozero.pins.mock import MockFactory
if Device.pin_factory is not None:
    Device.pin_factory.reset()
Device.pin_factory = MockFactory()
#pin35 per segnale relay vaccum valve
vacuum_valve= LED("19")
#pin36 per segnale relay teleruttore pompa
vacuum_coil= LED("16")
#pin37 per segnale relay soldier valve
soldier_valve= LED("26")
#pin38 per segnale relay teleruttore soldier
soldier_coil= LED("20")

#pin 40 per segnale micro coperchio
#micro_cop= Button("21")
micro = Button(21)
#micro_cop.when_pressed = micro_cop_on()

print (vacuum_valve.value, "stato valvola vuoto" )
print (vacuum_coil.value, "stato coil vuoto" )
print (soldier_valve.value, "stato valvola soldier")
print (soldier_coil.value, "stato coil soldier")
print (micro.value, "stato switch coperchio")

def vacuum_valve_on():
    vacuum_valve.on()
    print (vacuum_valve.value,"valvola vuoto aperta")
    #vacuum_valve.pin.drive_high(1)
    return True

def vacuum_valve_off():
    vacuum_valve.off()
    print(vacuum_valve.value,"valvola vuoto chiusa")
    return True

def vacuum_coil_on():
    vacuum_coil.on()
    print(vacuum_coil.value,"teleruttore pompa on")
    return

def vacuum_coil_off():
    vacuum_coil.off()
    print(vacuum_coil.value, "teleruttore pompa off")
    return True

def soldier_valve_on():
    soldier_valve.on()
    print (soldier_valve.value, "valvola saldatura aperta")
    return True

def soldier_valve_off():
    soldier_valve.off()
    print (soldier_valve.value, "valvola saldatura chiusa")
    return True

def soldier_coil_on():
    soldier_coil.on()
    print (soldier_coil.value,"teleruttore saldatura on")
    return True

def soldier_coil_off():
    soldier_coil.off()
    print (soldier_coil.value,"teleruttore saldatura off")
    return True

def micro_cop_on():
    micro.pin.drive_low()
    print (micro.value,"coperchio chiuso")
    return
