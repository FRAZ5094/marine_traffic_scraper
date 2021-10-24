import json
from datetime import datetime

import matplotlib.pyplot as plt
import pandas as pd


def read_dundee_port_data():
    with open("dundee_port_data.json", "r") as f:
        return json.load(f)


if __name__ == "__main__":
    data = read_dundee_port_data()

    boats = {}
    time = []
    for point in data:
        time.append(int(int(point["timestamp"]) / 1000))
        for boat in point["boats"]:
            if boat["boat_name"] not in boats.keys():
                boats[boat["boat_name"]] = {"in_port": []}

    for point in data:
        for key in boats.keys():
            boat_names = []
            for boat in point["boats"]:
                boat_names.append(boat["boat_name"])

            if key in boat_names:
                # true if in port
                boats[key]["in_port"].append(True)
            else:
                # false if not in port
                boats[key]["in_port"].append(False)

    # print("Boat names:")
    # for key in boats.keys():
    # print(key)

    date_end = datetime.fromtimestamp(time[0])
    date_end = datetime.fromtimestamp(time[-1])

    # print(boats["SEVEN PEGASUS"])

    for boat in boats.keys():
        boats[boat]["in_port_times"] = [[]]
        boats[boat]["out_port_times"] = [[]]
        in_port_count = 0
        out_port_count = 0
        prev_in_port = boats[boat]["in_port"][0]
        for i in range(1, len(boats[boat]["in_port"])):
            if boats[boat]["in_port"][i] != prev_in_port:
                if boats[boat]["in_port"][i]:
                    boats[boat]["in_port_times"].append([])
                    prev_in_port = not prev_in_port
                else:
                    boats[boat]["out_port_times"].append([])
                    prev_in_port = not prev_in_port

            if boats[boat]["in_port"][i]:
                boats[boat]["in_port_times"][in_port_count].append(time[i])
            else:
                boats[boat]["out_port_times"][out_port_count].append(time[i])

    # for l in boats["SEVEN PEGASUS"]["in_port_times"]:
    # print(l)

    print(len(boats["SEVEN PEGASUS"]["in_port_times"]))
    print(len(boats["SEVEN PEGASUS"]["out_port_times"]))
