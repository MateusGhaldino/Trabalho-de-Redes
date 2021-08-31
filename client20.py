# coding: utf-8

import socket
import pyaudio
import os
import keyboard
import sys

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

List = ClientSocket.recv(1024)
Flag_for_exit = ClientSocket.recv(1024)
List = List.decode('utf-8')
Flag_for_exit = Flag_for_exit.decode('utf-8')
Flag_for_exit = int(Flag_for_exit)


def Player_Cliente():
    p = pyaudio.PyAudio()

    FORMAT = 8
    CHANNELS = 2
    RATE = 44100
    CHUNK = 512 


    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    output=True)
    print("Tocando")
    content = ClientSocket.recv(CHUNK)
    while (content):
        stream.write(content)  # "Player" de áudio
        content = ClientSocket.recv(CHUNK)
        try:
            if((content[(len(content)-5):]).decode()=='saida'):
                break
        except:
            pass
    
    stream.close()
    p.terminate() 






while True:


    #Validando a entrada de dados do cliente
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(List)
        Input = input('Digite o número da música a ser tocada: ')

        #Verificando se foi um valor inteiro digitado         
        if Input.isdigit() == True:
            Int = int(Input)
            if(Int == Flag_for_exit):
                ClientSocket.send(str.encode(Input))
                sys.exit(0)
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
    Player_Cliente()