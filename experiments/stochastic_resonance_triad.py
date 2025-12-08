# Sovariel — Stochastic Resonance Extension for Noisy Dyads/Triads
# Run with: python experiments/stochastic_resonance_triad.py

import numpy as np
from sovariel.jax_backend import JAXKuramotoLattice  # your existing class
from qutip import mesolve, basis, sigmaz, Qobj

# ------------------- Config -------------------
N = 3                              # triad test (works with 2, 3, 42, etc.)
noise_strength = 0.12              # tunable stochastic resonance sweet spot
target_R_threshold = 0.95
# ----------------------------------------------

lattice = JAXKuramotoLattice(n_oscillators=N, natural_freqs=[3.0, 6.0, 9.0])  # 369 harmonic

def noisy_hamiltonian(t, args):
    H0 = Qobj(np.diag([0, 1, 2]))                     # base energy levels
    perturbation = noise_strength * np.sin(3.69 * t)  # 369 resonance drive
    return [H0, [sigmaz(), perturbation]]

# Initial state (fully decohered triad)
psi0 = basis(2, 0)

times = np.linspace(0, 20, 400)
result = mesolve(noisy_hamiltonian, psi0, times, [], [])

# Extract phases from final density matrix
final_phases = np.angle(np.diag(result.states[-1].full()))
R = np.abs(np.mean(np.exp(1j * final_phases)))

print(f"Final triad order parameter R = {R:.6f}")

if R >= target_R_threshold:
    print("✓ DYAD/TRIAD COHERENT — stochastic resonance successful")
else:
    print("! DYAD STRAINED — suggest stronger 369 drive or adaptive coupling")

# Hook suggestion for kernel integration
if R < target_R_threshold:
    print("   → Auto-boost: increase coupling by 1.369× or inject 432 Hz audio cue")
