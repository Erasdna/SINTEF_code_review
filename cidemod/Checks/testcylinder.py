from Cylinder.cylinder import Cylinder

from cideMOD import (
    CellParser,
    Problem,
    SolverCrashed,
    Trigger,
    ModelOptions,
)

import numpy as np
import matplotlib.pyplot as plt

#Define Chen path
overwrite = True
case = "Chen_2020"
data_path = "Checks/Data/data_{}".format(case)
params = "params_tuned.json"

C_rate = -1
I_app = -5 #C_rate * problem.Q
t_f = 3600 /abs(C_rate)*1.25
v_min = Trigger(2.5, "v")
#P4D modell
#Vi setter i=5 for å se om vi får noe nyttig
i=6
model_options = ModelOptions(mode='P4D', clean_on_exit=False,N_x=i,N_y=i,N_z=i)
cell = CellParser(params, data_path=data_path)

# #Checking that the class correctly builds the mesh
# cyll=Cylinder(model_options,cell)
# cyll.build_mesh()
# E=[cyll.electrolyte, cyll.electrolyte,]
# b=3
# #Defining a problem with the cylindrical mesh
problem= Problem(cell, model_options)
problem.set_cell_state(1, 273 + 25, 273 + 25)
problem.setup(mesh_engine="Cylinder") #OBS Cylinder reads thr cylinder_3.xml file in the LOCAL repo

status = problem.solve_ie(
    min_step=36, i_app=I_app, t_f=t_f, store_delay=10, adaptive=True, triggers=[v_min]
)

plt.rc('text', usetex=False)
plt.rc('font', family='serif')
# fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 4))
fig, ax1 = plt.subplots(1, 1, figsize=(5.5, 4), dpi=200)
# plot voltage vs tid
ax1.plot(problem.WH.global_var_arrays[0], problem.WH.global_var_arrays[1], "-.")
ax1.set_xlabel("Time")
ax1.set_ylabel("Voltage")
ax1.legend(["P4D"], loc="best")

np.savetxt("Cylinder_Chen.txt",(problem.WH.global_var_arrays[0], problem.WH.global_var_arrays[1]))