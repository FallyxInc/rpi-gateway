# RPI Gateway Scripts

## File Structure

### single_connect

Running logger_single.py will conenct to a single fallyx device and log the data
in csv format. There is no minimum required RSSI to connect and performs basic
functionality.

Running send_to_api.py will take the csv files made in the folder root, and send them
to the fallyx api. It will recieve a response from the api and print it to the terminal.

### 1-sensor_1-gateway

Similar functionality as 'single_connect'. Improved features such as file transfer
to independent folder and handling of disconnect logic. The currently open files
will stay at the fodler root, then transfered to send_out when complete.

Running send_to_api.py will take the csv files made in the folder root, and send them
to the fallyx api. It will recieve a response from the api and print it to the terminal.
The script will only look in the send_out folder for data to be transfered.

Send_out folder houses all the .csv data ready to be sent out by the send_to_api.py script.

### multi-sensor_1-gateway

Folder contains 3 scripts that are required to run for full functionality.

logger_single.py
logger_single2.py
send_to_api.pi

The two logger scripts are able to connect to two seperate fallyx devices.
The RSSI of the device at intial connection must be -80 dBm.
The functionality of the scripts above provide:
    1. Connection to two devices with handling to ensure both devices do not connect
        to the same script.
    2. Proper handling of disconnection to esure the device can reconnect again.
    3. Moving the file to the send_out folder to ensure data is not lost on disconencton.
    4. Ensure there is a good connection of -80 RSSI to connect initally.

The send_to_api.py script will send the data to the fallyx api and print the response.
There is functionality to check if the file is empty to ensure empty data does not
get sent to the api.

main_run.sh is a bash script to run all the files in parallel. 


### multi-sensor_1-gateway_ext_ant

Exact same functionality as 'multi-sensor_1-gateway' but with initalizations
for external BLE antenna.

main_run_ant.sh runs the three scripts in parralel but also includes functioanlity
to initalize the external BLE antenna.

### misc-scripts

Folder contains older scripts and to be used for reference only. 

json_visualization.py is able to visualize the data
for debugging perpouses.


## RPI Zero w2 Setup 
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

##test 
