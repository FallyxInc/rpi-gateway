## New Start Checklist

1. Update and upgrade
```
sudo apt update && sudo apt upgrade
```
2. Change swap config. Change  CONF_SWAPSIZE=100 to CONF_SWAPSIZE=2048.
```
sudo nano /etc/dphys-swapfile
```
3. Disable blueooth
```
sudo nano /boot/firmware/config.txt
```
then add: 
```
dtoverlay=disable-bt
```
4. Add BT firmware:
```
wget https://github.com/winterheart/broadcom-bt-firmware/raw/master/brcm/BCM20702A1-0a5c-21e8.hcd
```
then,
```
sudo cp BCM20702A1-0a5c-21e8.hcd /lib/firmware/brcm/
```
then,
```
sudo hciconfig hci0 down
sudo hciconfig hci0 up
sudo systemctl restart bluetooth
```
5. Shutdown the pi and physically unplug the device
6.  Create the venv
   ```
   python -m venv ~/venv
   ```
7. Source the venv
   ```
   source ~/venv/bin/activate
   ```
8. Install packages
   ```
   pip install bleak requests
   ```

6. When the pi starts up use below to make sure the hci adapter is up

```
sudo hciconfig
```
if DOWN then use:
```
sudo hciconfig hci0 up
```


