import requests
import socket
import config

class TransmissionRPC(object):
    sessionID = ''
    login = ''
    password = ''

    def __init__(self, login, password, sessionID=''):
        self.sessionID = sessionID
        self.login = login
        self.password = password
        TransmissionRPC.sessionIDs = sessionID
        TransmissionRPC.login = login
        TransmissionRPC.password = password

    @classmethod
    def auth_rpc(self):
        r = requests.post(config.transmission_host, auth=(TransmissionRPC.login, TransmissionRPC.password))
        TransmissionRPC.sessionID = r.headers['X-Transmission-Session-Id']
        return TransmissionRPC.sessionID

    @staticmethod
    def get_rxtx():
        headers = {
            'X-Transmission-Session-Id': TransmissionRPC.sessionID
        }
        json = '{"method":"session-stats","arguments":{},"tag":""}'
        r = requests.post(config.transmission_host, headers=headers, data=json,
                          auth=(TransmissionRPC.login, TransmissionRPC.password))
        print(r.json()['arguments']['uploadSpeed'])
        tx = 10 * int(r.json()['arguments']['uploadSpeed'])
        rx = 10 * int(r.json()['arguments']['downloadSpeed'])
        vals = {
            'rx': rx,
            'tx': tx
        }
        return vals


def send_data(rx, tx):
    sock = socket.socket()
    try:
        sock.connect((config.narodmon_host, config.narodmon_port))
        sock.send(
            "#{}\n#{}#{}#{}\n#{}#{}#{}\n##".format(config.mac_addr, config.sensor_id_RX, rx, "RX", config.sensor_id_TX,
                                                   tx, "TX").encode())
        data = sock.recv(1024)
        sock.close()
        print(data)
    except socket.error as e:
        print('ERROR! Exception {}'.format(e))


if __name__ == "__main__":
    t = TransmissionRPC(config.rpc_login, config.rpc_pwd)
    TransmissionRPC.auth_rpc()
    speed = TransmissionRPC.get_rxtx()
    send_data(speed['rx'], speed['tx'])
