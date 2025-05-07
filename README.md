# robot_control_prj

Pick&Place project for the Robot Control course, UV Ljubljana.

## Comm. between PC and Robot

The communication is done by TCP, with Python as language.

Credit : Sebastjan Šlajpah, sebastjan.slajpah@fe.uni-lj.si
Repository : https://github.com/sslajpah/ur_tcpip

Tips :
- As both the host PC and the robot are DHCP, the hardcoded ip address has to be changed at every session.
- The Python code acts as server, robot always as client.
- The robot never indicates directly when the connection is severed.

## Tasks remaining

1. Pick&Place :
	a. Clean the PICK_total variables not in use
2. TCP Connection :
	a. Put in place an ACK system
	b. Launch the data stream when a first ACK is received
	c. ACK after every pieces

3. Tangram:

4. Robot :



## Contributors

- Mael Madec
- Riccardo Simion
