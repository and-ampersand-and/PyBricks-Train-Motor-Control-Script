# -----------------------------------------------
#  Set user defined values
# -----------------------------------------------

observeChannel = 1    # channel number to observe (0 to 255). Needs to match the value the primary hub is broadcasting on.

# define direction of motors

dirMotorA = 1       # Direction 1 or -1
dirMotorB = -1       # Direction 1 or -1

lightValue = 0      # the initial light value, any number between 0 and 100. This will get overridden by the broadcast hub

# -----------------------------------------------
#  Import classes and functions
# -----------------------------------------------

from pybricks.pupdevices import DCMotor, Motor, Light
from pybricks.parameters import Port, Stop, Button, Color
from pybricks.hubs import CityHub
from pybricks.tools import wait, StopWatch
from pybricks.iodevices import PUPDevice
from uerrno import ENODEV

# ----observe -----------------------------------------

def observe():
    global v
    global lightValue

    data = hub.ble.observe(observeChannel)

    if data is None:
        # No data has been received in the last 1 second.
        hub.light.on(Color.YELLOW)
        print('received nothing')
    else:
        # Data was received and is less that one second old.
        hub.light.on(Color.GREEN)

        speed, light = data

        v = speed
        lightValue = light

        drive()
        updateLights()

        print(lightValue)


# -----------------------------------------------
# updateLights
# -----------------------------------------------

def updateLights():
    global lightValue

    if hasLights:
        for x in range(1,3):
            if motor[x].getType() == "Light":
                if lightValue == min:
                    motor[x].obj.off()
                else:
                    motor[x].obj.on(lightValue)

# ----drive -------------------------------------------

def drive():
    global vold
    global v

    if vold != v:
        # for each motor 1,2 
        for x in range(1,3):
            # set speed and direction
            s = v*round(motor[x].getDir())
            # real motor commands depending on motor type
            if motor[x].getType() == "Motor" :
                motor[x].obj.run(s*motor[x].getSpeed()) #  in 2.7
            if motor[x].getType() == "DCMotor" : 
                motor[x].obj.dc(s) 
            if v == 0 and (motor[x].getType() == "Motor" or motor[x].getType() == "DCMotor"):  
                print("stop",x)
                motor[x].obj.stop()      
        vold = v
        
# ----portcheck -------------------------------------------

def portcheck(i):
    # list of motors, 1 +2 contain string "DC"
    devices = {
    1: "Wedo 2.0 DC Motor",
    2: "Train DC Motor",
    8: "Light",
    38: "BOOST Interactive Motor",
    46: "Technic Large Motor",
    47: "Technic Extra Large Motor",
    48: "SPIKE Medium Angular Motor",
    49: "SPIKE Large Angular Motor",
    75: "Technic Medium Angular Motor",
    76: "Technic Large Angular Motor",
}
    port = motor[i].getPort()
    # Try to get the device, if it is attached.
    try:
        device = PUPDevice(port)
    except OSError as ex:
        if ex.args[0] == ENODEV:
            # No device found on this port.
            motor[i].setType("---")
            print(port, ": not connected")
            return ("---")
        else:
            raise

    # Get the device id
    id = device.info()['id']
    
    # Look up the name.
    try:
        # get the attributes for tacho motors
        if "Motor" in devices[id] and not("DC" in devices[id]): 
            motor[i].setType("Motor")
            motor[i].obj = Motor(port)

            #new in 2.7
            # if motor[x].getDir() != 0 and motor[x].getType() == "Motor" : motor[x].obj.run(s*motor[x].getSpeed()) #  in 2.7
            devs_max_speed = {38:1530,46:1890,47:1980,48:1367,49:1278,75:1367,76:1278 }
            dspeed = devs_max_speed.get(PUPDevice(port).info()['id'], 1000)
            motor[i].obj.stop()
            motor[i].obj.control.limits(speed=dspeed,acceleration=10000)
            motor[i].setSpeed(dspeed/100*0.9)

        # and set type for simple DC Motors    
        if "DC" in devices[id]:
            motor[i].setType("DCMotor")
            motor[i].obj = DCMotor(port)

        if "Light" in devices[id]:
            motor[i].setType("Light")
            motor[i].obj = Light(port)
            if lightValue > 0:
                motor[i].obj.on(lightValue)

            global hasLights
            hasLights = True

        wait(100)    
        print ("--")
        print(port, ":", devices[id], motor[i].getType(),motor[i].getSpeed(),motor[i].getAcc())
    except KeyError:
        motor[i].setType("unkown")
        print(port, ":", "Unknown device with ID", id)
        
# ---- device  -------------------------------------------
    
class device():
    # store the device infos for each motor
    def __init__(self,port,dir):
        self.port = port
        self.dir = dir
        self.type=""
        self.speed=99
        self.acc=99
        self.obj=""
                
    def setType(self,x) : self.type = x
    def setSpeed(self,x): self.speed = x
    def setAcc(self,x)  : self.acc = x
    
    def getType(self)   : return self.type
    def getPort(self)   : return self.port
    def getDir(self)    : return self.dir
    def getSpeed(self)  : return self.speed
    def getAcc(self)    : return self.acc

# -----------------------------------------------
# globals
# -----------------------------------------------

v = 0
vold = 0

# -----------------------------------------------
# Ininitialize
# -----------------------------------------------

hub = CityHub(observe_channels=[observeChannel])

#define motors
motor = [0,0,0]
motor[1] = device(Port.A,dirMotorA)
motor[2] = device(Port.B,dirMotorB)

hasLights = False

# get the port properties
portcheck(1)
portcheck(2)


# -----------------------------------------------
# main loop
# -----------------------------------------------

while True:

    observe()

    wait(10)
    