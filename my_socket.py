import socket
import webbrowser
import os

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print(socket.gethostbyname_ex(socket.gethostname())[-1][-1])
server.bind((socket.gethostbyname_ex(socket.gethostname())[-1][-1], 9998))
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.listen()

while True:
    client, addr = server.accept()
    print(f'Connection {addr[0]}:{addr[1]}')
    while True:
        request = client.recv(1024).decode()
        print(request)
        if not request:
            break
        else:
            response = b'Ok'
            client.send(response)

            if request == '1':
                os.startfile('C:\hack.pptx')
            elif request == '2':
                webbrowser.open('https://web.telegram.org/z/')
            elif request == '3':
                os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
            else:
                print("Иди выспись! Я тебя не понимаю")
