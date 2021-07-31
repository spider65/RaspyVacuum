#file per la lettura dello status dei pin del gpio
from gpiozero import LED
from gpiozero import Button
from time import sleep
from gpiozero.pins.mock import MockFactory
from gpiozero import Device

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
micro_cop  = Button("21")
