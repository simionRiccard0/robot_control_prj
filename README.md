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
	b. Implement in the "place" phase the corresponding wanted position
2. TCP Connection :
	a. Test the new connection, correct the protocol python-side

3. Tangram:
	a. Integration of a transformation operation between pygame plane and camera/robot plane
	b. "Export" should retrieve positioning data first, then send transformed data
4. Robot :
	a. Implement either in the pre-program or before the loop a wait loop for tangram coordinates.
	b. Implement a refusal protocol as to when a new tangram is pushed directly during one placing with old coordinates.
	c. Implement a matching system between recognized CLOP elements and wanted elements, preferably by the robot.


## Contributors

- Mael Madec
- Riccardo Simion
