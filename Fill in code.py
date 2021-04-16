#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 15 16:16:18 2021

@author: benjaminlow
"""

""" FILL IN CODE """

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal
import Lab2Functions as l2f
import Lab2FunctionsNoPlot as l2fn
import GroupFunctions as gp


"""Import FILES!!"""


#Comment out missing trials 

data_quiz1, type1 =  gp.readfile("Quiz1.txt"), "Quiz 1"
data_quiz2, type2 =  gp.readfile("Quiz2.txt"), "Quiz 2"
data_quiz3, type3 =  gp.readfile("Quiz3.txt"), "Quiz 3"
#type = trial name in words so it can be used to define each chart

data_HRresting, type4 = gp.readfile("RestingHR.txt"), "Resting HR"
data_HRcontrol, type5 = gp.readfile("ControlHR.txt"), "Control HR"



"""Find Peaks"""
"run these and adjust the numbers to get all peaks"
peaksquiz1 = gp.findpeaks(data_quiz1, type1, 0.6, 1.0)
peaksquiz2 = gp.findpeaks(data_quiz2, type2, 0.6, 1.7)
peaksquiz3 = gp.findpeaks(data_quiz3, type3, 0.6, 1.0)
peaksrestingHR = gp.findpeaks(data_HRresting, type4, 0.6, 1.8)
peakscontrolHR = gp.findpeaks(data_HRcontrol, type5, 0.6, 1.8)


"""Find RR intervals and HR"""
RR_quiz1 = np.diff(peaksquiz1)
RR_quiz2 = np.diff(peaksquiz2)
RR_quiz3 = np.diff(peaksquiz3)
RR_HRresting = np.diff(peaksrestingHR)
RR_HRcontrol = np.diff(peakscontrolHR)


"Plots to visualize"
gp.plotRR(RR_quiz1, type1)
gp.plotRR(RR_quiz2, type2)
gp.plotRR(RR_quiz3, type3)
gp.plotRR(RR_HRresting, type4)
gp.plotRR(RR_HRcontrol, type5)


"""Calculate HR"""
heartrate_quiz1 = (1/RR_quiz1)*60
heartrate_quiz2 = (1/RR_quiz2)*60
heartrate_quiz3 = (1/RR_quiz3)*60
heartrate_HRresting = (1/RR_HRresting)*60
heartrate_HRcontrol = (1/RR_HRcontrol)*60


"Plot start to end"
yrange = [60,120]
#^^^ adjust y-lim for all HR plots to easily compare
#leave blank for best fit 
        #xrange = [] 
#change # to how many seconds at QUIZ start and end 
HRvsTQuiz1 = gp.plotHR(heartrate_quiz1, type1, 300, 900, yrange, peaksquiz1)
HRvsTQuiz2 = gp.plotHR(heartrate_quiz2, type2, 300, 900, yrange, peaksquiz2)
HRvsTQuiz3 = gp.plotHR(heartrate_quiz3, type3, 300, 900, yrange, peaksquiz3)
HRvsTResting = gp.plotHR(heartrate_HRresting, type4, 70, 200, yrange, peaksrestingHR)
#depends on how long your resting HR data is, i broke it up just cuz * just make sure they are withing x range *
HRvsTControl = gp.plotHR(heartrate_HRcontrol, type5, 300, 900, yrange, peakscontrolHR)


"HR Variable"
Quiz1_HRbegHR, Quiz1_midHR, Quiz1_HRendHR, Quiz1_HRbegHRV, Quiz1_midHRV, Quiz1_HRendHRV, Quiz1_HRAVG = gp.HRdata(HRvsTQuiz1, 300, 900, yrange, type1)
Quiz2_HRbeg, Quiz2_mid, Quiz2_HRend, Quiz2_HRbegHRV, Quiz2_midHRV, Quiz2_HRendHRV, Quiz2_HRAVG = gp.HRdata(HRvsTQuiz2, 300, 900, yrange, type2)
Quiz3_HRbeg, Quiz3_mid, Quiz3_HRend, Quiz3_HRbegHRV, Quiz3_midHRV, Quiz3_HRendHRV, Quiz3_HRAVG = gp.HRdata(HRvsTQuiz3, 300, 900, yrange, type3)
Resting_HRbeg, Resting_HRmid, Resting_HRend, Resting_HRbegHRV, Resting_midHRV, Resting_HRendHRV, Resting_HRAVG = gp.HRdata(HRvsTResting, 200, 500, yrange, type4)
Control_HRbeg, Control_HRmid, Control_HRend, Control_HRbegHRV, Control_midHRV, Control_HRendHRV, Control_HRAVG = gp.HRdata(HRvsTControl, 300, 900, yrange, type5)


"Tables of Values"

print("Trial \t \t HR - b \t HR - m \t HR - e|\t HRV - b\t HRV - m\t HRV - e|")
print(type1, "\t \t", Quiz1_HRbegHR,"\t", Quiz1_midHR,"\t", Quiz1_HRendHR, "|\t",Quiz1_HRbegHRV, "\t",Quiz1_midHRV, "\t",Quiz1_HRendHRV, "\t|", Quiz1_HRAVG )
print(type2, "\t \t", Quiz2_HRbeg, "\t",  Quiz2_mid, "\t",  Quiz2_HRend, "|\t",  Quiz2_HRbegHRV,  "\t", Quiz2_midHRV, "\t",  Quiz2_HRendHRV, "\t|", Quiz2_HRAVG )
print(type3, "\t \t", Quiz3_HRbeg, "\t",  Quiz3_mid, "\t",  Quiz3_HRend, "|\t",  Quiz3_HRbegHRV, "\t",  Quiz3_midHRV, "\t",  Quiz3_HRendHRV, "\t|", Quiz3_HRAVG  )
print(type4, "\t", Resting_HRbeg, "\t",  Resting_HRmid, "\t",  Resting_HRend, "|\t",  Resting_HRbegHRV,  "\t", Resting_midHRV,  "\t", Resting_HRendHRV, "\t|", Resting_HRAVG )
print(type5, "\t", Control_HRbeg, "\t",  Control_HRmid, "\t",  Control_HRend, "|\t",  Control_HRbegHRV, "\t", Control_midHRV, "\t",  Control_HRendHRV, "\t|", Control_HRAVG )

print("Peak Hr Quiz 1 = %", round(max(HRvsTQuiz1.Heartrate)))
print("Peak Hr Quiz 2 = %", round(max(HRvsTQuiz2.Heartrate)))
print("Peak Hr Quiz 3 = %", round(max(HRvsTQuiz3.Heartrate)))
print("Peak Hr Resting = %", round(max(HRvsTResting.Heartrate)))
print("Peak Hr Control = %", round(max(HRvsTControl.Heartrate)))

