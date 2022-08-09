println("Starting")

using PETLION, Plots, DelimitedFiles

N=10:10:50;

tm=[];
tm2=[];
println("Hello")
for i in N
    p = petlion(LCO, N_p = i, N_s = i, N_n = i, N_r_p = 20, N_r_n = 20, temperature = false, jacobian = :AD)
    @info i
    t1 = @elapsed simulate(p, I=-1, SOC=1);
    append!(tm,t1);
    t2 = @elapsed simulate(p, I=-1, SOC=1);
    append!(tm2,t2);
end

open("petlionTime.txt","w");
writedlm("petlionTime.txt",[N,tm,tm2]);


