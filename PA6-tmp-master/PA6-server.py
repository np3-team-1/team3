from socket import socket,AF_INET, SOCK_STREAM # 소켓 임포트
import sqlite3
import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "citysearch_project.settings")
django.setup()
from cities.models import City


def echo_server(my_port):
    sock = socket(AF_INET, SOCK_STREAM)  # 소켓 객체를 생성
    sock.bind(('192.168.0.63', my_port)) # 소켓객체에 주소값을 바인딩 시킴 호스트와 포트로 된 튜플값을 인자로 받음
    sock.listen(5)   # 리스닝 수 = 5
    print('server started')
    while True:   # 프로세스가 죽을때 까지
        conn, client_addr = sock.accept()  # 서버소켓에 클라이언트가 연결되면 클라이언트 소켓, 주소를 반환
        print('connected by', client_addr)  # 어떤 주소에서 연결되었는지 프린트
        try:
            while True:
                data = conn.recv(1024) #클라이언트로부터 1024바이트 만큼 데이터를 받아옴
                if not data: break  # 소켓이 닫힐때 까지
                print('server received', data.decode())
                r_msg=data.decode()
                s = r_msg.split()
                db = sqlite3.connect('temperature.db')
                cursor = db.cursor()

                # data type load
                if(s[0][5:]=='load'): # 데이터타입이 load 이면
                    datein=(s[1][5:]+" "+s[2])[:19] # 날짜와 초 단위까지나오게
                    tmp = s[3][-5:]
                    cursor.execute("INSERT INTO TMP VALUES(?, ?);",(datein, tmp)) # 데이터 베이스에 값 datein, temperature값 저장
                    db.commit()
                    msg = "server received\n"
                    conn.send(msg.encode())
                City(name=tmp, state=datein).save()
                db.close()

        # Exception Handling
        except OSError as e:
            print('socket error: ', e)
        except Exception as e:
            print('Exception at listening:'.format(e))
        else:
            print('client closed', client_addr)
        finally:
            conn.close()

if __name__ == '__main__':
    echo_server(50011)   # 포트번호


