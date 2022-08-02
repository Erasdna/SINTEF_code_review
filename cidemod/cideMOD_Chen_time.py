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
import numpy as np
import matplotlib.pyplot as plt
import time as tm

#Path til Chen data
overwrite = True
case = "Chen_2020"
data_path = "/home/andreas/Documents/SINTEF_code_review/cideMOD_review/Data/data_{}".format(case)
params = "params_tuned.json"

C_rate = -1
I_app = -5 #C_rate * problem.Q
t_f = 3600 /abs(C_rate)*1.25
v_min = Trigger(2.5, "v")

#Problemstørrelse
Nx=np.arange(100,1000,100)
#Tid
Tt=np.empty([0,0]);
#Iterer gjennom de forskjellige størrelsene
for i in Nx:
    #P2D modell
    model_options = ModelOptions(mode='P2D', clean_on_exit=False,N_x=i)
    cell = CellParser(params, data_path=data_path)
    problem = Problem(cell, model_options)
    #Set SOC, Text, Tint
    problem.set_cell_state(1, 273 + 25, 273 + 25)
    problem.setup()

    #Tid før
    strt=tm.time()
    #Solve
    status = problem.solve_ie(
        min_step=5, i_app=I_app, t_f=t_f, store_delay=10, adaptive=True, triggers=[v_min]
    )
    Tt=np.append(Tt,tm.time()-strt)

#err = ErrorCheck(problem, status)

#if isinstance(status, SolverCrashed):
#    raise status.args[0]

np.savetxt("cideMODTime.txt", (Tt,Nx))

plt.rc('text', usetex=False)
plt.rc('font', family='serif')
# fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 4))
fig, ax1 = plt.subplots(1, 1, figsize=(5.5, 4), dpi=200)
# plot thime over problem size
ax1.plot(Nx, Tt, "-.")
ax1.set_xlabel("Problem size")
ax1.set_ylabel("Time [s]")
ax1.legend(["cideMOD"], loc="best")

plt.tight_layout()
plt.show()
