# Loads data generated from performance tests of the different softwares
import numpy as np
import matplotlib.pyplot as plt

cideMOD=np.loadtxt("cidemod/Checks/Data/cideMODTime2.txt")
pybamm=np.loadtxt("pybamm/Data/pybammTime3.txt")
battmo=np.transpose(np.loadtxt("battmo/Data/battmoTime_SD_notsimple.txt"))
petlion=np.loadtxt("petlion/Kode/petlionTime.txt")
petlion2=np.loadtxt("petlion/Kode/petlionTime2.txt")

plt.rc('text', usetex=False)
plt.rc('font', family='serif')
# fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 4))
fig, ax1 = plt.subplots(1, 1, figsize=(5.5, 4), dpi=200)
# plot thime over problem size
ax1.semilogy(cideMOD[1],cideMOD[0], ">")
ax1.semilogy(pybamm[1], pybamm[0],"v")
ax1.semilogy(battmo[1], battmo[0],"^")
ax1.semilogy(petlion[0]*3,petlion[1],"<")
ax1.semilogy(petlion[0]*3,petlion[2],"<")
ax1.semilogy(petlion2[0]*3,petlion2[1],"<")
ax1.semilogy(petlion2[0]*3,petlion2[2],"<")
ax1.set_xlabel("Problem size")
ax1.set_ylabel("Time [s]")
ax1.legend(["cideMOD", "PyBaMM","BattMo","Petlion: AD, 1st run", "Petlion: AD, 2nd run", "Petlion: Symbolic, 1st run", "Petlion: Symbolic, 2nd run"], loc="best")

plt.rc('text', usetex=False)
plt.rc('font', family='serif')
# fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 4))
fig, ax1 = plt.subplots(1, 1, figsize=(5.5, 4), dpi=200)
# plot thime over problem size
ax1.plot(cideMOD[1],cideMOD[0], ">")
ax1.plot(pybamm[1], pybamm[0],"v")
ax1.plot(battmo[1], battmo[0],"^")
ax1.set_xlabel("Problem size")
ax1.set_ylabel("Time [s]")
ax1.legend(["cideMOD", "PyBaMM","BattMo"], loc="best")

plt.tight_layout()
plt.show()
