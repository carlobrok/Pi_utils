import wiringpi
import time  # time.sleep
from datetime import datetime
import signal
import subprocess
import os
import tarfile
import shutil


# ADJUST THESE VALUES:

folder_path = "/home/pi/projects/KamelPi/Debug/"
program_name = "KamelPi"

led_pin = None
sw_pin = 26             # WiringPi pin 26

# ==== END ===============



program_path = folder_path + program_name

# ============ defs ===================

def timestamp_str():
    return datetime.now().strftime("%Y%m%d_%H%M%S")

def make_tarfile(output_filename, source_dir):
    if os.path.isdir(source_dir):
        with tarfile.open(output_filename, "w:gz") as tar:
            tar.add(source_dir, arcname=os.path.basename(source_dir))
            clear_folder(source_dir)
            print("Saved logs to: " + output_filename)
    else:
        print("folder '" + source_dir + "' doesn't exist. No log files archived")

def kill_prog(p):
    if p != None:
        os.killpg(os.getpgid(p.pid), signal.SIGTERM)
        logs_archive_name = "logs_" + timestamp_str() + ".tar.gz"
        make_tarfile(folder_path + logs_archive_name, folder_path + "logs")
        print("Stopped program")

def clear_folder(folder):
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            #elif os.path.isdir(file_path): shutil.rmtree(file_path)
        except Exception as e:
            print(e)

def prog_sw():
    return wiringpi.digitalRead(26)

# ======= main ===============

def main():

    print("Program: " + program_path)
    print("")
    p = None  # process holding variable

    wiringpi.wiringPiSetup()
    wiringpi.pinMode(26, 0) # Pinmode input
    wiringpi.pullUpDnControl(26, 2) # Internal pullup

    last_prog_sw = None

    running = False

    while True:
        sw_state = prog_sw()
        if sw_state != last_prog_sw:
            time.sleep(0.1)
            sw_state = prog_sw()

            if running == True:
                if sw_state != last_prog_sw and sw_state == 1:
                    print("Starting program...")
                    p = subprocess.Popen(program_path,shell=True,preexec_fn=os.setsid)
                else:
                    print("Stopping program!")
                    kill_prog(p)
                    p = None
            elif running == False and sw_state == 0:
                running = True
        last_prog_sw = sw_state
        time.sleep(0.05)


if __name__== "__main__":
    main()
