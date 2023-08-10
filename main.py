from machine import Pin, UART
import struct
from time import sleep

MOVR = 0x65766F6D
MOVE = 0x65766F6D

loxonePort = UART(1, baudrate=9600, tx=Pin(4), rx=Pin(5), invert=UART.INV_RX | UART.INV_TX) 
loxonePort.init(bits=8, parity=None, stop=1)

emeloPort = UART(0, baudrate=115200, tx=Pin(0), rx=Pin(1)) 
emeloPort.init(bits=8, parity=None, stop=2)

def CRC16(pbuf, n):
    crc = 0xffff
    for i in range(n):
        crc = crc ^ pbuf[i]
        for j in range(8):
            a = crc
            carry_flag = a & 0x0001
            crc = crc >> 1
            if carry_flag == 1:
                crc = crc ^ 0xa001
    return crc

'''
s = '0x6D 0x6F 0x76 0x72 0x00 0x00 0x00 0xC8 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x53 0xc7'
data = [int(n, 16) for n in s.split()]
emeloPort.write(bytearray(data))
'''

'''
#DeltaPosition = 0xC8000000
DeltaPosition = 0
uDPos = 0
data = struct.pack('<ihBBBBBB', DeltaPosition, uDPos, 0, 0, 0, 0, 0, 0)
print(data)
crc = CRC16(data, len(data))
print('crc: ' + str(crc))
print(struct.pack('<IihBBBBBBH', MOVR, DeltaPosition, uDPos, 0, 0, 0, 0, 0, 0, crc))
payload = struct.pack('<IihBBBBBBH', MOVR, DeltaPosition, uDPos, 0, 0, 0, 0, 0, 0, crc)
emeloPort.write(payload)
'''

'''
Position = 100
uPosition = 0
data = struct.pack('<ihBBBBBB', Position, uPosition, 0, 0, 0, 0, 0, 0)
print('data: ' + str(data))
crc = CRC16(data, len(data))
print('crc: ' + str(crc))
payload = struct.pack('<IihBBBBBBH', MOVE, Position, uPosition, 0, 0, 0, 0, 0, 0, crc)
print('payload: ' + str(payload))
emeloPort.write(payload)
'''

#emeloPort.write('rigt')

def sendMoveCommand(buf):
    Position = int(buf.decode('utf-8'))
    uPosition = 0
    data = struct.pack('<ihBBBBBB', Position, uPosition, 0, 0, 0, 0, 0, 0)
    print('data: ' + str(data))
    crc = CRC16(data, len(data))
    print('crc: ' + str(crc))
    payload = struct.pack('<IihBBBBBBH', MOVE, Position, uPosition, 0, 0, 0, 0, 0, 0, crc)
    print('payload: ' + str(payload))
    emeloPort.write(payload)

while True:
    if loxonePort.any(): 
        buf = loxonePort.read()
        print('from loxone: ' + str(buf))
        #emeloPort.write(buf)
        try:
            sendMoveCommand(buf)
        except:
            emeloPort.write(buf)
        
    if emeloPort.any():
        buf = emeloPort.read()
        print('from emelo: ' + str(buf))
        loxonePort.write(buf)
