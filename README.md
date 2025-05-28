# robot_control_prj

Pick&Place project for the Robot Control course, UV Ljubljana.

## URScript 

The locating, picking & placing part is done by an UR5e.
The code produced following this project is located in **/RobotControl**,
and the project is **tangram.urp**. The installation setup is most likely **comm.installation**.

## Comm. between PC and Robot

The communication is done by TCP, with Python as language.
Base and examples have been provided by Sebastjan Šlajpah.
However, the main code approaches the communication differently than this first approach.
It is instead a quasi-websocket communication system, with Queue and asynchronous comm.

Credit : Sebastjan Šlajpah, sebastjan.slajpah@fe.uni-lj.si
Repository : https://github.com/sslajpah/ur_tcpip

Tips :
- As both the host PC and the robot are DHCP, the hardcoded ip address has to be changed at every session.
- The Python code acts as server, robot always as client.
- The robot never indicates directly when the connection is severed.

### Linux

How to set up the computer for communicating with the UR Robot.
```bash
hostname -I 
ip addr show
sudo ip addr add 192.168.65.XXX/24 dev __device_name__
```

## How to launch the program

### Before launching

Before launching, check if :
1. The PC has an open port for communication.
2. The IP address in cfg.py is the same as the open port.
3. The IP address in tangram.urp is matching too.

### The program

Once launched, the robot waits endlessly for connecting to the PC.
Meanwhile, the python part is waiting 10s before dropping off and showing the user interface (it is for debug reasons). If it connects before the 10s, it quickly shows the GUI.

The tangram game is made with pygame. As such, playing with the shapes is easy.
5 top buttons are present to make appear pieces inside the main field. A bin is present where pieces can be dragged and dropped to delete them. Pieces can be rotated by holding the left click and pressing either RIGHT ARROW or LEFT ARROW, tilting them by 15°.

### Quitting

Closing the window simply closes the program, if the connection is stopped.
Stopping the program, both on the robot and the pc, is essential before launching the program again.

## Contributors

- Mael Madec
- Riccardo Simion
