#!/usr/bin/env python
#plot graph
import matplotlib
import matplotlib.pyplot as plt
import sys
from matplotlib.gridspec import GridSpec
matplotlib.rcParams.update({"figure.figsize": (10.0, 4.0)})
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

        duration = max(xBand_raw_time)
        meanlevel = 20
        stdlevel = 15
#        meanlevel = int(sys.argv[1][:2])
 #       stdlevel = int(sys.argv[1][-2:])


        gs1 = GridSpec(3, 1)
        gs1.update(left=0.04, right=0.98, wspace=0.1, hspace=1.3, bottom=0.12, top=0.93)
 #
# Signal reverse for PIR-2
        for i, element in enumerate(pir2_detect_status):
            if element == 1:
                pir2_detect_status[i] = 0
            else:
                pir2_detect_status[i] = 1

# Ideal motion arrays creation
        id_mot_time = np.linspace(0, 30, 5000)
        id_mot_status = [0] * 5000
        for i, element in enumerate(id_mot_time):
            if element > 5 and element < 15:
                id_mot_status[i] = 1
            if element > 20 and element < 30:
                id_mot_status[i] = 1
# Ideal motion plot
        pl = plt.subplot(gs1[0])
        pl.plot(id_mot_time, id_mot_status, '#984300', linewidth=4)
        plt.fill_between(id_mot_time, id_mot_status, color='#984300',hatch='/', alpha='0.5')
        pl.text(9, 0.4, 'Motion', color = 'w', fontsize=20, style='oblique')
        pl.text(24, 0.4, 'Motion', color='w', fontsize=20, style='oblique')
        plt.axis([0, duration, 0, 1.1])  # limits can be taken from metadata
        plt.yticks(np.arange(0, 1.1, 1.0))
        plt.ylabel('Motion status')
        plt.xlabel('Time, s')
        plt.title('Real motion, (a)')
# Movement detection plot for PIR-1 sensor
        pir1_plt = plt.subplot(gs1[1])
        pir1_plt.plot(pir1_detect_time, pir1_detect_status, 'r', linestyle='-', linewidth=4)
        plt.fill_between(pir1_detect_time, pir1_detect_status, color='r', hatch='/', alpha='0.5')
        plt.axis([0, duration, 0, 1.1])  # limits can be taken from metadata
        plt.legend(loc='upper left', frameon=False)
        plt.ylabel('Motion status')
        plt.xlabel('Time, s')
        plt.yticks(np.arange(0, max(pir1_detect_status) + 0.1, 1.0))
        plt.xticks(np.arange(0, max(pir1_detect_time), 1.0))
        plt.title('Movement detection graph for PIR-1 sensor, (b)')
# Movement detection plot for PIR-2 sensor
        pir2_plt = plt.subplot(gs1[2])
        pir2_plt.plot(pir2_detect_time, pir2_detect_status, '#ff9900', linestyle='-', linewidth=4)
        plt.fill_between(pir2_detect_time, pir2_detect_status, color='#ff9900', hatch='/', alpha='0.5')
        plt.axis([0, duration, 0, 1.1])  # limits can be taken from metadata
        plt.legend(loc='upper left', frameon=False)
        plt.ylabel('Motion status')
        plt.xlabel('Time, s')
        plt.yticks(np.arange(0, max(pir2_detect_status) + 0.1, 1.0))
        plt.xticks(np.arange(0, max(pir2_detect_time), 1.0))
        plt.title('Movement detection graph for PIR-2 sensor, (c)')

#        plt.savefig(out_path + file[10:-5] + '.png')
#        os.rename(file, out_path + file)
        plt.show()
