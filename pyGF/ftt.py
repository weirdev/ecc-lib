# File transfer terminal for sending data to Xilinx board over serial connection

import time
import serial
import io

class SerialConnection:
    def __init__(self):
        # configure the serial connections (the parameters differs on the device you are connecting to)
        self.ser = serial.Serial(
            port='COM4',
            baudrate=115200,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=5
        )
        self.ser.open()

    def write(self, b):
        self.ser.write(b)

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
        if inp.to_lower() == "exit":
            break
        try
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
    scon = SerialConnection()
    # Read initial output
    print(scon.read().decode())
    entercommandloop()
    