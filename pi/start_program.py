import time  # time.sleep
from datetime import datetime
import signal
import subprocess
import os
import tarfile
import shutil

def make_tarfile(output_filename, source_dir):
    if source_dir in os.listdir():
        with tarfile.open(output_filename, "w:gz") as tar:
            tar.add(source_dir, arcname=os.path.basename(source_dir))
            clear_folder(source_dir)
            print("saved logs backup archive")
    else:
        print("folder '" + source_dir + "' doesn't exist. No log files archived")

def kill_prog(p):
    if p != None:
        os.killpg(os.getpgid(p.pid), signal.SIGTERM)
        make_tarfile("logs_backup.tar.gz","logs")
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



program_name = "Robot_log"
print("Program: " + program_name)
#print("Enter filename: ")

#program_name = input()

print()
print("Write 'start' or 'stop' to run / kill the program")
print("Or 'abort' to kill program and exit")


p = None

while True:
    cmd = input()
    if cmd == "start":
        p = subprocess.Popen(program_name,shell=True,preexec_fn=os.setsid)
    elif cmd == "stop":
        kill_prog(p)
        p = None
    elif cmd == "abort":
        kill_prog(p)
        break
