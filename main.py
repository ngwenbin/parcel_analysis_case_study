# Variables

# parcel_id
# parcel_type
# enter_time
# leave_time
# unloading_container
# unloading_port
# loading_container
# loading_port

# Problem statement
# Find out key drivers of processing time of the parcels. When the facility is more congested with parcels, processing time will increase.
# Define congestion -> Congestion of a parcel is defined by its moving speed container operating capacity.
# This is similar to a car on an expressway, number of cars on the expressway and car's moving speed.

import numpy as np
import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

rawDf = pd.read_excel("data.xlsx", usecols="B:L", sheet_name="Sheet4")
fig, ax = plt.subplots()
ax.xaxis.set_major_locator(ticker.MultipleLocator(10))


def floatHourToTime(fh):
    hours, hourSeconds = divmod(fh, 1)
    minutes, seconds = divmod(hourSeconds * 60, 1)
    return (
        int(hours),
        int(minutes),
        int(seconds * 60),
    )


def getUnloadContDf(container_num):
    return rawDf.loc[rawDf["unloading_container"] == container_num]


### Capacity calculation
def getContainerCapacity(unloadingContainer):
    containerDf = getUnloadContDf(unloadingContainer).sort_values("enter_time_sec")
    enterTimeData = containerDf["enter_time_sec"].to_numpy()
    leaveTimeData = containerDf["leave_time_sec"].to_numpy()

    parcelQueue = []  # sorted by earliest leave time
    X = []
    Y = []
    currParcelsInQueue = 0
    for idx, entryTime in enumerate(enterTimeData):
        currParcelsInQueue += 1
        parcelLeaveTime = leaveTimeData[idx]
        if parcelQueue:
            if entryTime > parcelQueue[0]:
                currParcelsInQueue -= 1
                hour, minute, second = floatHourToTime(entryTime % 1)
                X.append("{0}:{1}:{2}".format(hour + 8, minute, second))
                Y.append(currParcelsInQueue)
                parcelQueue.pop(0)

            parcelQueue.insert(0, parcelLeaveTime) if parcelLeaveTime < parcelQueue[
                0
            ] else parcelQueue.append(parcelLeaveTime)

            parcelQueue.sort()
        parcelQueue.append(parcelLeaveTime)

    ax.plot(X, Y, label="Container: {0}".format(unloadingContainer))


containers = [1, 2, 3, 4, 5]
for container in containers:
    getContainerCapacity(container)

plt.ylabel("Parcels in queue")
plt.xlabel("Time")
plt.legend()
plt.show()
