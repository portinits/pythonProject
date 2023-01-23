import socket
import time

def write_to_file(output):
    f = open("roundtrip_time.txt", "a")
    f.write(output)
    f.close()

# HOST = "192.168.0.100"
# HOST = "10.20.20.184/24"
HOST = "10.20.20.167"
PORT = 30000

print("Starting Program")
count = 0
pos_reached = b'Position Reached: '
round = 0

while count < 1000:

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen(5)
    print("listen")
    c, adr = s.accept()


    try:
        msg = c.recv(1024)

        print(msg)
        time.sleep(1)
        if msg == b'asking_for_data':
            count = count + 1
            print("The count is", count)
            time.sleep(0.5)

            string = "(10,0,0,0,0,0)"
            #string = input("(x,y,z,Rx,Ry,Rz): ")
            byt = string.encode()

            ms_old = time.time_ns()
            c.send(byt)

        while (msg != b'data_received'):
            msg = c.recv(1024)

        ms_new = time.time_ns()
        print('Roundtrip time:' + str((float(ms_new - ms_old))/1000000) + 'ms' )
        write_to_file(str(ms_new + ' ' + (ms_new - ms_old)) + '\n')


        while(msg != b'Moving finished'):
            print("robot moving... ")
            msg = c.recv(1024)
            time.sleep(0.1)
            print(msg)
            round = round + 1
            if(round >20):
                raise Exception("Moving failed!")

    except socket.error as socketerror:
        print(count)

print("HI")
c.close()
s.close()

print("Programm finished")
