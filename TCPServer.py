from socket import *
import random
serverPort = 16666
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(5)
print('The server is ready to receive')
while True:
	connectionSocket,addr = serverSocket.accept()
	rn = random.randint(0, 31)
	print(rn)
	sentence = int(connectionSocket.recv(1024).decode())
	if rn == sentence:
		message = 'correct'
		connectionSocket.send(message.encode())
		connectionSocket.close()
	else:
		message = 'incorrect'
		connectionSocket.send(message.encode())
	