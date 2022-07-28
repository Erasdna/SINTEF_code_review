a=5
for i=1:5
    b=i
end

param{1} = Parameters_init;
t0=0;
tf=3600;
out = startSimulation(t0,tf,[],-30, param);