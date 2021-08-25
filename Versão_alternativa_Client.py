# coding: utf-8

import socket
import pyaudio
import os
import keyboard

ClientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '127.0.0.1'
port = 16000
CODIGO_VAZIO = '-1'
CONEXAO_ENCERRADA = '0'
SUCESSO = '1'
OK = '2'
INTERROMPIDA = '-1'


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

    stop = ''

    while content:

        stream.write(content)  # "Player" de áudio

        if keyboard.is_pressed('p'):  # Se apertar 'p'
            stop = True
            ClientSocket.send(CONEXAO_ENCERRADA.encode('utf-8'))
            break  # Sai do loop
        elif (len(content) < 4096):
            ClientSocket.send(OK.encode('utf-8'))
            stop = False
            break
        else:
            stop = False
            ClientSocket.send(SUCESSO.encode('utf-8'))
        content = ClientSocket.recv(CHUNK)
    ClientSocket.send(str.encode('Música executada'))

    if stop == True:
        return INTERROMPIDA
    else:
        return SUCESSO
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

        Resultado = Player_Cliente()

        if Resultado == SUCESSO:
            print('A música foi executada com Sucesso!')
        else:
            print('A execução da música foi interrompida com Sucesso!')

    elif Response == CONEXAO_ENCERRADA:
        print('Conexão encerrada')
        ClientSocket.close()
        break
    else:
        print('Comando Inválido')