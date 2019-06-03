import sys , socket
import serial
import datetime
import sqlite3

port = "/dev/ttyACM0"
ser = serial.Serial(port,9600)
ser.flushInput()

def echo_client(server_addr):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(server_addr)
    print('connected: ', sock.getpeername())
    while True:
        message = sys.stdin.readline()
        if message == '\n':
            temperture=[]  # 온도를 저장하기 위한 리스트
            ser.write("in".encode('utf-8'))
            temperture.append(float(ser.readline()))
            s_msg = "type:load\r\ntime:%s\r\ntemperature%s\r\n" %(datetime.datetime.now(),temperture[0])  #시간과 온도를 서버로 보냄
            sock.send(s_msg.encode('utf-8'))
        data = sock.recv(1024).decode('utf-8')
        print(data,end='')
    sock.close()

if __name__ == '__main__':
    echo_client(('192.168.0.63',50011))