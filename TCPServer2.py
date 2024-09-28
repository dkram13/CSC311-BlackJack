from socket import *
import random

card_suits = ["Hearts", 'Diamonds', 'Spades', 'Clubs']
card_values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
deck = [(val, suit) for val in card_values for suit in card_suits]

def values(val):
	if val[0] in ['Jack', 'Queen', 'King']:
		return int(10)
	elif val[0] == 'Ace':
		return int(11)
	else:
		return int(val[0]) 


def main():
    print("Starting server...")
    serverPort = 16666
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.bind(('', serverPort))
    serverSocket.listen(5)
    print('The server is ready to receive')
    while True:
        connectionSocket,addr = serverSocket.accept()
        sentence = connectionSocket.recv(1024).decode()
        if 'yes' == sentence:
            message = 'Okay lets play a game.'
            connectionSocket.send(message.encode())
            connectionSocket.close()
        else:
            message = 'To bad I would have won.'
            connectionSocket.send(message.encode())
              
if __name__ == '__main__':
    main()

