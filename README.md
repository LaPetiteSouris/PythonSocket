# PythonSocket
Python Socket Assignment for Distributed System at Tampere University of Technology, Finland.
The original project was required to be written in C with strictly pre-defined protocol. However, presented here is another Python
version of the project, insprired by similar requirements but without apply strictly defined transmission protocol.

for details, refer to http://www.cs.tut.fi/~hajap/assignments/socket/.



#How to run project:
Execute command "python server.py"  to start server. Later, run "python client.py" to simulate a client request

Default login is:

Debug: 123 <br />
Deb: 123 <br />

#Requirements:
UNIX environment.
Python 2.7

#Design concept:
1.Client will initialize a TCP connection to the server and provide a username  U<br />

2.Server  :
-Queries user database and gets password P1 of username U (if user is unknown the connection is terminated) <br />
-Creates a random number R, which is sent to the client <br />

3.Client:
-Asks an password P2 from the user <br />
-Concatenates the password and the random number (P2+R) and calculates from this data an SHA256-hash value H1. <br />
-Value H1 is sent to the server <br />

4.Server: 
-Calculates SHA256-hash( P1+R ) value H2. <br />
-Compares values H1 ja H2. <br />
-If values are the same, then password is correct and connection is accepted. ELSE the connection is terminated <br />

5.Server and Client start sending 'ping' . Transmission is carried out using UDP Protocol with HMAC verification using common
key namely H1 and H2 as above.



