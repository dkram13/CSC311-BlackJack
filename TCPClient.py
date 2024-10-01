from socket import *

def main():
	serverName = '127.0.0.1'
	serverPort = 16666
	clientSocket = socket(AF_INET, SOCK_STREAM)
	clientSocket.connect((serverName, serverPort))
	print('\n Connect to:', '127.0.0.1, 16666')

	while True:
		intro = input('Would you like to play a game of black jack: ')  # asks user if they want to play
		clientSocket.send(intro.encode())  # sends user's answer
		if intro.lower() == "no":  # gets us out of game if user says no
			print("Exiting the game.")
			break
		
		start_reply = clientSocket.recv(1024).decode()  # receives confirmation of game
		print(start_reply)
		heWon = clientSocket.recv(1024).decode()
		if "Dealer got Blackjack" in heWon:
			print(heWon)
			break
		else:
			print(heWon)
		iWannaPlay = True

		while iWannaPlay:
			deal_message = clientSocket.recv(1024).decode()  # receives the card draw message from server
			if 'You drew an Ace.' in deal_message:
				ace_val = input(deal_message)
				clientSocket.send(ace_val.encode())
			hitOrStay = input(deal_message)  # asks user to hit or stay
			clientSocket.send(hitOrStay.encode())  # sends user's answer to the server
			
			if hitOrStay.lower() == "stay":
				print (clientSocket.recv(1024).decode())
				iWannaPlay = False  # breaks the loop if the user chooses to stay

		play_again = input("Would you like to play another game? (yes/no): ")  # Ask if they want to play again
		if play_again.lower() != "yes":
			print("Exiting the game.")
			break	
	clientSocket.close()

if __name__ == '__main__':
	main()
## Server sends cards and asks to Hit or Stay
## if the dealer is dealt 21 games over right away
## server starts and get the cards ready to send
## client receives cards and sends back an answer