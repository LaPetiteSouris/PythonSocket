import socket
import hashlib

print('Please enter your username')
u1=raw_input()
s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('127.0.0.1', 8080))
s.sendall(u1)
r=s.recv(256)
if r != 'Failed':
	print('Please enter your password:')
	p1=raw_input()
	h1=str(p1)+str(r)
	h1hash=hashlib.sha256(h1).hexdigest()
	s.sendall(h1hash)
	result=s.recv(256)
	if result == 'Done':
		print ('You are authorized to access !')
	elif result == 'Failed':
		print ('Authentication error')
	s.close()
elif r == 'Failed':
	print ('Authentication error')
	s.close()

