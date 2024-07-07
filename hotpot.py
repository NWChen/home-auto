import asyncio
import os
import sys
import time
from datetime import datetime
from kasa import Credentials, DeviceType, Discover


def log(line):
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"{timestamp} {line}")


async def discover(credentials: Credentials):
    print("Discovering plugs...")
    devices = await Discover.discover()
    return devices


async def turn_on(plug: DeviceType.Plug):
    log(f"Turning on plug: {plug.alias}")
    await plug.turn_on()
    await plug.update()


async def turn_off(plug: DeviceType.Plug):
    log(f"Turning off plug: {plug.alias}")
    await plug.turn_off()
    await plug.update()


async def main():
    TIMEOUT_SECONDS = 60
    KASA_USERNAME = os.environ.get("KASA_USERNAME")
    KASA_PASSWORD = os.environ.get("KASA_PASSWORD")
    credentials = Credentials(KASA_USERNAME, KASA_PASSWORD)
    devices = await discover(credentials)

    device_list = []
    for host, device in devices.items():
        device_list.append(device)
        print(f"({len(device_list)}) {device.alias} <{host}>")

    id_1 = int(input("Enter first plug to toggle: ").strip())
    id_2 = int(input("Enter second plug to toggle: ").strip())
    plug_1 = device_list[id_1 - 1]
    plug_2 = device_list[id_2 - 1]
    print(f"Selected plugs <{plug_1.alias}>, <{plug_2.alias}>. CTRL-C to stop.")

    try:
        while True:
            await turn_on(plug_1)
            await turn_off(plug_2)
            time.sleep(TIMEOUT_SECONDS)

            await turn_off(plug_1)
            await turn_on(plug_2)
            time.sleep(TIMEOUT_SECONDS)
    except KeyboardInterrupt:
        print("Stopping.")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
