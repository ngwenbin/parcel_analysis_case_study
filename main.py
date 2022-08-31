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


container_1_df = getUnloadContDf(1).sort_values("enter_time_sec")
enterTimeData = container_1_df["enter_time_sec"].to_numpy()
leaveTimeData = container_1_df["leave_time_sec"].to_numpy()

### Capacity calculation

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
            X.append("{0}:{1}".format(minute, second))
            Y.append(currParcelsInQueue)
            parcelQueue.pop(0)

        parcelQueue.insert(0, parcelLeaveTime) if parcelLeaveTime < parcelQueue[
            0
        ] else parcelQueue.append(parcelLeaveTime)

        parcelQueue.sort()
    parcelQueue.append(parcelLeaveTime)

# print(X, Y, currParcelsInQueue)

fig, ax = plt.subplots()
ax.plot(X, Y)
ax.xaxis.set_major_locator(ticker.MultipleLocator(7))
plt.show()
