from cideMOD import (
    CellParser,
    ErrorCheck,
    NDProblem,
    Problem,
    SolverCrashed,
    Trigger,
    init_results_folder,
    ModelOptions,
)

import os

#Path til Chen data
overwrite = True
case = "Chen_2020"
data_path = "/home/andreas/Documents/SINTEF_code_review/cideMOD_review/Data/data_{}".format(case)
params = "params_tuned.json"

#Lagrer mappe med Chen referanse-data
save_path = init_results_folder(
    case, overwrite=overwrite, copy_files=[f"{data_path}/{params}"]
)

#P2D modell
model_options = ModelOptions(mode='P2D', clean_on_exit=False)

cell = CellParser(params, data_path=data_path)
problem = Problem(cell, model_options, save_path=save_path)
#Set SOC, Text, Tint
problem.set_cell_state(1, 273 + 25, 273 + 25)
problem.setup()
C_rate = -1
I_app = -5 #C_rate * problem.Q
t_f = 3600 /abs(C_rate)*1.25

v_min = Trigger(2.5, "v")
#Solve
status = problem.solve_ie(
    min_step=5, i_app=I_app, t_f=t_f, store_delay=10, adaptive=True, triggers=[v_min]
)
err = ErrorCheck(problem, status)

if isinstance(status, SolverCrashed):
    raise status.args[0]

import numpy
import matplotlib.pyplot as plt
plt.rc('text', usetex=False)
plt.rc('font', family='serif')
# fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 4))
fig, ax1 = plt.subplots(1, 1, figsize=(5.5, 4), dpi=200)

# plot the 1C results over time
ax1.plot(problem.WH.global_var_arrays[0], problem.WH.global_var_arrays[1], "-.")
ax1.set_xlabel("Time [s]")
ax1.set_ylabel("Voltage [V]")
ax1.legend(["cideMOD"], loc="best")

plt.tight_layout()
plt.show()