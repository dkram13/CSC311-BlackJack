from socket import *
serverName = '127.0.0.1'
serverPort = 16666
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))
print('\n Connect to:', '127.0.0.1, 16666')
while True:
	sentence = input('Would you like to play a game of black jack:')
	clientSocket.send(sentence.encode())
	modifiedSentence = clientSocket.recv(1024).decode()
	print(modifiedSentence)
	if modifiedSentence == ("correct"):
		break
clientSocket.close()

## Server sends cards and asks to Hit or Stay
## if the dealer is dealt 21 games over right away
## server starts and get the cards ready to send
## client receives cards and sends back an answer