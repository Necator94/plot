#!/usr/bin/env python
#plot graph
import matplotlib
import matplotlib.pyplot as plt
import sys
from matplotlib.gridspec import GridSpec
matplotlib.rcParams.update({"figure.figsize": (25.0, 13.0)})
import numpy as np
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("plot_all")

#try:
#    sys.argv[1]
#except NameError:
#    logger.error('type argv[1] - as a folder name in processed data directory (../processed_data/folder_name)  ')

#out_path = '../processed_data/' + sys.argv[1] + '/'
#if os.path.exists(out_path):
#    print "path exists, + new folder created"
#    out_path = '../processed_data/' + sys.argv[1] + '_new' + '/'
#    os.makedirs(out_path)
#else:
#    os.makedirs(out_path)

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
                pir1_detect_time.append(string[0])
                pir1_detect_status.append(string[1])

            if line == "pir2_detect_signal\n":
                pir2_detect_signal_flag = True
                continue
            if line == "/end_of_pir2_detect_signal\n":
                pir2_detect_signal_flag = False
                continue
            if pir2_detect_signal_flag == True:
                string = line.split()
                pir2_detect_time.append(string[0])
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
        duration = 30
        meanlevel = int(sys.argv[1][:2])
        stdlevel = int(sys.argv[1][-2:])


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

        gs1 = GridSpec(3, 2, height_ratios=[4, 1])
        gs1.update(left=0.03, right=0.98, wspace=0.1, hspace=0.6, bottom=0.05, top=0.93)
  #      plt.suptitle('Sensor response for ' + file[10:-5] + ' meters', fontsize=20)
        raw_plt = plt.subplot(gs1[0])
        raw_plt.grid(color='#c1c1c1', linestyle=':', linewidth=1)
        raw_plt.plot(xBand_raw_time, xBand_raw_data, 'b')

        plt.yticks(np.arange(0, 1.1, 1.0))

        plt.axis([0, duration, 0, 1.1])  # limits can be taken from metadata
        plt.ylabel('Motion status')
        plt.xlabel('Time, s')
        ttl = raw_plt.title
        ttl.set_position([.5, 1.05])
        plt.title('Raw X-Band sensor signal')

        fr_tr_plt = plt.subplot(gs1[1])
        fr_tr_plt.grid(color='#c1c1c1', linestyle=':', linewidth=1)
        fr_tr_plt.plot(fr_trans_graph[0], fr_trans_graph[1], 'b', linewidth=2)
        plt.ylabel('Movement intensity')
        plt.xlabel('Time, s')
        ttl = fr_tr_plt.title
        ttl.set_position([.5, 1.05])
        plt.title('Frequency transformation graph for raw X-Band sensor signal ')

        meanCr = []  # estimation level for mean value
        for i in enumerate(detect_signal[2]):
            meanCr.append(meanlevel)  # from metadata
        stdCr = []  # estimation level for std value
        for i in enumerate(detect_signal[3]):
            stdCr.append(stdlevel)  # from metadata

        detect_plt = plt.subplot(gs1[1, :])
        detect_plt.grid(color='#c1c1c1', linestyle=':', linewidth=1)
        detect_plt.plot(detect_signal[0], detect_signal[2], 'k', linestyle='-', linewidth=2, label="Mean value of the signal")
        detect_plt.plot(detect_signal[0], meanCr, 'k', linestyle='--', linewidth=2, label="Mean value citeria level = " + str(meanlevel) )
        detect_plt.plot(detect_signal[0], detect_signal[3], 'g', linestyle='-', linewidth=2, label="Standard deviation value of the signal")
        detect_plt.plot(detect_signal[0], stdCr, 'g', linestyle='--', linewidth=2, label="Standard deviation criteria level = " + str(stdlevel))

        plt.xticks(np.arange(0, max(detect_signal[0]) + 1, 1.0))

        plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3, ncol=4, mode="expand", borderaxespad=0.)
        plt.ylabel('Relative values')
        plt.xlabel('Time, s')
        ttl = detect_plt.title
        ttl.set_position([.5, 1.2])
        plt.title('Mean and standard deviation values of processed signal')

        for i, element in enumerate(pir2_detect_status):
            if element == 1:
                pir2_detect_status[i] = 0
            else:
                pir2_detect_status[i] = 0.66

        for i, element in enumerate(detect_signal[1]):
            if element == 1:
                detect_signal[1][i] = 0.33
            else:
                detect_signal[1][i] = 0

        pl = plt.subplot(gs1[2, :])
        pl.grid(color='#c1c1c1', linestyle=':', linewidth=1)
        pl.plot(detect_signal[0], detect_signal[1], 'b', linewidth=4, label = "X-Band sensor detection status")
        pl.plot(pir1_detect_time, pir1_detect_status, 'r', linestyle='-', linewidth=4, label = "PIR-1 sensor detection status")
        pl.plot(pir2_detect_time, pir2_detect_status, '#ff9900', linestyle='-', linewidth=4, label = "PIR-2 sensor detection status")
        plt.axis([0, duration, 0, 1.1])  # limits can be taken from metadata
        plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3, ncol=4, mode="expand", borderaxespad=0.)
        plt.yticks(np.arange(0, 1.1, 1.0))
        plt.xticks(np.arange(0, max(detect_signal[0]) + 1, 1.0))

        plt.ylabel('Motion status')
        plt.xlabel('Time, s')
        ttl = pl.title
        ttl.set_position([.5, 1.2])
        plt.title('Movement detection graph for radar sensor')
        '''
        pir1_plt = plt.subplot(gs1[3, :])
        pir1_plt.grid(color='#c1c1c1', linestyle=':', linewidth=1)
        pir1_plt.plot(pir1_detect_time, pir1_detect_status, 'r', linestyle='-', linewidth=4)
        plt.axis([0, duration, 0, 1.1])  # limits can be taken from metadata
        plt.legend(loc='upper left', frameon=False)
        plt.ylabel('Motion status')
        plt.xlabel('Time, s')
        plt.title('Movement detection graph for PIR-1 sensor')


        pir2_plt = plt.subplot(gs1[4, :])
        pir2_plt.grid(color='#c1c1c1', linestyle=':', linewidth=1)
        pir2_plt.plot(pir2_detect_time, pir2_detect_status, '#ff9900', linestyle='-', linewidth=4)
        plt.axis([0, duration, 0, 1.1])  # limits can be taken from metadata
        plt.legend(loc='upper left', frameon=False)
        plt.ylabel('Motion status')
        plt.xlabel('Time, s')
        plt.title('Movement detection graph for PIR-2 sensor')
        '''
   #     plt.savefig(out_path + file[10:-5] + '.png')
#        os.rename(file, out_path + file)
        plt.show()
