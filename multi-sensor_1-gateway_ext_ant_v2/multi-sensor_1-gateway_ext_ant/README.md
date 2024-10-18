# Instructions to incorperate external antenna into rpi zero w2

1. Plug in the adapter then boot the pi

2. Run the command to open the file:
```
sudo nano /boot/firmware/config.txt
```
3. When the file is open, add the line: 
```
dtoverlay=disable-bt
```
4. Save the file and reboot the pi

5. Open a terminal window and run the command:
```
sudo hciconfig
```
6. Make sure the adapter pops up, and the status should say 'UP'.

If the hci0 is down run the command:
```
sudo hciconfig hci0 up

```
7. Check that the bluetooth service is running with:
```
sudo systemctl status bluetooth
```
If inactive, run the command:
```
sudo systemctl start bluetooth
```
8. Next we need to power on the adapter with the command:
```
bluetoothctl
```
Then in the bluetooth control write:
```
power on
```
Exit the control with:
```
exit
```
9. You can then run the scripts with hopefully no errors

# Possible issues (external antenna with rpi zero w2)

1. Limited usb bandwidth (USB2.0) on the rpi zero w2. This could cause
    bottleneck with external antenna.

2. CPU is much less than rpi4 so this could also affect performance.

3. Power delivery to antenna. RPi 4 has USB3.0 (blue ports) that can
    supply 0.9A of power. The USB2.0 ports (Grey on rpi 4 and every usb on zero)
    can supply 0.5A of power.
    ** Probably Unlikely due to 33mA consuption in constant rx mode **

# Tests to perform

1. Measure power from antenna to verify no power issues.
2. Check if USB 2.0 on RPi 4 has no issues with adapter 


# Possible fixes

1. Handle discovery better in the script. See if we can filter
the devices to give a quciker search.

