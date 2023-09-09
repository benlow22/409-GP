#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 14 13:49:39 2021

@author: benjaminlow
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy.signal as sps
import lab4functions as l4f

column_names = [
      'x',
      'y',
      'z',
      't',
      'activity'
    ]


df = pd.read_csv('LabelledDataBL.csv')
time = df.t/1000 #plots seconds to use as a variable



fig,ax=plt.subplots()
plt.title('labelled Data')
ax.plot(time, df.x)
ax.plot(time, df.y)
ax.plot(time, df.z)
ax.set_ylabel("Accelerations (G)")
ax.set_xlabel("Time (s)")
ax.legend('xyz', loc = "upper center")
ax2=ax.twinx()          #create second Axis on right for activity 
ax2.plot(time, df.activity, color = 'black')

#calculate SF
sfreq = 1000/np.mean(np.diff(df.t))

"""Isolate walking and running Data"""
stepdata = df.loc[(df.activity == "Running")|(df.activity == "Walking")]
#reset index
stepdata = stepdata.reset_index(drop = True)
stepdata_time = stepdata.t/1000


#plot the Run and walking data
plt.figure(2)
plt.plot(stepdata_time, stepdata.x)
plt.plot(stepdata_time, stepdata.y)
plt.plot(stepdata_time, stepdata.z)
plt.title('isolated Walking and Running') 
plt.xlabel("Time [s]")
plt.ylabel("Acceleration [G]")
plt.legend('xyz')
#lines because there is no data points theres

"""Filter Running and Walking Data"""
low_pass = 3 # critical frequency 
low_pass1 = low_pass/(sfreq/2) #sfreq/2 = nyquist fq (~12) = ~1/4 = new critical fq between 0-1
b2, a2 = sps.butter(4, low_pass1, btype = 'lowpass')
xfilt = sps.filtfilt(b2, a2, stepdata.x)            #filtering each axis
yfilt = sps.filtfilt(b2, a2, stepdata.y)
zfilt = sps.filtfilt(b2, a2, stepdata.z)

xfilt_peaks,_ = sps.find_peaks(xfilt,distance = 5)  #peaks of filtered running/walking
yfilt_peaks,_ = sps.find_peaks(yfilt)  #peaks of filtered running/walking
 #peaks of filtered running/walking
# i wanted to filter both to see because i think Y would be more accurate or hopefully the same


plt.figure(2)
plt.plot(stepdata_time, xfilt)
plt.plot(stepdata_time[xfilt_peaks], xfilt[xfilt_peaks], "x", color = "r")
plt.xlim([84, 89])
plt.title('Peaks of Filtere Data') 
plt.xlabel("Time [s]")
plt.ylabel("Acceleration [G]")
plt.legend()





""" TRY seperating walking and running for more accurate filters"""

###Divide running and walking
stepdata_running = stepdata[stepdata['t'] <=400000]
stepdata_walking = stepdata[stepdata['t'] >=400000]
stepdata_running_time = stepdata_running.t/1000
stepdata_walking_time = stepdata_walking.t/1000

plt.figure(4)
plt.plot(stepdata_running_time, stepdata_running.x, color = "C0")
plt.plot(stepdata_walking_time, stepdata_walking.x, color = "C0")
plt.title('isolated Walking and Running') 
plt.xlabel("Time [s]")
plt.ylabel("Acceleration [G]")
plt.legend('x')


"""Filter NEW Running Data"""
xfilt_stepdata_running = sps.filtfilt(b2, a2, stepdata_running.x)            #filtering each axis
xfilt_stepdata_running_peaks,_ = sps.find_peaks(xfilt_stepdata_running,height = 0.5)  #peaks of filtered running/walking
#peaks of filtered running/walking
# i wanted to filter both to see because i think Y would be more accurate or hopefully the same

"""Filter NEW Walking Data"""
xfilt_stepdata_walking = sps.filtfilt(b2, a2, stepdata_walking.x)            #filtering each axis
xfilt_stepdata_walking_peaks,_ = sps.find_peaks(xfilt_stepdata_walking,height = 0.3, width = 5.75)  #peaks of filtered running/walking
#peaks of filtered running/walking
# i wanted to filter both to see because i think Y would be more accurate or hopefully the same

plt.figure(3)
plt.plot(stepdata_running_time, xfilt_stepdata_running, color ='C0')
plt.plot(stepdata_running_time[xfilt_stepdata_running_peaks], xfilt_stepdata_running[xfilt_stepdata_running_peaks], "x", color = "g")

plt.plot(stepdata_walking_time, xfilt_stepdata_walking, color ='C0')
plt.plot(stepdata_walking_time[5944+xfilt_stepdata_walking_peaks], xfilt_stepdata_walking[xfilt_stepdata_walking_peaks], "x", color = "r")
    # because walking data index starts at 5944, but the "peaks" start at 0
plt.title('Benjamin - Peaks of Filtered Data X-axis - Running') 
plt.xlabel("Time [s]")
plt.ylabel("Acceleration [G]")


stepcount_R1 = l4f.stepcount(0,200,stepdata_running_time,xfilt_stepdata_running_peaks)
stepcount_R2 = l4f.stepcount(200,400,stepdata_running_time,xfilt_stepdata_running_peaks)
stepcount_W1 = l4f.stepcount(400,560,stepdata_walking_time,xfilt_stepdata_walking_peaks)
stepcount_W2 = l4f.stepcount(560,750,stepdata_walking_time,xfilt_stepdata_walking_peaks)


print("Step count for 1st Run = ", stepcount_R1, "\t Actual = 308" )
print("Step count for 2nd Run = ", stepcount_R2, "\t Actual = 302" )
print("Step count for 1st Walk = ", stepcount_W1*2, "\t Actual = 212" )
print("Step count for 2nd Walk  = ", stepcount_W2*2, "\t Actual = 242" )
