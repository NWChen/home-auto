import asyncio
from kasa import DeviceType, Discover


async def discover():
    """Returns a dict of host (str) -> device (dict)."""
    devices = await Discover.discover()
    return devices


async def turn_on(plug: DeviceType.Plug):
    """Turn on a plug."""
    await asyncio.wait([plug.turn_on(), plug.update()])


async def turn_off(plug: DeviceType.Plug):
    """Turn off a plug."""
    await asyncio.wait([plug.turn_off(), plug.update()])
