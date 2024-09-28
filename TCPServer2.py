from socket import *
import random

card_suits = ["Hearts", 'Diamonds', 'Spades', 'Clubs']
card_values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
deck = [(val, suit) for val in card_values for suit in card_suits]

def values(val):
	if val[0] in ['Jack', 'Queen', 'King']:
		return 10
	elif val[0] == 'Ace':
		return 11
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
            reply = "Okay lets play a game.\n"
            connectionSocket.send(reply.encode())

            random.shuffle(deck)
            player_card1 = [deck.pop()]
            #p_card_val1 = (values(val) for val in player_card1)
            dealer_card1 = [deck.pop()]
            player_card2 = [deck.pop()]
            #p_card_val2 = (values(val) for val in player_card2)
            dealer_card2 = [deck.pop()]

            player_sum = sum(values(val) for val in player_card1 + player_card2)
            dealer_sum = sum(values(val) for val in dealer_card1 + dealer_card2)
            dealer_score = sum(values(val) for val in dealer_card1)
            

            print("----------------------------")
            print("Player shows: ", player_card1, player_card2)
            print("Player score: ", player_sum)
            print("Dealer shows: ", dealer_card1, "****")
            print("Dealer score: ", dealer_score)
            print("----------------------------")

            message = [
                "----------------------------", "\n",
                "Player shows: ", str(player_card1), str(player_card2),"\n",
                "Player score: ", player_sum, "\n",
                "Dealer shows: ", str(dealer_card1), "****", "\n",
                "Dealer score: ", dealer_score, "\n",
                "----------------------------", "\n"
            ]

            message_str = " ".join(map(str, message))

            connectionSocket.send(message_str.encode())
            #connectionSocket.close()  
        
        elif 'no' == sentence:
            message = 'To bad I would have won.'
            connectionSocket.send(message.encode())
        else:
            message = 'Invalid input.'
            connectionSocket.send(message.encode())
            break  
              
if __name__ == '__main__':
    main()

