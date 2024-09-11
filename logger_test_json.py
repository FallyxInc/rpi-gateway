import asyncio
import struct
import sys
import time
import json
from typing import Dict, List
from datetime import datetime
from bleak import BleakClient, BleakScanner, BleakError

# Example UUIDs for multiple characteristics
IMU_UUIDS = [
    '12345678-1234-5678-1234-56789abcdef1',
    '12345678-1234-5678-1234-56789abcdef2',
    '12345678-1234-5678-1234-56789abcdef3',
    '12345678-1234-5678-1234-56789abcdef4',
    '12345678-1234-5678-1234-56789abcdef5',
    '12345678-1234-5678-1234-56789abcdef6',
    '12345678-1234-5678-1234-56789abcdef7'
    
]


USER_LOC = "Dining Room"

TARGET_TAG_NAME = 'FallSensor'

class NanoIMUBLEClient:
    def __init__(self, service_uuid: str, characteristic_uuids: List[str], jsonout: bool = True) -> None:
        self._client = None
        self._device = None
        self._connected = False
        self._running = False
        self._service_uuid = service_uuid
        self._characteristic_uuids = characteristic_uuids
        self._found = False
        self._data = {
            "time": 0,
            "ax": 0.0, "ay": 0.0, "az": 0.0,
            "gx": 0.0, "gy": 0.0, "gz": 0.0
        }
        self._jsonout = jsonout
        self.newdata = False
        self.start_time = time.time()
        self.file = None
        self.writer = None
        self.sample_count = 0
        self.last_sample_time = time.time()
        self.samples_per_second = []
        self.last_print_time = time.time()
        self.json_file = None
        self.json_data = {
            "Location": USER_LOC,
            "Timestamp": [],
            "Ax": [],
            "Ay": [],
            "Az": [],
            "Gx": [],
            "Gy": [],
            "Gz": []
            
        }
        if self._jsonout:
            self.create_new_json()

    @property
    def connected(self) -> bool:
        return self._connected

    @property
    def data(self) -> Dict:
        return self._data

    @property
    def service_uuid(self) -> str:
        return self._service_uuid

    @property
    def running(self) -> bool:
        return self._running

    @property
    def device(self):
        return self._device

    async def discover_devices(self):
        print('Seeed XIAO BLE Service')
        print('Looking for Peripheral Device...')

        devices = await BleakScanner.discover()
        for d in devices:
            local_name = d.name or 'Unknown'
            print(f"Discovered Device: {local_name}, Address: {d.address}, RSSI: {d.rssi}")
            if local_name == TARGET_TAG_NAME:
                self._found = True
                self._device = d
                print(f'Found Peripheral Device {self._device.address}. Local Name: {local_name}')
                return

        print("Peripheral device not found. Retrying in 5 seconds...")
        await asyncio.sleep(5)

    async def connect(self) -> None:
        while not self._connected:
            await self.discover_devices()
            if not self._found:
                continue

            try:
                print(f"Attempting to connect to {self._device.address}")
                self._client = BleakClient(self._device.address)
                await self._client.connect()
                print(f'Connected to {self._device.address}.')
                self._connected = True
                # Discover characteristics to verify
                await self.discover_characteristics()

                await self.start()
                while self._connected:
                    if self._running and self.newdata:
                        self.save_data()
                        if time.time() - self.last_print_time >= 1:  # Print every second
                            self.print_newdata()
                            self.last_print_time = time.time()
                        self.newdata = False
                    if not self._client.is_connected:
                        print("Device disconnected. Reconnecting...")
                        self._connected = False
                        await self.disconnect()
                        break
                    await asyncio.sleep(0.01)
            except (BleakError, asyncio.TimeoutError, Exception) as e:
                print(f"Connection failed: {e}. Retrying in 5 seconds...")
                self._connected = False
                self._found = False
                await asyncio.sleep(5)

    async def disconnect(self) -> None:
        if self._connected:
            try:
                await self._client.disconnect()
            except Exception as e:
                print(f"Disconnection failed: {e}")
            finally:
                self._connected = False
                self._running = False

    async def start(self) -> None:
        if self._connected:
            try:
                for uuid in self._characteristic_uuids:
                    await self._client.start_notify(uuid, self.newdata_hndlr)
                self._running = True
            except Exception as e:
                print(f"Starting notification failed: {e}")

    async def stop(self) -> None:
        if self._running:
            try:
                for uuid in self._characteristic_uuids:
                    await self._client.stop_notify(uuid)
            except Exception as e:
                print(f"Stopping notification failed: {e}")


    def newdata_hndlr(self, sender, data):
        try:
            uuid = str(sender.uuid)  # Ensure UUID is in string format
            if uuid == IMU_UUIDS[0]:
                #print(f"Accel X UUID is {uuid}")
                self._data['ax'] = struct.unpack('<f', bytes(data[0:4]))[-1]



            elif uuid == IMU_UUIDS[1]:
                #print(f"Accel Y UUID is {uuid}")
                self._data['ay'] = struct.unpack('<f', bytes(data[0:4]))[-1]



            elif uuid == IMU_UUIDS[2]:
                #print(f"Accel Z UUID is {uuid}")
                self._data['az'] = struct.unpack('<f', bytes(data[0:4]))[-1]

                # Handle data for UUID 12345678-1234-5678-1234-56789abcdef3
                # Implement specific handling logic here

            elif uuid == IMU_UUIDS[3]:
                #print(f"Gyro X UUID is {uuid}")
                self._data['gx'] = struct.unpack('<f', bytes(data[0:4]))[-1]

                # Handle data for UUID 12345678-1234-5678-1234-56789abcdef4
                # Implement specific handling logic here

            elif uuid == IMU_UUIDS[4]:
                #print(f"Gyro Y UUID is {uuid}")
                self._data['gy'] = struct.unpack('<f', bytes(data[0:4]))[-1]

                # Handle data for UUID 12345678-1234-5678-1234-56789abcdef5
                # Implement specific handling logic here

            elif uuid == IMU_UUIDS[5]:
                #print(f"Gyro Z UUID is {uuid}")
                self._data['gz'] = struct.unpack('<f', bytes(data[0:4]))[-1]
                # Handle data for UUID 12345678-1234-5678-1234-56789abcdef6
                # Implement specific handling logic here

            elif uuid == IMU_UUIDS[6]:
                #print(f"Timestamp UUID is {uuid}")
                self._data['time'] = struct.unpack('<L', bytes(data[0:4]))[-1]
                # Handle data for UUID 12345678-1234-5678-1234-56789abcdef7
                # Implement specific handling logic here

            self.newdata = True
        except Exception as e:
            print(f"Error handling new data: {e}")
            self._connected = False

   
    def create_new_json(self):
        if self.json_file:
            self.json_file.close()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"imu_data_{timestamp}.json"
        self.json_file = open(filename, 'w')
        # Initialize JSON file with an empty list
        json.dump([], self.json_file)
        self.json_file.flush()

    def save_data(self) -> None:
         if self._jsonout:
              # Append new data to the appropriate lists
            self.json_data["Timestamp"].append(datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"))
            self.json_data["Ax"].append(self._data['ax'])
            self.json_data["Ay"].append(self._data['ay'])
            self.json_data["Az"].append(self._data['az'])
            self.json_data["Gx"].append(self._data['gx'])
            self.json_data["Gy"].append(self._data['gy'])
            self.json_data["Gz"].append(self._data['gz'])
                        
            # Update JSON file with new data
            self.json_file.seek(0)
            json.dump(self.json_data, self.json_file, indent=4)  # Use indent for readability
            self.json_file.flush()
            if time.time() - self.start_time > 60:
                self.create_new_json()
                self.start_time = time.time()


    def calculate_sample_rate(self):
        current_time = time.time()
        self.sample_count += 1
        elapsed_time = current_time - self.last_sample_time
        if elapsed_time >= 1.0:
            samples_per_second = self.sample_count / elapsed_time
            self.samples_per_second.append(samples_per_second)
            self.samples_per_second = self.samples_per_second[-10:]
            self.sample_count = 0
            self.last_sample_time = current_time
        if self.samples_per_second:
            return round(sum(self.samples_per_second) / len(self.samples_per_second), 2)
        return 0


    def print_newdata(self) -> None:
        _str = (f"\r Time: {self.data['time']/1000000.0:+3.3f} | " +
                "Accl: " +
                f"{self.data['ax']:+1.3f}, " + 
                f"{self.data['ay']:+1.3f}, " + 
                f"{self.data['az']:+1.3f} | " +
                "Gyro: " +
                f"{self.data['gx']:+3.3f}, " +
                f"{self.data['gy']:+3.3f}, " +
                f"{self.data['gz']:+3.3f} | " +
                f"Sample Rate: {self.calculate_sample_rate():+3.2f} Hz")
        sys.stdout.write(_str)
        sys.stdout.flush()



    async def discover_characteristics(self):
        if self._connected:
            services = await self._client.get_services()
            for service in services:
                if service.uuid == self._service_uuid:
                    print(f"Service UUID: {service.uuid}")
                    for characteristic in service.characteristics:
                        print(f"Characteristic UUID: {characteristic.uuid}")

async def run():
    imu_client = NanoIMUBLEClient('12345678-1234-5678-1234-56789abcdef0', IMU_UUIDS, True)
    await imu_client.connect()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(run())
    except KeyboardInterrupt:
        print('\nReceived Keyboard Interrupt')
    finally:
        print('Program finished')
