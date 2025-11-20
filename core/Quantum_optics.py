# quantum_optics.py
from qutip import *

N_osc = 100
a = destroy(N_osc)
H = a.dag() * a
psi0 = coherent(N_osc, 5.0)

kappa = 0.1
c_ops = [np.sqrt(kappa) * a]

times = np.linspace(0, 50, 500)
result = mesolve(H, psi0, times, c_ops, [a.dag() * a, a + a.dag()])

plot_expectation_values(result)
