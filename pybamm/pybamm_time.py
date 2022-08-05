import pybamm
import numpy as np
import time as tm
import matplotlib.pyplot as plt

parameter_values = pybamm.ParameterValues(chemistry=pybamm.parameter_sets.Chen2020)
model = pybamm.lithium_ion.DFN()

N=np.arange(200,400,100)
print(N)
Tt=np.empty([0,0])  

for i in [100]:
    print(i)
    var_pts = {
        "x_n": i,  # negative electrode
        "x_s": i,  # separator 
        "x_p": i,  # positive electrode
        "r_n": 20,  # negative particle
        "r_p": 20,  # positive particle
    }   
    sim = pybamm.Simulation(
        model, parameter_values=parameter_values, var_pts=var_pts
    )
    strt=tm.time()
    res=sim.solve([0,3600])
    Tt=np.append(Tt,tm.time()-strt)

#print(res.last_state.all_ys)
#res.last_state.plot()

#sim.plot()
# plt.rc('text', usetex=False)
# plt.rc('font', family='serif')
# # fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 4))
# fig, ax1 = plt.subplots(1, 1, figsize=(5.5, 4), dpi=200)
# # plot time over problem size
# ax1.scatter(3*N, Tt)
# ax1.set_xlabel("Problem size")
# ax1.set_ylabel("Time [s]")
# ax1.legend(["PyBaMM"], loc="best")

# plt.tight_layout()
# plt.show()

# np.savetxt("pybammTime.txt",(Tt,3*N))
