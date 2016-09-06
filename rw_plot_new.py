#!/usr/bin/env python
#plot graph
import matplotlib
import matplotlib.pyplot as plt
import sys
from matplotlib.gridspec import GridSpec
matplotlib.rcParams.update({"figure.figsize": (11.0, 5.0)})
import numpy as np
import os
import logging
import matplotlib.patches as patches

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
        meanlevel = 25
        stdlevel = 20
#        meanlevel = int(sys.argv[1][:2])
 #       stdlevel = int(sys.argv[1][-2:])
        '''
        a = []
        b = []
        for i, element in enumerate(xBand_raw_data):
            a.append(xBand_raw_data[i])
            b.append(xBand_raw_time[i])
            if len(a) > 500:
                a = []
                b = []
            if len(a) == 500:
                for s in range(len(a)):
                    if s > 1 and a[s] > a[s - 1]:
                        periods.append(b[s])
                        print periods
                    if len(periods) > 1:
                        freq = 1 / (periods[-1] - periods[-2])
                        fr_trans_graph[0].append(xBand_raw_time[i - 1])
                        fr_trans_graph[1].append(freq)
                        slide_window.append(freq)
                st_dev = np.std(slide_window)  # standard deviation
                mean_vol = np.mean(slide_window)
                periods = []
                slide_window = []
                detect_signal[0].append(xBand_raw_time[i])
                detect_signal[2].append(mean_vol)
                detect_signal[3].append(st_dev)
                '''


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

        gs1 = GridSpec(2, 1)
        gs1.update(left=0.069, right=0.98, wspace=0.1, hspace=0.75, bottom=0.11, top=0.93)
 #       plt.suptitle('Sensor response for ' + file[10:-5] + ' meters', fontsize=20)

# Frequency transform plot for X-Band
        fr_tr_plt = plt.subplot(gs1[0])
        fr_tr_plt.grid(color='#c1c1c1', linestyle=':', linewidth=1)
        fr_tr_plt.plot(fr_trans_graph[0], fr_trans_graph[1], 'b', linewidth=2)
        plt.xticks(np.arange(0, max(detect_signal[0]) + 1, 1.0))
        plt.ylabel('Frequency, Hz')
        plt.xlabel('Time, s')
        plt.title('Frequency transformation graph for raw radio wave sensor signal, (a)')

        fr_tr_plt.add_patch(
            patches.Ellipse((12.33, 35), 2, 65, color='r', zorder=10, fill=False, linewidth=3))
# Std and mean criteria level arrays creation
        meanCr = []  # estimation level for mean value
        for i in enumerate(detect_signal[2]):
            meanCr.append(meanlevel)  # from metadata
        stdCr = []  # estimation level for std value
        for i in enumerate(detect_signal[3]):
            stdCr.append(stdlevel)  # from metadata


# Mean and standard deviation plot
        detect_plt = plt.subplot(gs1[1])
        detect_plt.grid(color='#c1c1c1', linestyle=':', linewidth=1)
        detect_plt.plot(detect_signal[0], detect_signal[2], 'k', linestyle='-', linewidth=2, label="Mean value of the signal")
        detect_plt.plot(detect_signal[0], meanCr, 'k', linestyle='--', linewidth=2, label="Mean value citeria level = " + str(meanlevel) )
        detect_plt.plot(detect_signal[0], detect_signal[3], 'g', linestyle='-', linewidth=2, label="Standard deviation value of the signal")
        detect_plt.plot(detect_signal[0], stdCr, 'g', linestyle='--', linewidth=2, label="Standard deviation criteria level = " + str(stdlevel))

        detect_plt.text(2, 15, 'Standatd deviation criteria', fontsize=13, color = 'g')
        detect_plt.text(2, 26, 'Mean criteria', fontsize=13, )
        plt.xticks(np.arange(0, max(detect_signal[0]) + 1, 1.0))
        plt.axis([0, duration, 0, max(max(detect_signal[2]), max(detect_signal[3])) + 10])  # limits can be taken from metadata
        plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3, ncol=4, mode="expand", borderaxespad=0., fontsize=9)
        detect_plt.add_patch(
            patches.Ellipse((12.7, 16), 2, 33, color='r', zorder=10, fill=False, linewidth=3))
        plt.ylabel('Mean and\n st. deviation values')
        plt.xlabel('Time, s')
        ttl = detect_plt.title
        ttl.set_position([.5, 1.18])
        plt.title('Mean and standard deviation plot for radio wave sensor signal, (b)')


#        plt.savefig(out_path + file[10:-5] + '.png')
#        os.rename(file, out_path + file)
        plt.show()
