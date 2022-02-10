# -*- coding: utf-8 -*-
from crono_dict import languages


def makeJson(
    name,
    nutrients,
    names={},
    category=0,
    tags=[],
    notes="",
    barcodes=[],
    measures=[],
    defaultmeasure=52542633,
    label="EU",
    owner=0,
    id=8675309,
    source="CronoPy",
):
    js = {}
    js["owner"] = owner
    js["comments"] = notes
    js["labelType"] = label
    js["foodTags"] = tags
    js["source"] = source
    js["barcodes"] = barcodes
    js["nutrients"] = nutrients
    js["measures"] = [
        {
            "amount": 1,
            "name": "oz",
            "id": 52542632,
            "type": "Weight",
            "value": 28.3495231,
        },
        {"amount": 1, "name": "g", "id": 52542633, "type": "Weight", "value": 1},
    ]
    if len(measures) > 0:
        js["measures"].extend(measures)
    js["defaultMeasureId"] = defaultmeasure
    js["translations"] = [
        {"translationId": languages["en"], "name": name, "languageCode": "en"}
    ]
    for lang in names:
        js["translations"].append(
            {
                "translationId": languages[lang],
                "name": names[lang],
                "languageCode": lang,
            }
        )
    js["name"] = name
    js["id"] = id
    js["category"] = category
    js["properties"] = {}  # please contact me if you figure what this does
    return js
