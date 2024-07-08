import asyncio
import os
from datetime import datetime
from kasa import Discover, exceptions
from plugs import discover, turn_off, turn_on
from weather import is_sunny


async def update(plugs) -> None:
    """Update step."""
    lat, lon = 40.7128, -74.0060
    print('Getting weather...')
    _is_sunny = is_sunny(lat, lon)

    for plug in plugs:
        if _is_sunny:
            print(f"{datetime.now()}: Turning off plugs")
            await turn_off(plug)
        else:
            print(f"{datetime.now()}: Turning on plugs")
            await turn_on(plug)


async def setup(hosts_filename) -> None:
    """Setup plugs."""
    print("Discovering plugs...")
    devices = await discover()

    device_list = []
    for idx, (host, device) in enumerate(devices.items()):
        device_list.append((host, device))
        print(f"({idx}) {device.alias} <{host}>")

    finished_idx = len(device_list)
    print(f"({finished_idx}) Finished")

    selected_id, selected_devices = -1, []
    while selected_id != finished_idx:
        selected_id = int(
            input(f"Select a plug, or {finished_idx} to finish: ").strip()
        )
        if selected_id != finished_idx:
            selected_devices.append(device_list[selected_id])

    lines = []
    with open(hosts_filename, "w", encoding="utf-8") as f:
        for host, _ in selected_devices:
            f.write(f"{host}\n")
            lines.append(host)

    print(f"Setup complete! Selected {len(selected_devices)} devices.")
    return lines


async def connect(host, username, password):
    """Connect to a single plug."""
    return await Discover.discover_single(host, username=username, password=password)


async def main(hosts_filename, kasa_username, kasa_password):
    """Main handler."""
    plugs = []
    with open(hosts_filename, "r", encoding="utf-8") as f:
        lines = f.readlines()
        if len(lines) < 1:
            print(f"Hosts file {hosts_filename} is empty; starting setup.")
            lines = await setup(hosts_filename)

        for host in lines:
            host = host.strip()
            successfully_acted = False
            while not successfully_acted:
                try:
                    plug = await connect(host, kasa_username, kasa_password)
                    successfully_acted = True
                except Exception as e:
                    print(f"Encountered error {e}; trying again, then quitting")

            plugs.append(plug)

    await update(plugs)


if __name__ == "__main__":
    HOSTS_FILENAME = "plugs.txt"
    KASA_USERNAME = os.environ.get("KASA_USERNAME")
    KASA_PASSWORD = os.environ.get("KASA_PASSWORD")
    asyncio.run(main(HOSTS_FILENAME, KASA_USERNAME, KASA_PASSWORD))
