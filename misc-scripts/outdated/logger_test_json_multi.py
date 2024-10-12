import asyncio
import struct
import sys
import time
import json
from typing import Dict, List
from datetime import datetime
from bleak import BleakClient, BleakScanner, BleakError
from concurrent.futures import ThreadPoolExecutor

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


USER_LOC = "Ayaan's Room"

TARGET_TAG_NAMES =['FallSensor', 'FallSensor1', 'FallSensor2']

class NanoIMUBLEClient:
    def __init__(self, service_uuid: str, characteristic_uuids: List[str], jsonout: bool = True) -> None:
        self._clients = []
        self._devices = []  # Initialize as an empty list
        self._connected = False
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
        self.json_files = {}  # Dictionary to store file handlers and data for each device
        self.json_data = {
                    "Location" : USER_LOC,
                    "Timestamp": [],
                    "Ax": [],
                    "Ay": [],
                    "Az": [],
                    "Gx": [],
                    "Gy": [],
                    "Gz": []
                
}
        if self._jsonout:
            self.create_new_json_files()
        self.executor = ThreadPoolExecutor(max_workers=1)

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
    def devices(self):
        return self._devices
    def _sync_discover_devices(self):
        # This is a synchronous method to discover devices
        return asyncio.run(BleakScanner.discover()) 

    async def discover_devices(self):
        loop = asyncio.get_running_loop()
        devices = await loop.run_in_executor(self.executor, self._sync_discover_devices)
        for d in devices:
            local_name = d.name or 'Unknown'
            print(f"Discovered Device: {local_name}, Address: {d.address}, RSSI: {d.rssi}")
            if local_name in TARGET_TAG_NAMES:
                self._devices.append(d)
                print(f'Found Peripheral Device {d.address}. Local Name: {local_name}')

        if not self._devices:
            print("No target devices found. Retrying in 5 seconds...")
            await asyncio.sleep(5)

    async def start(self) -> None:
        if self._connected:
            try:
                for client in self._clients:
                    for uuid in self._characteristic_uuids:
                        await client.start_notify(uuid, self.newdata_hndlr)
                self._running = True
            except Exception as e:
                print(f"Starting notification failed: {e}")

    async def stop(self) -> None:
        if self._running:
            try:
                for client in self._clients:
                    for uuid in self._characteristic_uuids:
                        await client.stop_notify(uuid)
            except Exception as e:
                print(f"Stopping notification failed: {e}")


    async def connect(self) -> None:
        while not self._connected:
            await self.discover_devices()
            if not self._devices:
                continue

            # Connect to all found devices
            for device in self._devices:
                try:
                    print(f"Attempting to connect to {device.address}")
                    client = BleakClient(device.address)
                    await asyncio.get_event_loop().run_in_executor(self.executor, client.connect)
                    self._clients.append(client)
                    print(f'Connected to {device.address}.')
                    # Create a new JSON file for this device
                    if device.address not in self.json_files:
                        self.create_new_json_file(device.address)
                    # Discover characteristics to verify
                    await self.discover_characteristics(client)
                except (BleakError, asyncio.TimeoutError, Exception) as e:
                    print(f"Connection failed: {e}. Retrying in 5 seconds...")
                    continue

            # Main loop for handling connected clients
            while any(client.is_connected for client in self._clients):
                for client in self._clients:
                    if client.is_connected:
                        if self._running and self.newdata:
                            self.save_data()
                            if time.time() - self.last_print_time >= 1:  # Print every second
                                self.print_newdata()
                                self.last_print_time = time.time()
                            self.newdata = False
                        if not client.is_connected:
                            print(f"Device {client.address} disconnected. Reconnecting...")
                            await self.disconnect(client)
                    await asyncio.sleep(0.01)

    async def disconnect(self, client=None) -> None:
        if client:
            try:
                await asyncio.get_event_loop().run_in_executor(self.executor, client.disconnect)
                self.json_files.pop(client.address, None)  # Remove the file handler for this device
            except Exception as e:
                print(f"Disconnection failed: {e}")
        else:
            for client in self._clients:
                try:
                    await asyncio.get_event_loop().run_in_executor(self.executor, client.disconnect)
                    self.json_files.pop(client.address, None)  # Remove the file handler for this device
                except Exception as e:
                    print(f"Disconnection failed: {e}")
            self._clients = []
        self._connected = False
        self._running = False

    def newdata_hndlr(self, sender, data):
        try:
            uuid = str(sender.uuid)  # Ensure UUID is in string format
            client_address = None
            for client in self._clients:
                if sender in client.characteristics:
                    client_address = client.address
                    break
            if not client_address:
                return

            if client_address in self.json_files:
                device_data = self.json_data.setdefault(client_address, {
                    "Timestamp": [],
                    "Ax": [],
                    "Ay": [],
                    "Az": [],
                    "Gx": [],
                    "Gy": [],
                    "Gz": []
                
                })
                print(f"Writing data to {client_address}")
                if uuid in IMU_UUIDS:
                    if uuid == IMU_UUIDS[0]:
                        device_data['Ax'].append(struct.unpack('<f', bytes(data[0:4]))[-1])
                    elif uuid == IMU_UUIDS[1]:
                        device_data['Ay'].append(struct.unpack('<f', bytes(data[0:4]))[-1])
                    elif uuid == IMU_UUIDs[2]:
                        device_data['Az'].append(struct.unpack('<f', bytes(data[0:4]))[-1])
                    elif uuid == IMU_UUIDs[3]:
                        device_data['Gx'].append(struct.unpack('<f', bytes(data[0:4]))[-1])
                    elif uuid == IMU_UUIDs[4]:
                        device_data['Gy'].append(struct.unpack('<f', bytes(data[0:4]))[-1])
                    elif uuid == IMU_UUIDs[5]:
                        device_data['Gz'].append(struct.unpack('<f', bytes(data[0:4]))[-1])
                    elif uuid == IMU_UUIDs[6]:
                        device_data['Timestamp'].append(datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"))

                self.newdata = True
        except Exception as e:
            print(f"Error handling new data: {e}")
            self._connected = False
  

    def create_new_json_files(self):
        for device in self._devices:
            self.create_new_json_file(device.address)

    def create_new_json_file(self, address):
        if address in self.json_files:
            self.json_files[address].close()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"imu_data_{address}_{timestamp}.json"
        file = open(filename, 'w')
        # Initialize JSON file with an empty list
        json.dump(self.json_data, file)
        file.flush()
        self.json_files[address] = file
        print(f"Created new JSON file: {filename}")


    def save_data(self) -> None:
        if self._jsonout:
            for address, file in self.json_files.items():
                device_data = self.json_data.get(address, {})
                # Update JSON file with new data
                file.seek(0)
                json.dump(device_data, file, indent=4)  # Use indent for readability
                file.flush()
            if time.time() - self.start_time > 60:
                self.create_new_json_files()
                self.start_time = time.time()
                print("Data saved to JSON files.")

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


    async def discover_characteristics(self, client):
        if client.is_connected:
            services = await client.get_services()
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
