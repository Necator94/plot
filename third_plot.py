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


# Std and mean criteria level arrays creation
        meanCr = []  # estimation level for mean value
        for i in enumerate(detect_signal[2]):
            meanCr.append(meanlevel)  # from metadata
        stdCr = []  # estimation level for std value
        for i in enumerate(detect_signal[3]):
            stdCr.append(stdlevel)  # from metadata

        gs2 = GridSpec(2, 1)
        gs2.update(left=0.05, right=0.98, wspace=0.1, hspace=0.6, bottom=0.2, top=0.89)
# Mean and standard deviation plot
        detect_plt = plt.subplot(gs2[0])
        detect_plt.grid(color='#c1c1c1', linestyle=':', linewidth=1)
        detect_plt.plot(detect_signal[0], detect_signal[2], 'k', linestyle='-', linewidth=2, label="Mean value of the signal")
        detect_plt.plot(detect_signal[0], meanCr, 'k', linestyle='--', linewidth=2, label="Mean value citeria level = " + str(meanlevel) )
        detect_plt.plot(detect_signal[0], detect_signal[3], 'g', linestyle='-', linewidth=2, label="Standard deviation value of the signal")
        detect_plt.plot(detect_signal[0], stdCr, 'g', linestyle='--', linewidth=2, label="Standard deviation criteria level = " + str(stdlevel))
        plt.xticks(np.arange(0, max(detect_signal[0]) + 1, 1.0))
        plt.axis([0, duration, 0, max(max(detect_signal[2]), max(detect_signal[3])) + 10])  # limits can be taken from metadata
        plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3, ncol=4, mode="expand", borderaxespad=0., fontsize=9)
        plt.ylabel('Relative values')
        plt.xlabel('Time, s')
        ttl = detect_plt.title
        ttl.set_position([.5, 1.2])
        plt.title('Mean and standard deviation plot for radio wave sensor signal, (a)')


        gs3 = GridSpec(4, 1)
        gs3.update(left=0.05, right=0.98, wspace=0.1, hspace=1.15, bottom=0.09, top=1.02)
# Ideal motion arrays creation
        id_mot_time = np.linspace(0, 30, 5000)
        id_mot_status = [0] * 5000
        for i, element in enumerate(id_mot_time):
            if element > 5 and element < 15:
                id_mot_status[i] = 1
            if element > 20 and element < 30:
                id_mot_status[i] = 1
# Ideal motion plot
        pl = plt.subplot(gs3[2])
        pl.plot(id_mot_time, id_mot_status, '#984300', linewidth=4)
        plt.fill_between(id_mot_time, id_mot_status, color='#984300',hatch='/', alpha='0.5')
        pl.text(7.7, 0.4, 'Real motion', color = 'w', fontsize=20, style='oblique')
        pl.text(22.7, 0.4, 'Real motion', color='w', fontsize=20, style='oblique')
        plt.axis([0, duration, 0, 1.1])  # limits can be taken from metadata
        plt.yticks(np.arange(0, 1.1, 1.0))
        plt.ylabel('Motion status')
        plt.xlabel('Time, s')
        plt.title('Real motion, (b)')
# Movement detection plot for radar sensor
        pl = plt.subplot(gs3[3])
        pl.plot(detect_signal[0], detect_signal[1], 'b', linewidth=4, label = "X-Band sensor detection status")
        plt.fill_between(detect_signal[0], detect_signal[1], color='b', hatch='/', alpha='0.5')
        plt.axis([0, duration, 0, 1.1])  # limits can be taken from metadata
        plt.yticks(np.arange(0, max(detect_signal[1]) + 0.1, 1.0))
        plt.xticks(np.arange(0, max(detect_signal[0]), 1.0))
        plt.ylabel('Motion status')
        plt.xlabel('Time, s')
        plt.title('Movement detection graph for radar sensor, (c)')


#        plt.savefig(out_path + file[10:-5] + '.png')
#        os.rename(file, out_path + file)
        plt.show()
