import serial

def sendText(text):
    ser = serial.Serial('/dev/cu.usbmodem14101', 9600)  # open serial port
    ser.write(text.encode())  # write a string
    ser.close()  # close ports

