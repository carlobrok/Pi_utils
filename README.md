# Pi_utils

### start_program.py

**Requirements:** 
* python3 + wiringpi
  * `sudo apt-get update`
  * `sudo apt-get install python3-all-dev`
  * `sudo apt-get install python3-pip`
  * `sudo pip3 install wiringpi telepot`

Script starts program when switch pin (internal pullup) is high.
When the pin is pulled low, the program will stop, the logfiles will be saved to a tar.gz archive.
Finally the logs folder will be cleared.

The status led will be on while the program is running and turns off as soon as the logs has been archived.

**setup:**
* set ***folder_path*, *program_name*, *led_pin* and *sw_pin*** in the start_program.py file
* write to ***rc.local*** :
  * `sudo nano /etc/rc.local`
  * before `exit 0` write `python3 /path/to/your/directory/start_program.py &`

Now the script starts every time the raspberry pi boots.

To temporarily pause the autorun on boot write a **#** in front of the last line of ***rc.local***.

</br>

### upload_build_project.sh

Script uploads changed *.cpp* file to the given ip address and rebuilds the project.

**Run script:**

`$ ./upload_build_project.sh <ip address> <source folder> <parent folder of project on pi> <project name> [-c]`

**Description:**

* **ip address** of the remote raspberry pi (e.g. *192.168.20.95*)
* **source folder** on the computer (e.g. *~/git/PIv10/*)
* the **parent folder** of the project folder (e.g. */home/pi/projects/*)
* use **-c** to clean project, rebuild everything (optional)

