import numpy as np
import matplotlib.pyplot as plt

cideMOD=np.loadtxt("cidemod/cideMODTime2.txt")
pybamm=np.loadtxt("pybamm/PyBaMM/Kode/pybammTime.txt")
battmo=np.transpose(np.loadtxt("battmo/battmoTime_SD_notsimple.txt"))
petlion=np.loadtxt("PETLION_review/petlionTime.txt")

plt.rc('text', usetex=False)
plt.rc('font', family='serif')
# fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 4))
fig, ax1 = plt.subplots(1, 1, figsize=(5.5, 4), dpi=200)
# plot thime over problem size
ax1.plot(cideMOD[1],cideMOD[0], ">")
ax1.plot(pybamm[1], pybamm[0],"v")
ax1.plot(battmo[1], battmo[0],"^")
ax1.plot(petlion[0]*3,petlion[1],"<")
ax1.plot(petlion[0]*3,petlion[2],"<")
ax1.set_xlabel("Problem size")
ax1.set_ylabel("Time [s]")
ax1.legend(["cideMOD", "PyBaMM","BattMo","Petlion, 1st run", "Petlion, 2nd run"], loc="best")

plt.tight_layout()
plt.show()
