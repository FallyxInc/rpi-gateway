# Instructions to incorperate external antenna into rpi zero w2

1. Run the command to open the file:
'''
sudo nano /boot/firmware/config.txt
'''
2. When the file is open, add the line: 
'''
dtoverlay=disable-bt
'''
3. Reboot the pi

