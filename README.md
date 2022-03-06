# CronometerPy
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Python Library for generating json for importing to [Cronometer](https://cronometer.com/) foods.

Import the makeJsonDict()-function from [crono_json.py](https://github.com/Lanjelin/CronometerPy/blob/main/crono_json.py), and give it at least a name for the food, and a list of dictionaries containing the nutriends. It will return a dictionary you can use directly with json.dump.

```py
import json
from crono_json import makeJsonDict
from cronopy import CronoPy

name = "TINE Helmelk 3,5 % fett 1 liter"
nutrients = [
    {"id": 208, "amount": 63.0},
    {"id": 204, "amount": 3.5},
    {"id": 606, "amount": 2.3},
    {"id": 205, "amount": 4.5},
    {"id": 269, "amount": 4.5},
    {"id": 203, "amount": 3.4},
    {"id": 307, "amount": 40.0},
]
crono_json_dict = makeJsonDict(name, nutrients)
# Save as json
with open(f"fancy_name.json", "w") as outfile:
    json.dump(crono_json_dict, outfile)

# Directly save to cronometer custom foods
cron = CronoPy()
msg, error = cron.Login(username, password)
if error:
    raise SystemExit(msg)
else:
    print(msg)
msg, error = cron.importCustomFood(crono_json_dict)
if error:
   print(f"Error: {msg}")
else:
   print(msg)
msg, error = cron.Logout()
print(msg)
```

For a complete example with all the variables, take a look at [example.py](https://github.com/Lanjelin/CronometerPy/blob/main/example.py), it's output is available in [example.json](https://github.com/Lanjelin/CronometerPy/blob/main/example.json)

The file [example_minimal.json](https://github.com/Lanjelin/CronometerPy/blob/main/example_minimal.json) contains the minimal amount of information required by Cronometer to accept the json-file.

[crono_dict.py](https://github.com/Lanjelin/CronometerPy/blob/main/crono_dict.py) contains all the variables I've been able to pull, and is required by [crono_json.py](https://github.com/Lanjelin/CronometerPy/blob/main/crono_json.py).

Go make something fancy!
