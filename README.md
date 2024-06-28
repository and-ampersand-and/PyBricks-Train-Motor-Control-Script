# PyBricks-Train-Motor-Control-Script

This script allows you to control Lego Trains via PyBricks without using the official Powered Up App.

The original version of this script was written by Eurobrick user Lok24. It automatically detects what motors your hub is using and provides a number of quality of life improvements over the standard Lego firmware, such as smooth acceleration.

It also adds better support for technic motors. Using the default firmware and a PoweredUp remote, holding the +/- buttons causes technic motors to run at full speed, and releasing the button causes the motor to stop. This script makes those motors work like the regular Lego train motor, allowing you to accelerate or decelerate these motors freely and maintaining the speed when you release the button.

I have added a few additional features to the script, specifically support for the official Powered Up lights as well as Hub to Hub communication, which allows you to control multiple locomotives on one train simultaneously.

More information about the original script from Lok24: https://www.eurobricks.com/forum/index.php?/forums/topic/187081-control-your-trains-without-smart-device-with-pybricks/

PyBricks: https://code.pybricks.com/

Special thanks to:

Eurobricks user Lok24 for writing the origional version of this script

Youtuber BatteryPoweredBricks for help testing

## Setup

I highly recommend this setup tutorial video by BatteryPoweredBricks: https://www.youtube.com/watch?v=sgDMOHEmgL0

Installation instructions:
1: Go to https://code.pybricks.com
2: Install Pybricks on your Hub, instructions here: https://pybricks.com/install/technic-boost-city/
3: Import motorcontrol_modified.py into pybricks, and run the code on your hub.
4: Assuming the code ran, it should be saved to your hub. You can disconnect it from your computer and use it as normal.

## Customization

There are a number of customization options for the script:

```
# define the two profiles
# profil_x = (minimum speed,maximum Speed,accelerate in steps of ..., wait for next acceleration(in ms)

Profil_A = (20,100,10,100)  #min,max,step,acc
Profil_B = (10,500,5,200)   #min,max,step,acc
```
Defines the minimum speed, maximum speed, how much the speed increases each time it accelerates, and the wait time before accelerating again (in milliseconds).

The minimum speed is 0 and the maximum speed is 100. Note that Profile_B by default has a maximum speed of 500. The motor's speed will still max out at 100.

You can swap between modes by pressing the red button on the remote.

```
# define direction of motors

dirMotorA = 1       # Direction 1 or -1
dirMotorB = -1       # Direction 1 or -1
```

Sets the direction of each motor, for ports A and B. For a locomotive with two standard train motors, they will often be facing opposite directions, hence why you might need to set them to go in opposite directions.

```
autoacc = False      # accelerate continuously when holding button
```

If False, you must press and release the Up/Down buttons on the remote for each acceleration step. If True, you can hold the button down to continuously accelerate/decelerate.

```
lightValue = 0      # the initial light value, any number between 0 and 100
```

If you have the Powered Up LIghts on your train, this value will be initial light value, with 0 being off. You can further control the brightness of the lights with the B buttons on the remote.

```
shouldBroadcast = False    # whether the hub should broadcast data for a second hub to observe

broadcastChannel = 1    # channel number to broadcast on (0 to 255). Needs to match the value the second hub is observing.
```

These settings are only used for Hub-to-Hub communication, which allows you to control multiple hubs at the same time. This is useful if you have multiple locomotives on the same train. You will be able to accelerate/decelerate/stop them simultaneously.

Setting shouldBroadcast to True causes this hub to broadcast the motor speed and light brightness. Broadcast channel is the channel, between 0 and 255, on which to broadcast on. It must match the observeChannel setting on the observer_hub.

More information about Hub-to-Hub communication, see the Multi-unit section below.

```
mode=1              # start with function number...
```
This sets which profile is the default. For more information about profiles, see above.

```
watchdog = False    # "True" or "False": Stop motors when loosing remote connection
```

Set this to True if you want the motors to stop when the hub looses connection to the remote.

```
remoteTimeout =10   # hub waits x seconds for remote connect after starting hub
```

Number of seconds the hub waits while trying to connect to the remote at startup.

```
remoteName = ""     # connect this remote only
```

You can make the Hub only connect to a specific remote. You can name the remote using the official Lego Powered Up app.

## Multi-unit control via Hub-to-Hub communication

Video Summary by BatteryPoweredBricks: https://www.youtube.com/watch?v=RLTdA9oc_tw

Maybe you want a train with multiple powered locomotives, all moving in sync. Such as a passenger train with a locomotive at each end (for instance, combining two copies of any of the official Lego passenger trains). Maybe you want multiple locomotives pulling a big freight train, like often happens in real life. Or, you want to add a powered piece of rolling stock to a train to give it some extra pulling power.

The default Lego firmware can do this by having one remote connect to multiple hubs. However, you can't utilize some of QoL features of this script, like reversing motor direction, smooth acceleration, or better support for technic motors.

PyBricks by default does not allow one remote to connect to multiple hubs. However, PyBricks allows hubs to broadcast and receive data over bluetooth. This script uses that broadcasting power to to allow you to control multiple hubs at the same time, allowing for simultaneous control of multiple locomotives on one train, accelerating and decelerating them together.

This is useful if you need a second locomotive (or a powered piece of rolling stock) to allow for longer trains. You can have any number of hubs working simultaneously, allowing for super long and heavy trains.

Many people buy two of the current passenger train sets to run a full consist with a locomotive at each end, and with this script you can utilize the motors in both locomotives.

I highly recommend all powered units use the same motors/wheels/gear ratios in order to ensure they all move at the same speed.

### Setup

One of your hubs will be the main hub, referred to as the broadcaster hub. This hub will connect to the remote and regulate the speed for the rest of the train. The rest will be observers, who listen to the broadcaster.

The broadcaster hub will need `motorcontrol_modified.py` installed on it. Set `shouldBroadcast` to True, and set `broadcastChannel` to any value you want. If you want to have multiple different sets of Multi-unit setups, each train will need it's own channel.

Each observer hub will need the `observer_hub.py` script installed on it. Set the `observerChannel` to the broadcastChannel. Make sure to verify the `dirMotor` values are correct for whichever direction each locomotive will be facing.

### In operation

When the broadcaster hub starts, it will begin broadcasting it's current speed and lightvalue.

When you start an observer hub, the led will turn yellow to indicate it is listening but not receiving any data. Once it starts receiving data, the led will return green.

There is sometimes a slight lag between broadcasting and observing. It is usually unnoticeable, but is most noticeable if one of the hubs is connected to a computer via bluetooth. In testing, this seems to have very little affect on performance while running a train.

# Troubleshooting

Multiple users have observed issues using L-Motors with this script, including me. These seem to be erratic, with the script working sometimes but not always. I've attempted to fix it a couple times but being unable to consistently recreate it has made that very difficult.

The error is that the first time you press a direction on the remote, the script will crash and the hub will start blinking blue. Pressing the green button on the hub will launch the script again, but it will likely keep crashing.

To fix this issue, I recommend rolling back your PyBricks firmware to 3.2.3, which has worked for me. You'll have to use an older version of this script that doesn't include Broadcasting compatibility.

### Step 1: Download PyBricks 3.2.3
Download pybricks-cityhub-v3.2.3.zip from Pybrick's github page here: https://github.com/pybricks/pybricks-micropython/releases/tag/v3.2.3

### Step 2: Re-install PyBricks on your Hub with the old firmware
Re-install Pybricks on your hub. But on the first step under 'Select your hub' (https://youtu.be/sgDMOHEmgL0?t=103) you'll want to upload the ZIP file you downloaded under 'Advanced'. After you do this, Pybricks code will keep asking you if you want to update to the latest firmware. You'll want to ignore that.

### Step 3: Use an older version of the script

You will need this older version of the script: https://github.com/and-ampersand-and/PyBricks-Train-Motor-Control-Script/blob/0b5dc0766753b03aacfd82886135d69e5ef04071/motorcontrol_modified.py
The newer version of the script has Broadcasting functionality that isn't compatible with PyBricks 3.2.3

