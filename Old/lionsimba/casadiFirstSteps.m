addpath("/home/andreas/casadi-linux-matlabR2014b-v3.5.5");
import casadi.*

x = MX.sym('x')
disp(jacobian(sin(x),x))