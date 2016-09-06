#!/usr/bin/env python
#plot graph
import matplotlib
import matplotlib.pyplot as plt
import sys
from matplotlib.gridspec import GridSpec
#matplotlib.rcParams.update({"figure.figsize": (25.0, 13.0)})
import numpy as np
import os
import matplotlib.patches as patches




def calc_center(time_ar, stat_ar, coeff):
    front = []
    bfront = []
    diff = []
    center = []
    out = []
    for i in range(2): out.append([])
    for i, element in enumerate(stat_ar):
        if element > stat_ar[i - 1] and time_ar[i] > 2: front.append(time_ar[i])
        if element < stat_ar[i - 1] and time_ar[i] > 2: bfront.append(time_ar[i])
    if len(bfront) < len(front): bfront.append(30)
    for i in range(len(front)): diff.append(bfront[i] - front[i])
    for i in range(len(front)):
        if front[i] < 20: center.append(((front[i] + diff[i] - 5) * 1.4) - coeff)
        else: center.append(14 + coeff - (((front[i] + diff[i]) - 20) * 1.4))
    out[0] = center
    out[1] = diff
    return out

def pl_point(inp, cl):
    center = inp[0]
    diff = inp[1]
    for i in range(len(center)):
        detect_plt.add_patch(
            patches.Ellipse((int(file[10:-6]), center[i]), 0.2, diff[i], color = cl, zorder=10, fill=False, linewidth=3))




gs2 = GridSpec(1, 1)
detect_plt = plt.subplot(gs2[0])

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
        meanlevel = 25
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

# Signal reverse for PIR-2
        for i, element in enumerate(pir2_detect_status):
            if element == 1: pir2_detect_status[i] = 0
            else: pir2_detect_status[i] = 1

 #       pl_point(calc_center(pir1_detect_time, pir1_detect_status, 7), "r")
        pl_point(calc_center(detect_signal[0], detect_signal[1], 0), "b")
#        pl_point(calc_center(pir2_detect_time, pir2_detect_status, 6), "#ff9900")


plt.suptitle('Detection area for ' , fontsize=20)
plt.grid(color='#c1c1c1', linestyle='-', linewidth=1)
detect_plt.add_patch(
    patches.Ellipse((0, 7), 0.5, 0.5, color="black", zorder=10, linewidth=3))

gs2.update(left=0.03, right=0.98, wspace=0.1, hspace=0.6, bottom=0.05, top=0.93)



plt.xticks(np.arange(0, 12, 1.0))
plt.yticks(np.arange(0, 15, 1.0))
plt.axis([0, 11, 0, 14])
#        plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3, ncol=4, mode="expand", borderaxespad=0.)
plt.ylabel('Width, m')
plt.xlabel('Length, m')
#        ttl = detect_plt.title
#        ttl.set_position([.5, 1.2])
 #       make_ticklabels_invisible(plt.gcf())
#        plt.title('Mean and standard deviation plot for radio wave sensor signal, (c)')
plt.show()
