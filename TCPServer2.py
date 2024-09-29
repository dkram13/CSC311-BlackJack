from socket import *
import random

def makeDeck():
    card_suits = ["Hearts", 'Diamonds', 'Spades', 'Clubs']
    card_values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
    deck = [(val, suit) for val in card_values for suit in card_suits]   
    return deck

def addCards(cards):
    cardSum = sum(values(val) for val in cards)
    return cardSum

def hit(socket, deck, p_card1, p_card2, p_sum, d_card1, d_card2, d_score, d_sum):
    new_card = (deck.pop())
    new_sum = values(socket, new_card) + p_sum
    #return (new_card, new_sum)
    
    message = [
    "----------------------------", "\n",
    "Player shows: ", p_card1, p_card2, new_card,"\n",
    "Player score: ", new_sum, "\n",
    "Dealer shows: ", d_card1, "****", "\n",
    "Dealer score: ", d_score, "\n",
    "----------------------------", "\n"
    ]
    message_str = " ".join(map(str, message))
    socket.send(message_str.encode())
    if new_sum > 21:
        
        print("----------------------------")
        print("Player shows: ", p_card1, p_card2, new_card)
        print("Player score: ", new_sum)
        print("Dealer shows: ", d_card1, d_card2)
        print("Dealer score: ", d_sum)
        print("----------------------------")
        print('Player busted, Dealer wins\n')
        message = [
            "----------------------------", "\n",
            "Player shows: ", p_card1, p_card2, new_card,"\n",
            "Player score: ", new_sum, "\n",
            "Dealer shows: ", d_card1, d_card2, "\n",
            "Dealer score: ", d_sum, "\n",
            "----------------------------", "\n"
            "\nPlayer busted, Dealer wins\n"
        ]
        lose_message = " ".join(map(str, message))
        socket.send(lose_message.encode())
        socket.close()
        exit()
    elif new_sum == 21:
        print('\nBlackjack! Player wins\n')
        message = [
            "----------------------------", "\n",
            "Player shows: ", p_card1, p_card2, new_card,"\n",
            "Player score: ", new_sum, "\n",
            "Dealer shows: ", d_card1, d_card2, "\n",
            "Dealer score: ", d_sum, "\n",
            "----------------------------", "\n"
            "\nBlackjack! Player wins\n"
        ]
        win_message = " ".join(map(str, message))
        socket.send(win_message.encode())
        socket.close()
        exit()
    else:
        print("----------------------------")
        print("Player shows: ", p_card1, p_card2, new_card)
        print("Player score: ", new_sum)
        print("Dealer shows: ", d_card1, d_card2)
        print("Dealer score: ", d_sum)
        print("----------------------------")
        hit_or_stay(socket, deck, p_card1, p_card2, new_sum, d_card1, d_card2, d_score, d_sum)


def stay(socket, deck, p_card1, p_card2, p_sum, d_card1, d_card2, d_score, d_sum):
    while d_sum < 17:
        new_card = (deck.pop())
        new_sum = values(socket, new_card) + d_sum
 
        message = [ "\n\n Dealer hit: \n"
            "----------------------------", "\n",
            "Player shows: ", str(p_card1), str(p_card2),"\n",
            "Player score: ", p_sum, "\n",
            "Dealer shows: ", str(d_card1), str(d_card2), "\n",
            "Dealer score: ", new_sum, "\n",
            "----------------------------", "\n"
        ]
        message_str = " ".join(map(str, message))
        socket.send(message_str.encode())
        if 21 >= new_sum > p_sum:
            print("----------------------------")
            print("Player shows: ", p_card1, p_card2, new_card)
            print("Player score: ", p_sum)
            print("Dealer shows: ", d_card1, d_card2)
            print("Dealer score: ", new_sum)
            print("----------------------------")
            print('\nDealer wins\n')
            socket.close()
            exit()
        elif 21 >= p_sum > new_sum:
            print("----------------------------")
            print("Player shows: ", p_card1, p_card2, new_card)
            print("Player score: ", p_sum)
            print("Dealer shows: ", d_card1, d_card2)
            print("Dealer score: ", new_sum)
            print("----------------------------") 
            print('\nPlayer wins\n')
            socket.close()
            exit()
        elif p_sum == new_sum:
            print("----------------------------")
            print("Player shows: ", p_card1, p_card2, new_card)
            print("Player score: ", p_sum)
            print("Dealer shows: ", d_card1, d_card2)
            print("Dealer score: ", new_sum)
            print("----------------------------")
            print('\nPush\n')
            socket.close()
            exit()
    if d_sum >= 17:
        if 21 >= d_sum > p_sum:
            print("----------------------------")
            print("Player shows: ", p_card1, p_card2)
            print("Player score: ", p_sum)
            print("Dealer shows: ", d_card1, d_card2)
            print("Dealer score: ", d_sum)
            print("----------------------------")
            print('\nDealer wins\n')
            socket.close()
            exit()
        elif 21 >= p_sum > d_sum:
            print("----------------------------")
            print("Player shows: ", p_card1, p_card2)
            print("Player score: ", p_sum)
            print("Dealer shows: ", d_card1, d_card2)
            print("Dealer score: ", d_sum)
            print("----------------------------") 
            print('\nPlayer wins\n')
            socket.close()
            exit()
        elif p_sum == d_sum:
            print("----------------------------")
            print("Player shows: ", p_card1, p_card2)
            print("Player score: ", p_sum)
            print("Dealer shows: ", d_card1, d_card2)
            print("Dealer score: ", d_sum)
            print("----------------------------")
            print('\nPush\n')
            socket.close()
            exit()

def hit_or_stay(socket, deck, p_card1, p_card2, p_sum, d_card1, d_card2, d_score, d_sum):
    flag = 'True'
    socket.send(flag.encode())
    hit_message = socket.recv(1024).decode()
    if hit_message == 'hit':
        print('\nPlayer hit.\n')
        hit(socket, deck, p_card1, p_card2, p_sum, d_card1, d_card2, d_score, d_sum)
    elif hit_message == 'stay':
        flag = 'False'
        print('\nPlayer stood\n')
        stay(socket, deck, p_card1, p_card2, p_sum, d_card1, d_card2, d_score, d_sum)
#def moreCardsPlayer():

#def moreCardsDealer():
      

def values(socket, val):
    if val[0] in ['Jack', 'Queen', 'King']:
        return 10
    elif val[0] == 'Ace':
        while True:  # Loop until valid input
            try:
                ace_choice = socket.recv(1024).decode()
                if ace_choice == '1':
                    return 1
                elif ace_choice == '11':
                    return 11
                else:
                    print("Invalid choice. Please enter 1 or 11.")
            except ValueError:
                print("Please enter a valid number (1 or 11).")
        '''flag = 'Ace'
        socket.send(flag.encode())
        reply = socket.recv(1024).decode()
        if reply == '1':
            return 1
        elif reply == '11':
            return 11
        else:
            return None''' 
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
        connectionSocket, addr = serverSocket.accept()
        sentence = connectionSocket.recv(1024).decode()
        if 'yes' == sentence:
            reply = "Okay lets play a game.\n"
            connectionSocket.send(reply.encode())
            dealersDeck = makeDeck()
            random.shuffle(dealersDeck)
            '''playerCards = []
            dealerCards = []
            playerCards.append(dealersDeck.pop())
            dealerCards.append(dealersDeck.pop())
            playerCards.append(dealersDeck.pop())
            dealerCards.append(dealersDeck.pop())
            playerSum = addCards(playerCards)
            dealerSum = addCards(dealerCards)
            print("----------------------------")
            print("Player shows: ", playerCards)
            print("Player score: ", playerSum)
            dealerCards.pop()
            print("Dealer shows: ", dealerCards)
            print("Dealer score: ", dealerSum)
            print("----------------------------")

            message = [
                "----------------------------", "\n",
                "Player shows: ", str(playerCards),"\n",
                "Player score: ", playerSum, "\n",
                "Dealer shows: ", str(dealerCards), "****", "\n",
                "Dealer score: ", dealerSum, "\n",
                "----------------------------", "\n"
            ]'''
            player_card1 = [dealersDeck.pop()]
            #p_card_val1 = (values(val) for val in player_card1)
            dealer_card1 = [dealersDeck.pop()]
            player_card2 = [dealersDeck.pop()]
            #p_card_val2 = (values(val) for val in player_card2)
            dealer_card2 = [dealersDeck.pop()]

            player_sum = sum(values(connectionSocket, val) for val in player_card1 + player_card2)
            dealer_sum = sum(values(connectionSocket, val) for val in dealer_card1 + dealer_card2)
            dealer_score = sum(values(connectionSocket, val) for val in dealer_card1)
            

            print("----------------------------")
            print("Player shows: ", player_card1, player_card2)
            print("Player score: ", player_sum)
            print("Dealer shows: ", dealer_card1, dealer_card2)
            print("Dealer score: ", dealer_sum)
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

            if player_sum < 21:
                hit_or_stay(connectionSocket, dealersDeck, player_card1, player_card2, player_sum, dealer_card1, dealer_card2, dealer_score, dealer_sum)
            elif player_sum == 21:
                flag = 'False'
                connectionSocket.send(flag.encode())
                print('\nBlackjack! Player wins\n')
                win_message = ('\nBlackjack! Player wins\n')
                connectionSocket.send(win_message.encode())
                connectionSocket.close()
                exit()
        elif 'no' == sentence:
            message = 'Too bad I would have won.'
            connectionSocket.send(message.encode())
        else:
            message = 'Invalid input.'
            connectionSocket.send(message.encode())
              
if __name__ == '__main__':
    main()


