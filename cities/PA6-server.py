import os
import django
from django.utils import timezone
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "citysearch_project.settings")
django.setup()
from cities.models import City
import socketserver, json
import logging
import time

class IoTRequestHandler(socketserver.StreamRequestHandler):
    def handle(self):
        client = self.request.getpeername()
        logging.info("Client connecting: {}".format(client))

        for line in self.rfile:

            try:
                request = json.loads(line.decode('utf-8'))
            except ValueError as e:

                error_msg = '{}: json decoding error'.format(e)
                status = 'ERROR {}'.format(error_msg)
                response = dict(status=status, deviceid=request.get('deviceid'),
                                msgid=request.get('msgid'))
                response = json.dumps(response)
                self.wfile.write(response.encode('utf-8') + b'\n')
                self.wfile.flush()
                logging.error(error_msg)
                break
            else:
                status = 'OK'
                logging.debug("{}:{}".format(client, request))


            data = request.get('data')
            if data:
                distance = float(data.get('distance'))

                City(distance=distance, pub_date=timezone.now()).save()


        logging.info('Client closing: {}'.format(client))


logging.basicConfig(filename='', level=logging.DEBUG,
                    format='%(asctime)s:%(levelname)s:%(message)s')

serv_addr = ("192.168.0.63",50011)
with socketserver.ThreadingTCPServer(serv_addr, IoTRequestHandler) as server:
    logging.info('Server starts: {}'.format(serv_addr))
    server.serve_forever()