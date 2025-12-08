from qutip import mesolve, basis, sigmaz, Qobj
import numpy as np

def apply_stochastic_resonance(n_oscillators=3, noise_strength=0.12, duration=20.0):
    def hamiltonian(t, args):
        H0 = Qobj(np.diag(np.arange(n_oscillators)))
        drive = noise_strength * np.sin(3.69 * t)
        return [H0, [sigmaz(), drive]]

    times = np.linspace(0, duration, 400)
    result = mesolve(hamiltonian, basis(2, 0), times, [], [])
    phases = np.angle(np.diag(result.states[-1].full()))
    R = np.abs(np.mean(np.exp(1j * phases)))
    return R
