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
                imo = str(boat["boat_imo"])
                boats[boat["boat_name"]] = {"in_port": [], "imo": imo}

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

    date_start = datetime.fromtimestamp(time[0]).strftime("%d-%m-%y")
    print(date_start)
    date_end = datetime.fromtimestamp(time[-1]).strftime("%d-%m-%y")
    print(date_end)

    print(boats.keys())

    for boat in boats.keys():
        boats[boat]["in_port_times"] = []
        boats[boat]["out_port_times"] = []
        in_port_count = 0
        out_port_count = 0
        prev_in_port = None  # not true or false
        for i in range(1, len(boats[boat]["in_port"])):
            if boats[boat]["in_port"][i] != prev_in_port:
                if boats[boat]["in_port"][i]:
                    boats[boat]["in_port_times"].append([])
                    prev_in_port = not prev_in_port
                else:
                    boats[boat]["out_port_times"].append([])
                    prev_in_port = not prev_in_port

            if boats[boat]["in_port"][i]:
                boats[boat]["in_port_times"][-1].append(time[i])
            else:
                boats[boat]["out_port_times"][-1].append(time[i])

    print("----")

    # calculate in/out of port delta_t's

    for boat in boats.keys():
        in_port_delta_ts = []
        out_port_delta_ts = []

        for section in boats[boat]["in_port_times"]:
            delta_t = section[-1] - section[0]
            in_port_delta_ts.append(int(delta_t / 60))  # in seconds

        for section in boats[boat]["out_port_times"]:
            delta_t = section[-1] - section[0]
            out_port_delta_ts.append(int(delta_t / 60))  # in seconds

        average_in_port = int(
            ((sum(in_port_delta_ts)) / (len(in_port_delta_ts)) / 60)
        )  # in minutes
        boats[boat]["average_time_in_port"] = average_in_port
        boats[boat]["number_in_port"] = len(boats[boat]["in_port_times"])
        boats[boat]["number_out_port"] = len(boats[boat]["out_port_times"])

        total_time_in_port = sum(in_port_delta_ts)
        total_time_out_port = sum(out_port_delta_ts)
        total_time = total_time_out_port + total_time_in_port

        percent_in_port = int((total_time_in_port / total_time) * 100)

        boats[boat]["percent_in_port"] = percent_in_port

    boat_names = []
    imos = []
    time_first_in_port = []
    number_of_times_visited_port = []
    number_of_times_out_of_port = []
    average_time_spent_in_port_per_visit = []
    percent_in_port = []
    for boat in boats.keys():
        boat_names.append(boat)
        imos.append(boats[boat]["imo"])
        time_first = datetime.fromtimestamp(
            boats[boat]["in_port_times"][0][0]
        ).strftime("%d-%m-%y %H:%M:%S")

        time_first_in_port.append(time_first)

        number_of_times_visited_port.append(boats[boat]["number_in_port"])
        number_of_times_out_of_port.append(boats[boat]["number_out_port"])
        average_time_spent_in_port_per_visit.append(boats[boat]["average_time_in_port"])
        percent_in_port.append(boats[boat]["percent_in_port"])

    boat_data = pd.DataFrame(
        {
            "boat names": boat_names,
            "imo": imos,
            "time first in port": time_first_in_port,
            "number of times visited port": number_of_times_visited_port,
            "number of times out of port": number_of_times_out_of_port,
            "average time spend in port per visit": average_time_spent_in_port_per_visit,
            "percentage of time in port": percent_in_port,
        }
    )

    # print(boat_data["time first in port"])
    # print(boats["SEVEN PEGASUS"])

    boat_data.to_csv(fr"boat_data_({date_start}_to_{date_end}).csv", index=False)

    for boat in boats.keys():
        plt.plot(time, boats[boat]["in_port"])
        plt.title(f"{boat} imo={boats[boat]['imo']} 1=in port 0=not in port")
        plt.savefig(f"./boats_in_port_figs/{boat}_data.png")
