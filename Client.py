import socket
from socket import AF_INET, SOCK_DGRAM
import os

#host = '127.0.0.1' # localhost
port = 5555
bufsize = 1024
sockaddr = (host, port)
uClientSock = socket.socket(AF_INET, SOCK_DGRAM)
uClientSock.settimeout(10)

#file for send
file = input('write file address\n')

name = os.path.basename(file)
size = str(os.path.getsize(file))
print('name -', name)
print('size of file -', size, 'byte')

def send_packages():
    print('send file...')
    with open(file, "rb") as f:
        buf = f.read(bufsize)
        while (buf):
            uClientSock.sendto(buf, sockaddr)
            buf = f.read(bufsize)
    uClientSock.sendto('STOP'.encode(), sockaddr)

def count_packages():
    count = 0
    with open(file, "rb") as f:
        buf = f.read(bufsize)
        while (buf):
            count += 1
            buf = f.read(bufsize)
        return count

def send_file():
    global switch
    print('send name and size...')
    uClientSock.sendto(name.encode(), sockaddr)
    uClientSock.sendto(size.encode(), sockaddr)
    test_name_size()
    send_packages()

# test name and size
def test_name_size():
    print('control name and size...')
    try:
        data, addr = uClientSock.recvfrom(bufsize) # count of packages
        if data.decode() != str(name + size):
            print('lost package name or size')
            uClientSock.sendto('False'.encode(), sockaddr)
            send_file()
        else:
            uClientSock.sendto('True'.encode(), sockaddr)
            print('Name and size sent')
    except socket.timeout:
        print('Timeout error name or size')
        uClientSock.sendto('Repeat'.encode(), sockaddr)
        test_name_size()

def test_packages():
    try:
        data, addr = uClientSock.recvfrom(bufsize)
        if data.decode() != 'True':
            print('lost package')
            send_packages()
            test_packages()
        else:
            print('File sent!')
    except socket.timeout:
        print('Timeout error test packages')
        uClientSock.sendto('Repeat'.encode(), sockaddr)
        test_packages()

#start program
send_file()
test_packages()
uClientSock.close()
