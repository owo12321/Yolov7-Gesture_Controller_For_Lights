from socket import *
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(18,GPIO.OUT)

IP = '192.168.0.107'
PORT = 50001
BUFLEN = 1024

listenSocket = socket(AF_INET, SOCK_STREAM)
listenSocket.bind((IP, PORT))

listenSocket.listen(5)
print('Starting success, ',end='')



while True:
    print(f'waiting at port{PORT}')
    dataSocket, addr = listenSocket.accept()
    print(f'Received a client connection from {addr}')

    while True:
        print('\nWaiting to receive')

        recved = dataSocket.recv(BUFLEN)
        if not recved or recved==b'exit':
            print('The peer party is disconnected')
            break
        if recved==b'on':
            GPIO.output(18, GPIO.HIGH)
        elif recved==b'off':
            GPIO.output(18, GPIO.LOW)
        
        dataSocket.send(f'turn {recved.decode()} done'.encode('utf-8'))


dataSocket.close()
listenSocket.close()