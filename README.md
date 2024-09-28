# RPI Gatway Scripts


## RPI Zero w2 
### Increase Clock Frequency to 1.2 GHz
1. Open /boot/firmware/config.txt
2. Add the following lines to the file
   #Overclock
   arm_freq=1200
   core_freq=525
   over_voltage=2
3. Save the file and reboot the RPi
4. If the Pi does not boot after the change
   a. Turn the pi off
   b. Take out SD card and connect SD to laptop
   c. Find the config.txt file
   d. Lower the arm_freq by 100, until the pi boots

### Add additional swap memory
Edit /etc/dphys-swapfile to change CONF_SWAPSIZE=100 to CONF_SWAPSIZE=2048. After making the change, restart the Pi.
