using PETLION, Plots
p = petlion(LCO)
##
sol = simulate(p, I=-1, SOC=1)
##
#simulate!(sol, p, 1800, V=:hold, I_min=1/20)
plot(sol.t, sol.V;  label="PETLION", xlabel="Time (s)", ylabel="Voltage (V)", legend=:topright)
