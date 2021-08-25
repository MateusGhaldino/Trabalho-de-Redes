# coding: utf-8

import socket
import pyaudio
import os


ClientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '127.0.0.1'
port = 16000
CODIGO_VAZIO = '-1'
CONEXAO_ENCERRADA = '0'
SUCESSO = '1'


print('Conectando ao servidor')
try:
    ClientSocket.connect((host, port))
except socket.error as e:
    print(str(e))

def Player_Cliente():
    p = pyaudio.PyAudio()

    FORMAT = 8
    CHANNELS = 2
    RATE = 44100
    CHUNK = 4096 


    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    output=True)

    content = ClientSocket.recv(CHUNK)

    while content:
        stream.write(content)  # "Player" de áudio
        content = ClientSocket.recv(CHUNK)
        if(len(content) < 4096):
            break
    ClientSocket.send(str.encode('Música executada'))
    stream.close()
    p.terminate() 



List = ClientSocket.recv(1024)
Flag_for_exit = ClientSocket.recv(1024)
List = List.decode('utf-8')
Flag_for_exit = Flag_for_exit.decode('utf-8')
Flag_for_exit = int(Flag_for_exit)



while True:


    #Validando a entrada de dados do cliente
    while True:
        print(List)
        Input = input('Digite o número da música a ser tocada: ')

        #Verificando se foi um valor inteiro digitado         
        if Input.isdigit() == True:
            Int = int(Input)

            #Verificando se esse valor é valido
            if (Int < 0) or (Int > Flag_for_exit):
                #print('Valor Inválido! Por favor tente novamente')
                #Limpando a Tela do console
                os.system('cls') or ('clear')
                print('Comando Inválido! Por favor, tente novamente.')
            else:
                break
        else:
            print('Comando Inválido')

    ClientSocket.send(str.encode(Input))
    Response = ClientSocket.recv(1024)
    Response = Response.decode('utf-8')

    if Response == SUCESSO:
        print('Executando')        
        #Response_1 = ClientSocket.recv(1024)
        Player_Cliente()
    elif Response == CONEXAO_ENCERRADA:
        print('Conexão encerrada')
        ClientSocket.close()
        break
    else:
        print('Comando Inválido')