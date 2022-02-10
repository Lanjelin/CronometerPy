# -*- coding: utf-8 -*-
import json
from crono_json import makeJson

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
names = {
    "pl": "Całe Mleko 3,5 % Ttłuszcze 1 litr",
    "fr": "TINE Lait Entier 3,5 % Gras 1 litre",
}  # Is anyone even using these?
category = 7  # Dairy and Egg Products
tags = ["Brand", "Dairy"]
notes = "Allergens: Milk"  # Any note you want really
barcodes = ["07038010000065", "07038011000064", "07038012000063"]
measures = [
    {"amount": 1, "name": "Glass, small", "id": 1, "type": "Weight", "value": 100},
    {"amount": 1, "name": "Glass, large", "id": 2, "type": "Weight", "value": 300},
]
defaultmeasure = 2  # Glass, large - id from measures variable
label = "EU"  # Don't think Cronometer applies this
owner = 0  # Put your own owner value here if you want, you can find it if exporting one of your existing foods
id = 8675309  # Think Cronometer ignores this
source = (
    "CronoPy"  # This is only visible before saving, afterwards it's changed to Custom
)

js = makeJson(
    name,
    nutrients,
    names=names,
    category=category,
    tags=tags,
    notes=notes,
    barcodes=barcodes,
    measures=measures,
    defaultmeasure=defaultmeasure,
    label=label,
    owner=owner,
    id=id,
    source=source,
)
with open(f"example.json", "w") as outfile:
    json.dump(js, outfile)
