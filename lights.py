import asyncio
import os
from kasa import Discover
from plugs import discover, turn_off, turn_on
from weather import is_sunny


async def update(plugs) -> None:
    """Update step."""
    lat, lon = 40.7128, -74.0060
    action = turn_off if is_sunny(lat, lon) else turn_on

    for plug in plugs:
        await action(plug)


async def setup(hosts_filename) -> None:
    """Setup plugs."""
    print('Discovering plugs...')
    devices = await discover()

    device_list = []
    for idx, (host, device) in enumerate(devices.items()):
        device_list.append(device)
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

    with open(hosts_filename, "w", encoding="utf-8") as f:
        for host, _ in selected_devices:
            f.write(f"{host}\n")

    print(f"Setup complete! Selected {len(selected_devices)} devices.")


async def main(hosts_filename, kasa_username, kasa_password):
    """Main handler."""
    plugs = []

    with open(hosts_filename, "r", encoding="utf-8") as f:
        if len(f.read().strip()):
            for host in f.readlines():
                host = host.strip()
                plug = await Discover.discover_single(
                    host, username=kasa_username, password=kasa_password
                )
                plugs.append(plug)
        else:
            await setup(hosts_filename)

    await update(plugs)


if __name__ == "__main__":
    HOSTS_FILENAME = "plugs.txt"
    KASA_USERNAME = os.environ.get("KASA_USERNAME")
    KASA_PASSWORD = os.environ.get("KASA_PASSWORD")
    asyncio.run(main(HOSTS_FILENAME, KASA_USERNAME, KASA_PASSWORD))
