"""
  OTAUpdateManager.py
  
  OTAUpdateManager, a library for the ESP8266/Arduino platform
  for managing Over-The-Air updates for IoT devices
  
  @author Creator Raghul Raj G
  @version 1.0-gr2.1
  @license GNU v3.0
""" 
import time
import machine
import network
import uasyncio
import json
import ubinascii
import urequests
import urandom
import os
try:
    import usocket as socket
except:
    import socket
import ustruct as struct
from ubinascii import hexlify

class espFOTAException(Exception):
    pass

class espFOTA:

    def __init__(self, _User, _Token, _ssid, _password):
        self._user = _User
        self._token = _Token
        self.ssid = _ssid
        self.password = _password
        self.sub_topic = b"readytoupdate/" + _User + b"/" + _Token + b"/mpy"
        self.pub_topic = b"state/" + _User + b"/mpy"
        _Server = "http://firmware.serveo.net/mpydownload"
        self.host = _Server + "?user=" + _User.decode("utf-8") + "&token=" + _Token.decode("utf-8") + "&deviceid=" + ubinascii.hexlify(machine.unique_id()).decode("utf-8")
        self.client_id = ubinascii.hexlify(machine.unique_id())
        self.sock = None
        self.server = "serveo.net"
        self.port = 2512
        self.pid = 0
        self.user = "raghulrajg"
        self.pswd = "Gr2_nemam"
        self.lw_qos = 0
        self.status_LED= machine.Pin(2, machine.Pin.OUT)
        self.status_LED.value(1)
        self.Netconnect()

    def Netconnect(self):
        self.wifi = network.WLAN(network.STA_IF)
        self.wifi.active(True)
        if(not(self.wifi.isconnected())):
            self.wifi.disconnect()
            self.wifi.connect(self.ssid, self.password)
        while(not(self.wifi.isconnected())):
            print("Wifi not connected\nReconnecting")
            try:
                self.wifi.connect(self.ssid, self.password)
            except OSError as e:
                print(e)
            time.sleep(1)
            if self.wifi.isconnected():
                print('WiFi Connected')
                break

        self.status_LED.value(0)
        self.connection()

    def _send_str(self, s):
        self.sock.write(struct.pack("!H", len(s)))
        self.sock.write(s)

    def _recv_len(self):
        n = 0
        sh = 0
        while 1:
            b = self.sock.read(1)[0]
            n |= (b & 0x7f) << sh
            if not b & 0x80:
                return n
            sh += 7

    def connect(self, clean_session=True):
        self.sock = socket.socket()
        addr = socket.getaddrinfo(self.server, self.port)[0][-1]
        self.sock.connect(addr)
        premsg = bytearray(b"\x10\0\0\0\0\0")
        sz = 10 + 2 + len(self.client_id)
        if self.user is not None:
            sz += 2 + len(self.user) + 2 + len(self.pswd)
        i = 1
        premsg[i] = sz

        self.sock.write(premsg, i + 2)
        self.sock.write(bytearray(b"\x04MQTT\x04\xc2\x00\x00\x00\x0c")+self.client_id+bytearray(b"\x00\nraghulrajg\x00\tGr2_nemam"))
        resp = self.sock.read(4)
        assert resp[0] == 0x20 and resp[1] == 0x02
        if resp[3] != 0:
            raise espFOTAException(resp[3])
        return resp[2] & 1

    def publish(self, topic, msg, retain=False, qos=0):
        pkt = bytearray(b"\x30\0\0\0")
        pkt[0] |= qos << 1 | retain
        sz = 2 + len(topic) + len(msg)
        if qos > 0:
            sz += 2
        assert sz < 2097152
        i = 1
        while sz > 0x7f:
            pkt[i] = (sz & 0x7f) | 0x80
            sz >>= 7
            i += 1
        pkt[i] = sz
        #print(hex(len(pkt)), hexlify(pkt, ":"))
        self.sock.write(pkt, i + 1)
        self._send_str(topic)
        if qos > 0:
            self.pid += 1
            pid = self.pid
            struct.pack_into("!H", pkt, 0, pid)
            self.sock.write(pkt, 2)
        self.sock.write(msg)
        if qos == 1:
            while 1:
                op = self.wait_msg()
                if op == 0x40:
                    sz = self.sock.read(1)
                    assert sz == b"\x02"
                    rcv_pid = self.sock.read(2)
                    rcv_pid = rcv_pid[0] << 8 | rcv_pid[1]
                    if pid == rcv_pid:
                        return
        elif qos == 2:
            assert 0

    def subscribe(self, topic, qos=0):
        assert self.cb is not None, "Subscribe callback is not set"
        pkt = bytearray(b"\x82\0\0\0")
        self.pid += 1
        struct.pack_into("!BH", pkt, 1, 2 + 2 + len(topic) + 1, self.pid)
        #print(hex(len(pkt)), hexlify(pkt, ":"))
        self.sock.write(pkt)
        self._send_str(topic)
        self.sock.write(qos.to_bytes(1, "little"))
        while 1:
            op = self.wait_msg()
            if op == 0x90:
                resp = self.sock.read(4)
                #print(resp)
                assert resp[1] == pkt[2] and resp[2] == pkt[3]
                if resp[3] == 0x80:
                    raise espFOTAException(resp[3])
                return

    def wait_msg(self):
        res = self.sock.read(1)
        self.sock.setblocking(True)
        if res is None:
            return None
        if res == b"":
            raise OSError(-1)
        if res == b"\xd0":  # PINGRESP
            sz = self.sock.read(1)[0]
            assert sz == 0
            return None
        op = res[0]
        if op & 0xf0 != 0x30:
            return op
        sz = self._recv_len()
        topic_len = self.sock.read(2)
        topic_len = (topic_len[0] << 8) | topic_len[1]
        topic = self.sock.read(topic_len)
        sz -= topic_len + 2
        if op & 6:
            pid = self.sock.read(2)
            pid = pid[0] << 8 | pid[1]
            sz -= 2
        msg = self.sock.read(sz)
        self.cb(topic, msg)
        if op & 6 == 2:
            pkt = bytearray(b"\x40\x02\0\0")
            struct.pack_into("!H", pkt, 2, pid)
            self.sock.write(pkt)
        elif op & 6 == 4:
            assert 0

    def check_msg(self):
        self.sock.setblocking(False)
        return self.wait_msg()

    def callback(self, topic, msg):
        out = json.loads(msg)
        _Status = out["status"]
        if _Status == 1:
            response = urequests.get(self.host, stream=True)
            total_size = int(response.headers.get('Content-Length', 0))
            downloaded_size = 0
            chunk_size = 1024
            try:
                with open("main.py", 'w') as f:
                    while True:
                        chunk = response.raw.read(chunk_size)
                        if not chunk:
                            break
                        f.write(chunk)
                        downloaded_size += len(chunk)
                        # Calculate and print the progress percentage
                        progress = (downloaded_size / total_size) * 100
                        self.alive(tot = total_size, cur = downloaded_size)
                        print(f"Download progress: {progress:.2f}%")
                    
            finally:
                response.close()
            #restart ESP
            machine.reset()

    def connection(self):
        try:
            self.cb = self.callback
            self.connect()
            print("Server connected")
            self.subscribe(self.sub_topic)
        except OSError as e:
            self.reconnect()

    def reconnect(self):
        print("Can't connect")
        time.sleep(5)
        machine.reset()

    def alive(self, tot = 0, cur = 0):
        return json.dumps({"deviceID":self.client_id, "tot":tot, "cur":cur, "user":self._user, "token":self._token})

    def run(self):
        try:
            self.check_msg()
            self.publish(self.pub_topic, self.alive())
        except OSError as e:
            self.reconnect()

    

