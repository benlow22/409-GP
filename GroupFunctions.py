#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 15 17:08:17 2021

@author: benjaminlow
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal
import Lab2Functions as l2f
import Lab2FunctionsNoPlot as l2fn

column_names = [
    "ecg",
    "t"
]

Wn = 0.1
b, a = scipy.signal.butter(4, Wn, 'low', analog = False) 

def readfile (filename):
    data = pd.read_csv(filename,
    names = column_names, sep = '\t', skiprows = 500, skipfooter = 500, engine='python')
    data.t = data.t/1000
    return data

def findpeaks(file, trial, H, W):
    d_ecg, peaks_d_ecg = l2fn.decg_peaks(file.ecg,file.t)
    Rwave_peaks_d_ecg = l2fn.d_ecg_peaks(d_ecg, peaks_d_ecg, file.t, H, W)
    exercise_Rwave_t = l2f.Rwave_peaks(file.ecg, d_ecg, Rwave_peaks_d_ecg, file.t, trial)
    return exercise_Rwave_t


def plotRR(file,trial):
    plt.figure()
    plt.plot(file)
    plt.xlabel('NOT time, # of data points') 
    plt.title('RR intervals of ' + trial)
    plt.ylabel('time/distance between RR [s]')
    return

def xaxis(peakfile):
    newaxis = []
    for i in range(len(peakfile)-1):
        newaxis.append((peakfile[i] + peakfile[i+1])/2)
    return newaxis

def plotHR(file,trial,start,end,xrange,peak):
    Wn = 0.2
    b2, a2 = scipy.signal.butter(4, Wn, btype='lowpass') #find a good value for Wn
    filtHR = scipy.signal.filtfilt(b2, a2, file)
    t = xaxis(peak)
    HRvsT = pd.DataFrame(
        {'Heartrate': filtHR,
         't': t
         })
    plt.figure()
    plt.title('HR for ' + trial)
    plt.plot(HRvsT.t, HRvsT.Heartrate)
    plt.xlabel('Time [s] FUCK THIS') 
    plt.ylabel('HR [BPM]')
    plt.ylim(xrange)
    plt.axvline(start, color = 'red', label = "start time")
    plt.axvline(end, color = 'black', label = "end time")
    plt.legend()
    return HRvsT



def timecheck(file, start, end, xrange, trial):
    plt.figure()
    plt.title('HR for ' + trial)
    plt.plot(file.t, file.Heartrate)
    plt.xlabel('Time [s]') 
    plt.ylabel('HR [BPM]')
    plt.ylim(xrange)
    plt.axvline(start, color = 'red', label = "start time")
    plt.axvline(end, color = 'black', label = "end time")
    plt.legend()
    return 


  

def HRdata(file, start, end, xrange, trial):
    starttimeIndex = 0
    for i in range(len(file)):
        if file.t[i] >= start:
            starttimeIndex = i
            break
    endtimeIndex = 0
    for i in range(len(file)):
        if file.t[i] >= end:
            endtimeIndex = i
            break
    s = file[0:starttimeIndex]
    m = file[starttimeIndex:endtimeIndex]
    e = file[endtimeIndex:] 
    avgHRs = round(sum(file.Heartrate[0:starttimeIndex])/len(file[0:starttimeIndex]),2)
    avgHRm = round(sum(file.Heartrate[starttimeIndex:endtimeIndex])/len(file[starttimeIndex:endtimeIndex]),2)
    avgHRe = round(sum(file.Heartrate[endtimeIndex:])/len(file[endtimeIndex:(len(file))]),2)
    plt.figure()
    plt.title('HR for ' + trial)
    plt.plot(file.t, file.Heartrate, zorder =1)
    plt.xlabel('Time [s]') 
    plt.ylabel('HR [BPM]')
    plt.ylim(xrange)
    plt.axvline(start, color = 'red', label = "start time")
    plt.axvline(end, color = 'y', label = "end time")
    plt.legend()
    plt.hlines(y=avgHRs, xmin=file.t[0], xmax=start, linewidth=2, color='k', zorder =2)
    plt.hlines(y=avgHRm, xmin=start, xmax=end, linewidth=2, color='k', zorder =2)
    plt.hlines(y=avgHRs, xmin=end, xmax=file.t[len(file)-1], linewidth=2, color='k', zorder =2)
    avgHRVs = round(np.std(s.Heartrate),2)
    avgHRVm = round(np.std(m.Heartrate),2) 
    avgHRVe = round(np.std(e.Heartrate),2)
    totalavg = round(sum(file.Heartrate)/len(file))
    return avgHRs, avgHRm, avgHRe, avgHRVs, avgHRVm, avgHRVe, totalavg


