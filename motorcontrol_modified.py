# -----------------------------------------------
# MotorControl
#
# uses https://code.pybricks.com/ , LEGO City hub, LEGO remote control
# connect 1 or 2 motors of any kind to Port A and/or B
#
# Version 2_9
# -----------------------------------------------/
from pybricks.parameters import * # Color

# -----------------------------------------------
#  Set user defined values
# -----------------------------------------------

# define the two profiles
# profil_x = (minimun speed,maximum Speed,accelerate in steps of ..., wait for next acceleration(in ms)

Profil_A = (20,100,10,100)  #min,max,step,acc
Profil_B = (10,500,5,200)   #min,max,step,acc

# define direction of motors

dirMotorA = 1       # Direction 1 or -1
dirMotorB = -1       # Direction 1 or -1

autoacc = False      # accelarate continously when holding butten 

lightValue = 0      # the initial light value, any number between 0 and 100

shouldBroadcast = False    # whether the hub should broadcast data for a second hub to observe

broadcastChannel = 1    # channel number to broadcast on (0 to 255). Needs to match the value the second hub is observing.

# -----------------------------------------------
#  Set general values
# -----------------------------------------------

# assign buttons to function1 
# syntax: function = "name"
# name may  be "A+","A-","A0","B+","B-","B0","CENTER"

UP = "A+"
DOWN = "A-"
STOP = "A0"
SWITCH = "CENTER"
BUP = "B+"
BDOWN = "B-"
BSTOP = "B0"

mode=1              # start with function number...
watchdog = False    # "True" or "False": Stop motors when loosing remote connection
remoteTimeout =10   # hub waits x seconds for remote connect after starting hub
remoteName = ""     # connect this remote only

# Color and brightness of Hub LEDs
LEDconn = Color.GREEN*0.3       # if Hub connected, color * brightness
LEDnotconn = Color.RED*0.5      # if Hub is not connect, color * brightness

LED_A = Color.GREEN*0.3       # Remote Profil_A, color * brightness
LED_B = Color.RED*0.5      # Remote Profil_B, color * brightness

# -----------------------------------------------
#  Import classes and functions
# -----------------------------------------------

from pybricks.pupdevices import DCMotor, Motor, Remote, Light
from pybricks.parameters import Port, Stop, Button, Color
from pybricks.hubs import CityHub
from pybricks.tools import wait, StopWatch
from pybricks.iodevices import PUPDevice
from uerrno import ENODEV

# -----------------------------------------------
#  function 1 / drive motors
# -----------------------------------------------

def function1():

    vmax = profile[mode].vmax
    vmin = profile[mode].vmin
    accdelay =  profile[mode].acc
    step = profile[mode].step
  
    global v
   
    if CheckButton(UP) and not CheckButton(STOP) : 
        for x in range (1, step + 1):
            v = v + 1
            if v > vmax :
                v = vmax
            if v > 0 and v < vmin:    
                v = vmin
            if abs(v) < vmin:
                v = 0
            drive()
            wait (accdelay)  
            if v==0: 
                break 
        # further acceleration if button keeps pressed
        while autoacc == False and CheckButton(UP) :    
            wait (100)
        # avoid changing direction when reaching "0"     
        while v == 0 and  CheckButton(UP):  
            wait (100)

    if CheckButton(DOWN) and not CheckButton(STOP):
        for x in range (1, step + 1):
            v = v-1
            if v < vmax*-1 :
                v = vmax*-1
            if v < 0 and v > vmin*-1:    
                v = vmin*-1
            if abs(v) < vmin :
                v = 0   
            drive()
            wait (accdelay)  
            if v==0: 
                break 
        # further acceleration if button keeps pressed
        while autoacc == False and CheckButton(DOWN) :    
            wait (100)
        # avoid changing direction when reaching "0"
        while v == 0 and  CheckButton(DOWN) :    
            wait (100)
  
    if CheckButton(STOP): 
        v = 0
        drive()
        wait (100)    
        
class setprofile():
    def __init__(self,pr):
        self.vmin=pr[0]
        self.vmax=pr[1]
        self.step=pr[2]
        self.acc=pr[3]

profile = [0,0,0]
profile[1] = setprofile(Profil_A)
profile[2] = setprofile(Profil_B)

# -----------------------------------------------
#  function 2
# -----------------------------------------------
           
'''
def function2():
    if CheckButton(UP):
        timer[1].set(3000)
    if timer[1].check(): 
        print("Do something")
'''

# -----------------------------------------------
# updateLights
# -----------------------------------------------

def updateLights():
    global lightValue
    max = 100;
    min = 0;
    step = 10;

    waitBetweenSteps = 0;

    if CheckButton(BUP) and not CheckButton(BSTOP) :
        waitBetweenSteps = 100
        lightValue += step

    if CheckButton(BDOWN) and not CheckButton(BSTOP) :
        waitBetweenSteps = 100
        lightValue -= step

    if CheckButton(BSTOP) :
        waitBetweenSteps = 300
        if lightValue == min :
            lightValue = max
        else :
            lightValue = min
    
    if lightValue > max:
        lightValue = max
    if lightValue < min:
        lightValue = min
    
    for x in range(1,3):
        if motor[x].getType() == "Light":
            if lightValue == min:
                motor[x].obj.off()
            else:
                motor[x].obj.on(lightValue)

    wait (waitBetweenSteps)


# -----------------------------------------------
# general program routines and classes
# -----------------------------------------------

# ----CheckButton -------------------------------------------

def CheckButton(x):
    try:
        button = remote.buttons.pressed()
        if x == "A+"  : x = Button.LEFT_PLUS
        if x == "A-" : x = Button.LEFT_MINUS
        if x == "A0"  : x = Button.LEFT

        if x == "B+"  : x = Button.RIGHT_PLUS
        if x == "B-" : x = Button.RIGHT_MINUS
        if x == "B0"  : x = Button.RIGHT
    
        if x == "CENTER"  : x = Button.CENTER
        
        if x in button:
            return True
        else:
            return False
    except:
        return()

# ----delay -------------------------------------------

class delay:
    def __init__(self,id,time=0,watch=StopWatch(),busy=False):
        self.id=id
        self.time=time
        self.watch=watch
        self.busy=busy
        print ("Init Timer",id)
    # set a timer        
    def set(self,x):
        if  self.busy == False:
            self.busy = True
            self.watch.reset()
            self.time = x
            print("Timer",timer[1].id, "set to",x)
    #check if timer is reached, then return "True"
    def check(self):
        if self.busy == True:
            if self.watch.time() > self.time:
                self.busy = False
                self.time=0 
                print("Timer",timer[1].id, "stopped")
                return(True)
        else:
            return(False)

# ----drive -------------------------------------------

def drive():
    global vold
    global v
    print (v)
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
            #if motor[x].getDir() != 0 and motor[x].getType() == "DCMotor" : motor[x].obj.dc(s) 
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
    

# ---- broadcast -----------------------------------------

def broadcastData():
    global v

    data = ( v )
    hub.ble.broadcast(data)


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
#remoteConnected = False

# -----------------------------------------------
# Ininitialize
# -----------------------------------------------

hub = CityHub(broadcast_channel=broadcastChannel)

#define timers
timer = [0,0,0]
timer[1] = delay(1)
timer[2] = delay(2)
           
#define motors
motor = [0,0,0]
motor[1] = device(Port.A,dirMotorA)
motor[2] = device(Port.B,dirMotorB)

hasLights = False

# get the port properties
portcheck(1)
portcheck(2)    

# -----------------------------------------------
# remote connect
# -----------------------------------------------

hub.light.on(Color.RED)
print (hub.system.name())
try:
    remote = Remote(name=remoteName,timeout=remoteTimeout*1000)
except OSError as ex:
    hub.system.shutdown()

# -----------------------------------------------
# main loop
# -----------------------------------------------

while True:
   
    # --check if remote is connected ---------------------------------
    
    try:
        button = remote.buttons.pressed()
        hub.light.on(LEDconn)
        remoteConnected = True
    except OSError as ex:
        hub.light.on(LEDnotconn)
        print("Remote not connected")
        remoteConnected = False
       
        if watchdog == True:
            v=0
            drive()
        try:
            # reconnect remote
            remote = Remote(timeout=1000)
            wait(100)
            print("Remote reconnected")
            remoteConnected = True
        except OSError as ex:
            print("Remote not connected")

            
    if CheckButton(SWITCH):
        mode = mode+1
        if mode > 2: 
            mode = 1
        print (mode)
        if mode == 1 : remote.light.on(LED_A)
        if mode == 2 : remote.light.on(LED_B)    
   
        while CheckButton(SWITCH):
            button = remote.buttons.pressed()
            wait (100)

    if mode == 1 : function1()     
    if mode == 2 : function1()

    if hasLights : updateLights()

    if shouldBroadcast : broadcastData()
    
    wait(10)
    