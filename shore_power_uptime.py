import json 
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.ticker as tck

def read_dundee_port_data():
    #reads the data about the vessels that come to Dundee port
    with open("dundee_port_data.json", "r") as f:
        return json.load(f)

def read_viable_boats_file():
    #reads the list of shore power viable vessels that have come to Dundee port
    with open("viable_boats.txt", "r") as f:
        lines = f.readlines()

    for i in range(len(lines)):
        if "\n" in lines[i]:
            lines[i]=lines[i][:-1]

    return lines

def uptime(data,boats):
    #determines the percent uptime based on on the names of boats passed in
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


data = read_dundee_port_data()
viable_boats=read_viable_boats_file()

number_of_timestamps=0
number_of_shore_power_timestamps=0

viable_in_port=[]

boat_occurrences={}

for i in range(len(data)): #loop over boat data
    viable_in_port.append(0)
    number_of_timestamps+=1
    found_in_this_timestamp=False
    for name in data[i]["boats"]: #loop over every boat in each timestamp
        if name["boat_name"] in viable_boats: #if one of the vessels found is viable for shore power
            if name["boat_name"] in boat_occurrences.keys(): #checks if the vessel is already in the dict
                viable_in_port[i]+=1 #increments the number of shore power viable vessels this timestamp
                boat_occurrences[name["boat_name"]]+=1 #if already in dict increment
            else:
                boat_occurrences[name["boat_name"]]=1 #if not in dict, set to 1
                viable_in_port[i]+=1 #increments the number of shore power viable vessels this timestamp
            if not found_in_this_timestamp:
                number_of_shore_power_timestamps+=1
                found_in_this_timestamp=True

#sorts the vessels by number of occurrences in the boat data
sorted_boat_occurrences=sorted(boat_occurrences.items(), reverse=True, key=lambda x: x[1])

#mind the mean value of viable in port
mean_viable_boats=sum(viable_in_port)/len(viable_in_port)

#figure 4
plt.rcParams['axes.xmargin'] = 0
plt.figure()
plt.plot(viable_in_port)
plt.axhline(y=mean_viable_boats,color="r",linestyle="--")
plt.ylabel("Number of viable boats in port")
plt.xlabel("Time")
plt.grid()
plt.ylim([0,max(viable_in_port)+1])
plt.xticks([])
plt.savefig("number_of_viable_boats_in_port.png")

boats=[]
occurrences=[]

#loop over and rearrange data
for i in range(len(sorted_boat_occurrences)):
    boats.append(sorted_boat_occurrences[i][0])
    occurrences.append(sorted_boat_occurrences[i][1])

#figure 2
plt.rcParams['axes.xmargin'] = 0
a=9
plt.figure(figsize=(a,a/(4/3)),dpi=80)
n=30
plt.bar(range(1,n+1),(np.array(occurrences[0:n])/len(data))*100,align="center",width=0.8)
plt.xticks(range(1,n+1))
plt.yticks(range(0,52,2))
plt.xlabel("Vessels")
plt.ylabel("Percentage of timestamps in port")
plt.grid(which="both",axis="y")
plt.savefig("number_of_occurences_of_boats.png")

uptimes=[]

n=6
if n>len(boats):
    n=len(boats)

#find the uptime for top 1 vessel, then top 2 vessels ect up to top n boats
for i in range(n):
    uptimes.append(uptime(data,boats[0:i+1]))

#figure 4
plt.rcParams['axes.xmargin'] = 0
plt.figure()
plt.plot(list(range(1,n+1)),uptimes)
plt.xticks(list(range(1,n+1)))
plt.xlabel("Number of top vessels converted")
plt.ylabel("Percentage uptime")
plt.ylim([0,105])
plt.grid(which="both", axis="both")
plt.yticks(range(0,105,5))
plt.savefig("uptime_vs_boats_converted.png")
