import json

import matplotlib.pyplot as plt
import pandas as pd


def read_dundee_port_data():
    with open("dundee_port_data.json", "r") as f:
        return json.load(f)


if __name__ == "__main__":
    data = read_dundee_port_data()

    # 0 is going from in port to out of port
    # 1 is going from out of port to in port
    boats = {}
    time = []
    for point in data:
        time.append(int(int(point["timestamp"]) / 1000))
        for boat in point["boats"]:
            if boat["boat_name"] not in boats.keys():
                boats[boat["boat_name"]] = []

    for point in data:
        for key in boats.keys():
            boat_names = []
            for boat in point["boats"]:
                boat_names.append(boat["boat_name"])

            if key in boat_names:
                boats[key].append(True)
            else:
                boats[key].append(False)

    print("Boat names:")
    for key in boats.keys():
        print(key)
