# coding: utf-8

#Conserta o erro da encerramento da conexão com cliente e modularizar o código do cliente 

import socket
import os
from _thread import *
from os import listdir
from os.path import isfile, join
import wave

ServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = ''
port = 16000
ThreadCount = 0
CODIGO_VAZIO = '-1'
CONEXAO_ENCERRADA = '0'
SUCESSO = '1'
ERRO = '-1'


try:
    ServerSocket.bind((host, port))
except socket.error as e:
    print(str(e))

# Diretório de músicas
musicdir = 'C:/Users/mateu/OneDrive/Documentos/Musicas/'

# Lista com o nome das músicas
musiclist = [f for f in listdir(musicdir) if isfile(join(musicdir, f))]

music = ''
for i, nome in enumerate(musiclist):
    music = music+str(i)+' - '+nome.replace('.wav',' ')+'\n' # String com o número e nome das músicas
    saida = i+1 # Código para fechar o programa do cliente

Enviar = str(saida)

print('Servidor pronto para transmitir')
ServerSocket.listen(0)


def Player_server(i,nome,musiclist,codigo,connection,address):
    for i,nome in enumerate(musiclist):

        if codigo == str(i):
            print('Tocando: '+ nome.replace('.wav',' ') + 'para a conexão:'+ str(address))
            wf = wave.open(musicdir+nome, 'rb')
            CHUNK = 128    # Número de frames de áudio
            data = wf.readframes(CHUNK)
            
            while data:
                connection.send(data)
                data = wf.readframes(CHUNK)
                if(len(data)<1):
                    saida = b'saida'
                    connection.send(saida) 
            wf.close()
            return SUCESSO
    return ERRO

def threaded_client(connection,address):

    #Enviando a Playlist e o Flag de Saída para o processo do Cliente
    connection.send(str.encode('Lista de músicas disponíveis: \n\n'+music+str(saida)+' - Para fechar o programa\n'))
    connection.send(str.encode(Enviar))

    while True:
        cod = connection.recv(1024)
        CodDec = cod.decode('utf-8')

        #Realizando cast para poder fazer a comparação dos valores
        cod = int(cod)

        #Verificando se o comando digitado pelo usuário está vazio se caso estiver vazio o operador not retornará false para o if
        if not CodDec :
            connection.send(CODIGO_VAZIO.encode('utf-8'))

        #Verificando se o Flag saída foi digitado pelo cliente
        elif cod == saida:
            connection.close()
            print('A conexão com cliente '+ str (address) + 'foi finalizada')
            break

        #Executando a música para o cliente
        else:
            Resultado = Player_server(i,nome,musiclist,CodDec,connection,address)

            #A Música foi tocada com sucesso
            if Resultado == SUCESSO:
                print('Música reproduzida com sucesso para a conexão:'+ str(address))
            else:
                print('Ocorreu algum erro ao tocar a música para a conexão: ' + str(address))

while True:

    Client, address = ServerSocket.accept()
    print('Conectado a: ' + address[0] + ':' + str(address[1])) 
    start_new_thread(threaded_client, (Client,address))

    ThreadCount += 1
    print('Cliente: ' + str(ThreadCount))

ServerSocket.close()