import pybamm
import numpy as np
import matplotlib.pyplot as plt
import time as tm

N=np.arange(10,400,50)
Tt=np.zeros([7,8])
Tt2=np.zeros([7,8])

##OBS! This is not correct!!!
solvers=[
    pybamm.CasadiSolver(mode="fast"), 
    #pybamm.IDAKLUSolver,
    #pybamm.JaxSolver,
    #pybamm.AlgebraicSolver,
    #pybamm.ScikitsOdeSolver,
    #pybamm.ScikitsDaeSolver,
    pybamm.BaseSolver
]

parameter_values = pybamm.ParameterValues(chemistry=pybamm.parameter_sets.Chen2020)
model = pybamm.lithium_ion.DFN()

for j in range(len(solvers)):
    print(solvers[j])
    for i in range(len(N)):
        print(N[i])
        var_pts = {
            "x_n": N[i],  # negative electrode
            "x_s": N[i],  # separator 
            "x_p": N[i],  # positive electrode
            "r_n": 20,  # negative particle
            "r_p": 20,  # positive particle 
        } 
        
        sim = pybamm.Simulation(
            model, parameter_values=parameter_values, var_pts=var_pts
        )
        #res=sim.solve([0,3600], solver=solvers[j])
        res=solvers[j].solve(model, [0,3600])
        print(res.solve_time)
        Tt[j,i]=res.solve_time.value

        sim = pybamm.Simulation(
            model, parameter_values=parameter_values, var_pts=var_pts
        )
        #res=sim.solve([0,3600], solver=solvers[j])
        res=solvers[j].solve(model, [0,3600])

        Tt2[j,i]=res.solve_time.value

np.savetxt("..Data/SolverTime2.txt",Tt)

plt.rc('text', usetex=False)
plt.rc('font', family='serif')
# fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 4))
fig, ax1 = plt.subplots(1, 1, figsize=(5.5, 4), dpi=200)
# plot thime over problem size
for i in range(len(solvers)):
    ax1.scatter(N*3,Tt[i])
ax1.set_xlabel("Problem size")
ax1.set_ylabel("Time [s]")
ax1.legend(["Casadi - fast", "IDAKLU","Jax", "Algebraic","Scikit ODE", "Scikit DAE","Base"], loc="best")
plt.tight_layout()
plt.show()

plt.rc('text', usetex=False)
plt.rc('font', family='serif')
# fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 4))
fig, ax2 = plt.subplots(1, 1, figsize=(5.5, 4), dpi=200)
# plot thime over problem size
for i in range(len(solvers)):
    ax2.scatter(N*3,Tt[i]-Tt[0])
ax2.set_xlabel("Problem size")
ax2.set_ylabel("Time [s]")
ax2.legend(["Casadi - fast", "IDAKLU","Jax", "Algebraic","Scikit ODE", "Scikit DAE","Base"], loc="best")

plt.tight_layout()
plt.show()

plt.rc('text', usetex=False)
plt.rc('font', family='serif')
# fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 4))
fig, ax3 = plt.subplots(1, 1, figsize=(5.5, 4), dpi=200)
# plot thime over problem size
for i in range(len(solvers)):
    ax3.scatter(N*3,Tt2[i])
ax3.set_xlabel("Problem size")
ax3.set_ylabel("Time [s]")
ax3.legend(["Casadi - fast", "IDAKLU","Jax", "Algebraic","Scikit ODE", "Scikit DAE","Base"], loc="best")
plt.tight_layout()
plt.show()
