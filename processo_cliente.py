# coding: utf-8
import socket

import pyaudio

Music_1 = "Dimitri Vegas & Like Mike vs W&W - Arcade (Extended Mix)"
Music_2 = "Legião Urbana - Tempo Perdido "
Music_3 = "The Golden Army and Ramin Djawadi - Game Of Thrones (KSHMR & The Golden Army Remix)"

serverName = '127.0.0.1'
serverPort = 16000
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect((serverName, serverPort))

print("\nBem vindo ao Servidor de Músicas! \nMúsicas Disponíveis no momento \n1 - Dimitri Vegas & Like Mike vs W&W - Arcade (Extended Mix) \n2- Legião Urbana - Tempo Perdido \n3- The Golden Army and Ramin Djawadi - Game Of Thrones (KSHMR & The Golden Army Remix)")
message = input("Qual música você deseja ouvir: ")

clientSocket.send(message.encode('utf-8'))

modifiedMessage = clientSocket.recv(1024)
teste = modifiedMessage.decode("utf-8")


def Print_Name_Music(Comando):

    if(Comando == "1"):
        print("Tocando:",Music_1)

    elif(Comando == "2"):

        print("Tocando:",Music_2)

    elif (Comando == "3"):
        print("Tocando:",Music_3)

    else:
        print("Código Inválido")


def Player_Client(Comando):
    Print_Name_Music(Comando)
    p = pyaudio.PyAudio()

    FORMAT = 8
    CHANNELS = 2
    RATE = 44100
    CHUNK = 4096 


    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    output=True)

    content = clientSocket.recv(CHUNK)

    while content:
        stream.write(content)  # "Player" de áudio
        content = clientSocket.recv(CHUNK)
    stream.close()
    p.terminate() 
    return 1




if (teste == "1") or (teste == "2") or (teste == "3"):

    #implementar a reprodução de músicas


    Music = Player_Client(teste)

    if Music == 1:
        print("Audio executado com sucesso!")
    else:
        print("Erro ao tocar a Música")
    clientSocket.close() 
else:
    print("Não foi possível tocar a música, comando Inválido")
    
clientSocket.close()