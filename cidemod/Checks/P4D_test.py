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
data_path = "/home/andreas/Documents/SINTEF_code_review/cidemod/cideMOD/data/data_{}".format(case)
params = "params_tuned.json"

C_rate = -1
I_app = -5 #C_rate * problem.Q
t_f = 3600 /abs(C_rate)*1.25
v_min = Trigger(2.5, "v")
#P2D modell
i=5
model_options = ModelOptions(mode='P4D', clean_on_exit=False,N_x=i,N_y=i,N_z=i)
cell = CellParser(params, data_path=data_path)
problem = Problem(cell, model_options)
#Set SOC, Text, Tint
problem.set_cell_state(1, 273 + 25, 273 + 25)
problem.setup()
status = problem.solve_ie(
    min_step=36, i_app=I_app, t_f=t_f, store_delay=10, adaptive=True, triggers=[v_min]
)

print(problem.WH.global_vars.keys())