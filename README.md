# Pi_utils

### **start_program.py**  -  *python3*

Script starts program when switch pin (internal pullup) is high.
When the pin is pulled low, the program will stop, the logfiles will be saved to a tar.gz archive.
Finally the logs folder will be cleared.

The status led will be on while the program is running and turns off as soon as the logs has been archived.


### **uploadCppToPI.sh**

Script uploads changed *.cpp* file to the given ip address.
