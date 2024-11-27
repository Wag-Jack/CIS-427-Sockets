from socket import *

serverName = 'serverName'
serverPort = 3516

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect(serverName, serverPort)

sentence = input('Input a lowercase sentence')

clientSocket.send(sentence.encode())

modifiedSentence = clientSocket.recv(1024)

print("From Server: ", modifiedSentence.decode())

clientSocket.close()