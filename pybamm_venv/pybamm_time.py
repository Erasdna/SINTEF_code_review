import pybamm
import numpy as np
import time as tm
import matplotlib.pyplot as plt

parameter_values = pybamm.ParameterValues(chemistry=pybamm.parameter_sets.Chen2020)
model = pybamm.lithium_ion.DFN()
print(type(pybamm.standard_spatial_vars.x_n))

N=np.array([20,30,40,50])
Tt=np.empty([0,0])  

for i in N:
    var_pts = {
        pybamm.standard_spatial_vars.x_n: i,  # negative electrode
        pybamm.standard_spatial_vars.x_s: i,  # separator 
        pybamm.standard_spatial_vars.x_p: i,  # positive electrode
        pybamm.standard_spatial_vars.r_n: i,  # negative particle
        pybamm.standard_spatial_vars.r_p: i,  # positive particle
    }   
    sim = pybamm.Simulation(
        model, parameter_values=parameter_values, var_pts=var_pts
    )
    strt=tm.time()
    sim.solve([0,3600])
    Tt=np.append(Tt,tm.time()-strt)

plt.rc('text', usetex=False)
plt.rc('font', family='serif')
# fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 4))
fig, ax1 = plt.subplots(1, 1, figsize=(5.5, 4), dpi=200)
# plot time over problem size
ax1.plot(3*N, Tt, "-.")
ax1.set_xlabel("Problem size")
ax1.set_ylabel("Time [s]")
ax1.legend(["PyBaMM"], loc="best")

plt.tight_layout()
plt.show()