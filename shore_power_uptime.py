import json 
import matplotlib.pyplot as plt
from statistics import median

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

def uptime(data,boats):
    # print(boats)
    number_of_timestamps=0
    number_of_shore_power_timestamps=0
    for i in range(len(data)):
        number_of_timestamps+=1
        found_in_this_timestamp=False
        for name in data[i]["boats"]:
            if name["boat_name"] in boats:
                if not found_in_this_timestamp:
                    number_of_shore_power_timestamps+=1
                    found_in_this_timestamp=True

    return  (number_of_shore_power_timestamps/number_of_timestamps)*100


if __name__ == "__main__":
    data = read_dundee_port_data()
    viable_boats=read_viable_boats_file()

    number_of_timestamps=0
    number_of_shore_power_timestamps=0

    viable_in_port=[]

    boat_occurrences={}

    for i in range(len(data)):
        viable_in_port.append(0)
        number_of_timestamps+=1
        found_in_this_timestamp=False
        for name in data[i]["boats"]:
            if name["boat_name"] in viable_boats:
                if name["boat_name"] in boat_occurrences.keys():
                    viable_in_port[i]+=1
                    boat_occurrences[name["boat_name"]]+=1
                else:
                    boat_occurrences[name["boat_name"]]=1
                    viable_in_port[i]+=1
                if not found_in_this_timestamp:
                    number_of_shore_power_timestamps+=1
                    found_in_this_timestamp=True
    
    print("percentage of time that at least 1 viable boat is in port:", (number_of_shore_power_timestamps/number_of_timestamps)*100, "%")
    #print(viable_in_port)

    sorted_boat_occurrences=sorted(boat_occurrences.items(), reverse=True, key=lambda x: x[1])

    print(len(boat_occurrences))
    #print(viable_boats)
    median_viable_boats=median(viable_in_port)
    mean_viable_boats=sum(viable_in_port)/len(viable_in_port)
    print("median: ", median_viable_boats)
    print("mean: ", mean_viable_boats)
    # plt.figure()
    # plt.plot(viable_in_port)
    plt.ylabel("Number of viable boats in port")
    plt.xlabel("timestamp index")


    boats=[]
    occurrences=[]

    for i in range(len(sorted_boat_occurrences)):
        boats.append(sorted_boat_occurrences[i][0])
        occurrences.append(sorted_boat_occurrences[i][1])

    # plt.figure()
    # plt.bar(boats,occurrences)
    plt.xticks([])
    plt.xlabel("Top boats")
    plt.ylabel("Number of times found in port")
    # plt.show()

    

    print(occurrences)



    uptimes=[]

    n=10

    if n>len(boats):
        n=len(boats)

    for i in range(n):
        uptimes.append(uptime(data,boats[0:i+1]))

    plt.plot(list(range(1,n+1)),uptimes)
    plt.xticks(list(range(1,n+1)))
    plt.xlabel("Number of top boats converted")
    plt.ylabel("% uptime")
    plt.title("Uptime of shore power vs number of top boats converted")
    plt.grid()
    plt.savefig("uptime_vs_boats_converted.png")
    plt.show()

