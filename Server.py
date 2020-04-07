import socket
from socket import AF_INET, SOCK_DGRAM

host = ''
port = 5555
bufsize = 1024
sockaddr = (host, port)
all_data = b''
count = 0
name = 'name'
size = 0
addr = ('192.168.30.16', 5555)
uServerSock = socket.socket(AF_INET, SOCK_DGRAM)
uServerSock.bind(sockaddr)
uServerSock.settimeout(50)

def check_count_packages(count):
    print(count)
    if (count-2) * 1024 >= int(size):
        return True
    else:
        return False

def clear_file(name):
    with open(name, "wb") as f:
        pass
    f.close()

def make_file(name, data):
    with open(name, "ab") as f:
        f.write(data)
    f.close()

def get_packages():
    count = 1
    global all_data
    all_data = b''
    clear_file(name)
    while True:
        if count % 500 == 0:
            make_file(name, all_data)
            all_data = b''
        try:
            data, addr = uServerSock.recvfrom(bufsize)
        except socket.timeout:
            print('Timeout error')
            return count
        count += 1
        print('received from:', addr, 'data: package_' + str(count))
        try:
            if data.decode() == 'STOP':
                return count
        except Exception:
            all_data += data
            continue
        all_data += data

def test_name_size():
    global name, size, addr, count
    try:
        uServerSock.sendto(str(name + size).encode(), addr)
    except Exception:
        uServerSock.sendto('False'.encode(), addr)
    try:
        data, addr = uServerSock.recvfrom(bufsize)
        if data.decode() == 'Repeat':
            test_name_size()
        if data.decode() != 'True':
            print('Error name or size')
            download_file()
        else:
            count = get_packages()
    except socket.timeout:
        print('Timeout error test name and size')

def download_file():
    global name, size, addr
    print('wait...')
    try:
        data, addr = uServerSock.recvfrom(bufsize) # name
        name = data.decode()
        print('download start...')
        print('name -', name)
        uServerSock.settimeout(5)
        data, addr = uServerSock.recvfrom(bufsize) # size
        size = data.decode()
        print('size -', size, 'byte')
    except Exception:
        print('Package not received (name or size)')
    test_name_size()

def test_count_packages():
    # check packages
    global count
    if check_count_packages(count) == True:
        print('file received...')
        uServerSock.sendto(str('True').encode(), addr)
        make_file(name, all_data)
    else:
        print('lost package')
        uServerSock.sendto(str('False').encode(), addr)
        count = get_packages()
        test_count_packages()

#start program
download_file()
test_count_packages()
uServerSock.close()
