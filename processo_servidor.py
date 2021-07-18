# coding: utf-8

#Importandos os modúlos de sockets e wave para a execução das tracks

import socket
import wave

serverPort = 16000
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(0)


#Método para tocar as músicas via Servidor
def Player_Servidor(File):

    wf = wave.open(File, 'rb')
    CHUNK = 4096     # Número de frames de áudio
    data = wf.readframes(CHUNK)
    while data:
        connectionSocket.send(data)
        data = wf.readframes(CHUNK)
    wf.close()



print("Servidor pronto para receber Conexões")

#Definindo o nome das músicas para serem enviadas ao processo usuário;

Music_1 = "Dimitri Vegas & Like Mike vs W&W - Arcade (Extended Mix)"
Music_2 = "Legião Urbana - Tempo Perdido "
Music_3 = "The Golden Army and Ramin Djawadi - Game Of Thrones (KSHMR & The Golden Army Remix)"



while True:
    connectionSocket, addr = serverSocket.accept()
    print("Conexão vinda de {}".format(addr))

    mensagem = connectionSocket.recv(2048)

    comando = mensagem.decode('utf-8')
    if comando == "1":
        
        #Será exibido no Processo Servidor
        print("Tocando",Music_1," para a conexão {}".format(addr))

        #Retornando 1 para o processo indicando que musica está pronta para ser tocada
        connectionSocket.send(comando.encode('utf-8'))
        
        
        filename = 'C:/Users/mateu/OneDrive/Documentos/Musicas/Arcade.wav'
       
        Player_Servidor(filename)

   
        connectionSocket.close()


    elif comando == "2":
        #Será exibido no Processo Servidor
        print("Tocando",Music_2,"para a conexão {}".format(addr))
        
        #Retornando 2 para o processo indicando que musica está pronta para ser tocada
        connectionSocket.send(comando.encode('utf-8'))

        filename = 'C:/Users/mateu/OneDrive/Documentos/Musicas/Tempo_Perdido.wav'
       
        Player_Servidor(filename)


        connectionSocket.close()


    elif comando == "3":
        #Será exibido no Processo Servidor
        print("Tocando",Music_3,"para a conexão {}".format(addr))

        #Retornando 3 para o processo indicando que musica está pronta para ser tocada
        connectionSocket.send(comando.encode('utf-8'))

        filename = 'C:/Users/mateu/OneDrive/Documentos/Musicas/Game_of_Thrones _(KSHMR_&_The_Golden_Army_Remix).wav'

        Player_Servidor(filename)

        connectionSocket.close()

    else:

        #Será exibido no Processo Servidor
        print("A conexão {} solicitou um comando inválido".format(addr))

        #Retornando 0 para o processo cliente indicando que a musica não vai ser tocada;
        connectionSocket.send(comando.encode('utf-8'))
        connectionSocket.close()
        


    connectionSocket.close()

