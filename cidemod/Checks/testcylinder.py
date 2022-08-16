from Cylinder.cylinder import Cylinder

from cideMOD import (
    CellParser,
    Problem,
    SolverCrashed,
    Trigger,
    ModelOptions,
)

import numpy as np

#Define Chen path
overwrite = True
case = "Chen_2020"
data_path = "Checks/Data/data_{}".format(case)
params = "params_tuned.json"

C_rate = -1
I_app = -1 #C_rate * problem.Q
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