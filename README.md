## lights.py

Script to turn on Kasa plugs when it's dark out, turn them off when it's light out. Also turn them off at night. Includes a setup step to detect your plugs.

```sh
$ pip install requests python-kasa
$ python lights.py
```

## hotpot.py

Cycle between Kasa plugs controlling hotpots. This is useful if you want to use e.g. two hotpots on a single residential outlet but are limited by 20A breakers. The script will cycle between hotpots every minute, and heat loss to air should be less than the total heat added to the system.