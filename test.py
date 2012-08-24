import arduino

arduino = arduino.Arduino("/dev/ttyACM0")

print arduino.getState(10)
