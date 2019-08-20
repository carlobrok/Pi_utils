import wiringpi2 as wiringpi
import time

wiringpi.wiringPiSetup()
wiringpi.pinMode(26, 0) # Pinmode input
wiringpi.pullUpDnControl(26, 2) # Internal pullup

last_prog_sw = None
last_call = False

def prog_sw():
    return wiringpi.digitalRead(26)

counter = 1

while True:
    sw_state = prog_sw()
    if sw_state != last_prog_sw:
        time.sleep(0.1)
        sw_state = prog_sw()
        if sw_state != last_prog_sw and sw_state == 1:
            print("Switch is on!" + str(counter))
            counter += 1
        else:
            print("Switch is off!" + str(counter))
            counter += 1
    last_prog_sw = sw_state
    time.sleep(0.05)
