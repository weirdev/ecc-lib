# Serial terminal for sending file and text data to Xilinx board 
# (or any other device) over serial connection

import time
import serial
import io

class SerialConnection:
    def __init__(self, port):
        # configure the serial connections (the parameters differs on the device you are connecting to)
        self.ser = serial.Serial(
            port=port,
            baudrate=115200,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=5,
            writeTimeout=5
        )
        if self.ser.isOpen():
            try:
                self.ser.close()
            except:
                print("Could not close already open serial connection")
        self.ser.open()

    def write(self, b):
        '''
        # test how many bytes before board responds
        byteswritten = 0
        while self.ser.inWaiting() <= 0:
            print(self.ser.write(int(5).to_bytes(1, byteorder='little')))
            byteswritten += 1
            print(byteswritten)
            time.sleep(0.01)
        '''
        partkb = len(b) % 1024
        self.ser.write(b)
        self.ser.write(bytearray(1024-partkb))
        '''
        # try flushing between each byte written
        for byte in b:
            self.ser.write(byte.to_bytes(1, byteorder='little')) # Byteorder obviously irrelevent here
            self.ser.flush()
        '''
    def read(self):
        out = b''
        while self.ser.inWaiting() > 0:
            out += self.ser.read(1)
        return out
        
    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.ser.close()

def entercommandloop(scon):
    while True:
        print("[0]\tText input")
        print("[1]\tFile input")
        print("[2]\tCheck for new device response")
        inp = input(">> ")
        inp = inp.strip()
        if inp.lower() == "exit":
            break
        try:
            inp = int(inp)
        except:
            continue
        if inp == 0:
            tosend = input("Enter the text to transmit: ")
            # transmit stuff
            scon.write(tosend.encode())
        elif inp == 1:
            path = input("Enter the file path of the file to transmit: ")
            with open(path, 'rb') as binf:
                bindat = binf.read()
            print(len(bindat))
            scon.write(bindat)
        elif inp == 2:
            pass
        else:
            continue
        time.sleep(1)
        print("Response from device")
        print(scon.read().decode())
        print()

if __name__ == "__main__":
    port = input("Enter serial port: ")
    with SerialConnection(port) as scon:
        # Read initial output
        print(scon.read().decode())
        entercommandloop(scon)
    
