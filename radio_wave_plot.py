#!/usr/bin/env python
#plot graph
import matplotlib
import matplotlib.pyplot as plt
import sys
from matplotlib.gridspec import GridSpec
matplotlib.rcParams.update({"figure.figsize": (11.0, 6.0)})
import numpy as np
import os
import logging
import matplotlib.patches as patches
from pylab import *
from matplotlib.patches import Ellipse
from matplotlib.patches import ConnectionPatch


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("plot_all")

for file in os.listdir("."):
    if file.endswith(".data"):

        periods = []
        fr_trans_graph = []
        for i in range(2): fr_trans_graph.append([])
        detect_signal = []
        for i in range(4): detect_signal.append([])
        slide_window = []
        st_dev = 0
        mean_vol = 0

        xBand_raw_time = []
        xBand_raw_data = []

        pir1_detect_time = []
        pir1_detect_status = []

        pir2_detect_time = []
        pir2_detect_status = []

        raw_data_flag = 'foo bar'
        pir1_detect_signal_flag = 'foo bar'
        pir2_detect_signal_flag = 'foo bar'
        exp_parameter_flag = 'foo bar'

        plot_data = open(file, "r")
        for line in plot_data:

            if line == "row_data\n":
                raw_data_flag = True
                continue
            if line == "/end_of_row_data\n":
                raw_data_flag = False
                continue
            if raw_data_flag == True:
                string = line.split()
                xBand_raw_time.append(float(string[0]))
                xBand_raw_data.append(int(string[1]))

            if line == "pir1_detect_signal\n":
                pir1_detect_signal_flag = True
                continue
            if line == "/end_of_pir1_detect_signal\n":
                pir1_detect_signal_flag = False
                continue
            if pir1_detect_signal_flag == True:
                string = line.split()
                pir1_detect_time.append(float(string[0]))
                pir1_detect_status.append(int(string[1]))

            if line == "pir2_detect_signal\n":
                pir2_detect_signal_flag = True
                continue
            if line == "/end_of_pir2_detect_signal\n":
                pir2_detect_signal_flag = False
                continue
            if pir2_detect_signal_flag == True:
                string = line.split()
                pir2_detect_time.append(float(string[0]))
                pir2_detect_status.append(int(string[1]))
            '''
            if line == "exp_parameter\n":
                exp_parameter_flag = True
                continue
            if line == "/end_of_exp_parameter\n":
                exp_parameter_flag = False
                continue
            if exp_parameter_flag == True:
                string = line.split()
                duration = int(string[0])
                meanlevel = int(string[1])
                stdlevel = int(string[2])

            '''
        duration = max(xBand_raw_time)
        meanlevel = 20
        stdlevel = 15
#        meanlevel = int(sys.argv[1][:2])
 #       stdlevel = int(sys.argv[1][-2:])


        for i, element in enumerate(xBand_raw_data):
            if i > 1 and xBand_raw_data[i] > xBand_raw_data[i - 1]:
                periods.append(xBand_raw_time[i])
                if len(periods) > 1:
                    freq = 1 / (periods[-1] - periods[-2])
                    fr_trans_graph[0].append(xBand_raw_time[i - 1])
                    fr_trans_graph[1].append(freq)
                    slide_window.append(freq)
                    if len(slide_window) > 3:
                        slide_window = []
                    if len(slide_window) == 3:
                        st_dev = np.std(slide_window)  # standard deviation
                        mean_vol = np.mean(slide_window)

                    if mean_vol > meanlevel and st_dev < stdlevel:
                        detect_signal[0].append(xBand_raw_time[i])
                        detect_signal[1].append(1)
                        detect_signal[2].append(mean_vol)
                        detect_signal[3].append(st_dev)
                    else:
                        detect_signal[0].append(xBand_raw_time[i])
                        detect_signal[1].append(0)
                        detect_signal[2].append(mean_vol)
                        detect_signal[3].append(st_dev)
                    del periods[0]

        gs1 = GridSpec(3, 1)
        gs1.update(left=0.07, right=0.98, wspace=0.1, hspace=0.65, bottom=0.09, top=0.93)
 #       plt.suptitle('Sensor response for ' + file[10:-5] + ' meters', fontsize=20)
# Raw X-Band data plot

        raw_plt = plt.subplot(gs1[0])

        raw_plt.plot(xBand_raw_time, xBand_raw_data, 'b', zorder=1)
        raw_plt.grid(color='#c1c1c1', linestyle=':', linewidth=1)
        plt.yticks(np.arange(0, 1.1, 1.0))
        plt.axis([0, duration, 0, max(xBand_raw_data) + 0.1])  # limits can be taken from metadata
        plt.ylabel('Motion status')
        plt.xlabel('Time, s')
        plt.title('Raw radio wave sensor signal, (a)')

        raw_plt.add_patch(
            patches.Ellipse((10.5, 0.5), 3, 1, color='r', zorder=10, fill=False, linewidth=3))
        '''
        a = plt.axes([0.5, 0.7, .3, .2], axisbg='w')
        a.plot(xBand_raw_time, xBand_raw_data, 'b')
        a.axis([0, 3, 0, max(xBand_raw_data) + 0.1])  # limits can be taken from metadata
        '''
        pl = plt.subplot(gs1[1])
        pl.plot(xBand_raw_time, xBand_raw_data, 'b', zorder=1)
        pl.grid(color='#c1c1c1', linestyle=':', linewidth=1)
        plt.yticks(np.arange(0, 1.1, 1.0))
        plt.axis([9, 11, 0, max(xBand_raw_data) + 0.1])  # limits can be taken from metadata
        plt.ylabel('Motion status')
        plt.xlabel('Time, s')
        plt.title('Scaled segment of raw signal, (b)')

        xy = (1, 1)
        coordsA = "data"
        coordsB = "data"
        con = ConnectionPatch(xyA=(9.4,1.1), xyB=(9.4, 0.1), coordsA=coordsA, coordsB=coordsB,
                              axesA=pl, axesB=raw_plt,
                              arrowstyle="->", shrinkB=5,linewidth=10, color='r')
        pl.add_artist(con)

# Frequency transform plot for X-Band
        fr_tr_plt = plt.subplot(gs1[2])
        fr_tr_plt.grid(color='#c1c1c1', linestyle=':', linewidth=1)
        fr_tr_plt.plot(fr_trans_graph[0], fr_trans_graph[1], 'b', linewidth=2)
        plt.ylabel('Frequency, Hz')
        plt.xlabel('Time, s')
        plt.title('Frequency transformation graph for raw radio wave signal, (c)')





#        plt.savefig(out_path + file[10:-5] + '.png')
#        os.rename(file, out_path + file)
        plt.show()
