import matplotlib
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
matplotlib.rcParams.update({"figure.figsize": (10.0, 1.5)})
import numpy as np

id_mot_time = np.linspace(0,30,5000)
id_mot_status1 = [0] * 5000
for i, element in enumerate(id_mot_time):
    if element > 5 and element < 15:
        id_mot_status1[i] = 1
    if element > 20 and element < 30:
        id_mot_status1[i] = 1


gs1 = GridSpec(1, 1)
gs1.update(left=0.04, right=0.98, wspace=0.1, hspace=0.6, bottom=0.3, top=0.85)


pl = plt.subplot(gs1[0])
pl.plot(id_mot_time, id_mot_status1, '#984300', linewidth=4)
plt.fill_between(id_mot_time, id_mot_status1, color='#984300', hatch='/', alpha='0.5')
pl.text(8.5, 0.4, 'Motion', color='w', fontsize=20, style='oblique')
pl.text(23.5, 0.4, 'Motion', color='w', fontsize=20, style='oblique')
plt.axis([0, 30, 0, 1.1])  # limits can be taken from metadata
plt.yticks(np.arange(0, 1.1, 1.0))
plt.ylabel('Motion status')
plt.xlabel('Time, s')
plt.title('Experiment timetable')

plt.show()