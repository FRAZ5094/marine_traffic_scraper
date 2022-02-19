import json


def read_dundee_port_data():
    with open("dundee_port_data.json", "r") as f:
        return json.load(f)

def read_viable_boats_file():
    with open("viable_boats.txt", "r") as f:
        lines = f.readlines()

    for i in range(len(lines)):
        if "\n" in lines[i]:
            lines[i]=lines[i][:-1]

    return lines

def get_boat_names(data):
    boat_names=[]

    for point in data:
        for boat in point["boats"]:
            boat_name=boat["boat_name"]
            if boat_name not in boat_names:
                boat_names.append(boat["boat_name"])

    return boat_names

def get_average_time_in_port(data, target_boat):
    #print(target_boat)
    in_port=False

    total_time=0
    count=0
    for point in data:
        boats_this_timestamp=[]
        for boat in point["boats"]:
            boats_this_timestamp.append(boat["boat_name"])
        if target_boat in boats_this_timestamp:
            if not in_port:
                #print("boat just got in port")
                in_port=True
                count+=1
                start=int(point["timestamp"])
                #print(point["timestamp"])
        elif in_port:
            #print("boat just left port")
            in_port=False
            total_time+=int(point["timestamp"])-start
            #print(point["timestamp"])
    
    if in_port:
        total_time+=int(data[-1]["timestamp"])-start

    average_time_in_port=round((total_time/count)/(3.6*10**6),2)
    return [average_time_in_port,count]



if __name__ == '__main__':
    print("loading data...")
    data=read_dundee_port_data()
    print("loaded boat data")
    boat_names=get_boat_names(data)

    average_time_in_port={}

    for boat_name in boat_names:

        average_time_in_port[boat_name]=get_average_time_in_port(data,boat_name)

    print("Average times in port:\n")

    average_time_in_port=dict(sorted(average_time_in_port.items(), key=lambda item: item[1][0], reverse=True))

    viable_boats=read_viable_boats_file()
    #print(viable_boats)

    total=0
    for boat_name in average_time_in_port:
        if boat_name in viable_boats:
            print(boat_name, ":", average_time_in_port[boat_name][0], "Hours", "Count:", average_time_in_port[boat_name][1])
            total+=average_time_in_port[boat_name][0]

    print("Average time in port of all boats")

    n=len(viable_boats)

    print(total/n)

