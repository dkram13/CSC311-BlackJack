from socket import *

def main():
    serverName = '127.0.0.1'
    serverPort = 16666
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serverName, serverPort))
    print('\n Connect to:', '127.0.0.1, 16666')
    while True:
        intro = input('Would you like to play a game of black jack:')   # asks user if they want to play
        clientSocket.send(intro.encode()) # sends users answer
        if intro.lower() == "no": # gets us out of game if users says no
            print("Exiting the game.") 
            break
        reply = clientSocket.recv(1024).decode() # receives the reply could be one of three
        print(reply)
        
        message = clientSocket.recv(1024).decode()
        if not message:
            break
        print(message)
        break
    clientSocket.close()

if __name__ == '__main__':
    main()