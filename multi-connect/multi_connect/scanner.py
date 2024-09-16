
import asyncio
from bleak import BleakScanner
import subprocess 
import time

# Define the name of the device you're looking for
TARGET_DEVICE_NAME = "FallSensor"



def handle_device_found(device, advertisement_data):
    if device.name == TARGET_DEVICE_NAME:
        print(f"Target device '{TARGET_DEVICE_NAME}' found!")
        print("Running Script")
        subprocess.Popen(["python", "logger.py"])
        time.sleep(10)
        

async def scan_for_devices():
   
    scanner = BleakScanner()
 
    scanner.register_detection_callback(handle_device_found)
    
    print("Starting scan...")

    await scanner.start()

    try:
        while True:
            await asyncio.sleep(5)
    except KeyboardInterrupt:
        print("Stopping scan...")
    finally:
        await scanner.stop()

if __name__ == "__main__":
    asyncio.run(scan_for_devices())
