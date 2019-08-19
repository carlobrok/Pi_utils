import wiringpi
import time

wiringpi.wiringPiSetup()
wiringpi.pinMode(26, 0)
wiringpi.pullUpDnControl(26, PUD_UP)

last_prog_sw = None

while True:
    prog_sw = wiringpi.digitalRead(26)
    if prog_sw != last_prog_sw:
        if prog_sw:
            print("Switch is on!")
        else:
            print("Switch is off")
    last_prog_sw = prog_sw
