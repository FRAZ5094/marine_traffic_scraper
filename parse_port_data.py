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

    date_start = datetime.fromtimestamp(time[0])
    print(date_start)
    date_end = datetime.fromtimestamp(time[-1])
    print(date_end)

    print(boats.keys())

    # for boat in boats.keys():
    boat = list(boats.keys())[10]
    boats[boat]["in_port_times"] = []
    boats[boat]["out_port_times"] = []
    in_port_count = 0
    out_port_count = 0
    prev_in_port = None  # not true or false
    for i in range(1, len(boats[boat]["in_port"])):
        if boats[boat]["in_port"][i] != prev_in_port:
            if boats[boat]["in_port"][i]:
                boats[boat]["in_port_times"].append([])
                print(f"appending to in_port_times at i= {i}")
                print(time[i])
                prev_in_port = not prev_in_port
            else:
                boats[boat]["out_port_times"].append([])
                print(f"appending to out_port_times at i= {i}")
                print(time[i])
                prev_in_port = not prev_in_port

        if boats[boat]["in_port"][i]:
            boats[boat]["in_port_times"][-1].append(time[i])
        else:
            boats[boat]["out_port_times"][-1].append(time[i])

    # for l in boats[boat]["in_port_times"]:
    # print(l)

    print(len(boats[boat]["in_port_times"]))
    print(len(boats[boat]["out_port_times"]))

    print("----")
    print(boat)

    # calculate in/out of port delta_t's

    for section in boats[boat]["in_port_times"]:
        delta_t = (section[-1] - section[0]) / 60
        if delta_t <= 10:
            print(section)
        print(delta_t)

    plt.plot(time, boats[boat]["in_port"])
    plt.show()
