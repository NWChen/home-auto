import asyncio
import os
import time
from datetime import datetime
from kasa import Discover, exceptions
from plugs import discover, turn_off, turn_on
from weather import is_sunny

DRY_RUN = False
DUTY_CYCLE_ON_SECONDS = 10
MAX_RETRIES = 3


# TODO make this better
def log(msg) -> None:
    now = datetime.now()
    print(f"{now} {msg}")


async def cycle(plug) -> None:
    complete = False
    tries = 0

    while not complete and tries < MAX_RETRIES:
        tries += 1
        try:
            log("PUMP ON")
            if not DRY_RUN:
                await turn_on(plug)
            time.sleep(DUTY_CYCLE_ON_SECONDS)
            log("PUMP OFF")
            if not DRY_RUN:
                await turn_off(plug)
            complete = True
        except Exception as e:
            print(f"Encountered failure: {e} trying again (attempt #{tries}/{MAX_RETRIES})")


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


async def connect(host):
    """Connect to a single plug."""
    return await Discover.discover_single(host)


async def main(hosts_filename):
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
                    plug = await connect(host)
                    successfully_acted = True
                except Exception as e:
                    print(f"Encountered error {e}; trying again, then quitting")

            plugs.append(plug)

    await cycle(plugs[0])


if __name__ == "__main__":
    HOSTS_FILENAME = "/Users/nwc/git/home-auto/hydro.txt"
    asyncio.run(main(HOSTS_FILENAME))
