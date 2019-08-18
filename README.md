# Pi_utils

### **start_program.py**  -  *python3*

Script starts program when switch pin (internal pullup) is high.
When the pin is pulled low, the program will stop, the logfiles will be saved to a tar.gz archive.
Finally the logs folder will be cleared.

The status led will be on while the program is running and turns off as soon as the logs has been archived.


### **upload_build_project.sh**

Script uploads changed *.cpp* file to the given ip address and rebuilds the project.
The 

**Run script:**

`$ ./upload_build_project.sh <ip address> <source folder> <project's subfolder on pi> <project name>`
