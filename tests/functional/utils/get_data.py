import json


async def from_file(path_file):
    with open(path_file, "r") as file:
        return json.load(file)
