from threading import Timer
import random
from functools import wraps
from enum import Enum
import os

GLOBAL_BATTERY_MINIMUM = 20
GLOBAL_BATTERY_WITHDRAWAL_SPEED = 13
GLOBAL_CHARGING_DURATION = 15
GLOBAL_SLEEP_DURATION = 25

# class State (Enum):
#     WORKING = 1 #Device performs, but the battery charge is reduced with pre-defined value
#     CHARGING = 2 #Device continues to perform, but the battery charge is not decreased
#     SLEEPING = 3 #Device does NOT perform, but after pre-defined time it is put into charging mode


status = {
    "battery":100,
    "state": "WORKING"
}

#Annotation for all functions, that use power.
#If the device has enough power or if it's in charging mode, the function works as expected
#and the device status is updated accordingly.
#Otherwise, the function is not called.
def uses_battery(func):
    def function_wrapper(*args, **kwargs):
        #If the defise is not sleeping, perform the requested operation
        #and update the status
        if status["state"] != "SLEEPING":
            func(*args, **kwargs)
        update_status()
    return function_wrapper

#Check the battery status and updates the device state.
def update_status():
    check_battery()
    #If the device is not in a charging mode, reduce the charge
    if status["state"] == "WORKING": 
        reduce_charge()
    
        
#Puts the device in sleeping mode, and after a fixed time back to charging mode
def sleep():
    status["state"] = "SLEEPING"
    t = Timer(GLOBAL_SLEEP_DURATION, charge)
    t.start()

#Charges the device if not full. If full, disables charging
def charge(): 
    status["state"] = "CHARGING"
    t = Timer(GLOBAL_CHARGING_DURATION, wakeup)
    t.start()
#Wakes up the device
def wakeup():
    status["battery"] = 100
    status["state"] = "WORKING"

#Checks the battery charge and put's it either in charging mode 
#or in sleep mode with a fixed probability
def check_battery():
    if status["state"] == "WORKING":
        if status["battery"] <= GLOBAL_BATTERY_MINIMUM:
            should_charge = bool(random.getrandbits(1)) #Determines if device should sleep or put in charge
            if should_charge : 
                charge()
            else :
                sleep()

#Reduce the current charge of the battery
def reduce_charge():
    status["battery"] -= GLOBAL_BATTERY_WITHDRAWAL_SPEED 



#Returns the current state of the device
def get_status():
    return status

