from socket import *
serverName = '10.250.153.88'#10.250.153.88 - 10.250.155.197
serverPort = 16666
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))
print('\n Connect to:', '192.168.1.33,4000')
while True:
	sentence = input('Input your guess number is:')
	clientSocket.send(sentence.encode())
	modifiedSentence = clientSocket.recv(1024).decode()
	print(modifiedSentence)
	if modifiedSentence == ("correct"):
		break
clientSocket.close()