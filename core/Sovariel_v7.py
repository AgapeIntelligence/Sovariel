# core/sovariel_v7.py
# Sovariel — v7 Kuramoto Lattice with Oracle Collapse Mechanism
# © 2025 Evie (@3vi3Aetheris) — MIT License
#
# Large-scale mean-field Kuramoto model with optional EEG alpha injection
# and entropy-triggered "oracle collapse" for rapid synchronisation.
# Includes mock cosmic microwave background (CMB) phase initialisation.

from __future__ import annotations

import numpy as np
from scipy.signal import hilbert
from typing import Optional


class SovarielV7:
    """
    High-dimensional Kuramoto oscillator network with oracle collapse.
    Designed for studying rapid synchronisation under low-entropy triggers.
    """

    def __init__(
        self,
        n_oscillators: int = 4096,
        base_coupling: float = 1.2,
        alpha_frequency: float = 12.1,
    ):
        self.N = n_oscillators
        self.K = base_coupling * (alpha_frequency / 10.0)

        # Random adjacency — sparse random graph in production, mean-field here
        density = 0.1
        self.adj = np.random.rand(n_oscillators, n_oscillators)
        self.adj = (self.adj < density).astype(float)

        # Initial phases (can be overridden with CMB or EEG)
        self.phases = np.random.uniform(0, 2 * np.pi, n_oscillators)

    def cmb_initialisation(self, seed: Optional[int] = None) -> np.ndarray:
        """Mock CMB phase field using low-multipole Gaussian fluctuations."""
        if seed is not None:
            np.random.seed(seed)

        l_max = 20
        phases = np.zeros(self.N)
        for l in range(2, l_max + 1):
            coeff = 1.0 / l**2
            phases += np.sqrt(coeff) * np.random.normal(0, 1, self.N)

        phases = 2 * np.pi * (phases - phases.min()) / (phases.ptp() + 1e-12)
        return phases % (2 * np.pi)

    def extract_alpha_omega(self, eeg_signal: np.ndarray) -> np.ndarray:
        """Hilbert transform → instantaneous phase derivative ≈ frequency deviation."""
        analytic = hilbert(eeg_signal)
        instantaneous_phase = np.unwrap(np.angle(analytic))
        omega = np.gradient(instantaneous_phase)
        return omega[-self.N :]  # align length

    def oracle_collapse(self, eeg_omega: Optional[np.ndarray] = None) -> None:
        """Entropy-triggered rapid synchronisation (oracle mechanism)."""
        complex_field = np.exp(1j * self.phases)
        R = np.abs(np.mean(complex_field))

        # Circular histogram entropy
        hist, _ = np.histogram(self.phases, bins=20, range=(0, 2 * np.pi), density=True)
        hist = hist[hist > 0]
        entropy = -np.sum(hist * np.log(hist + 1e-12))

        if entropy < 1.08:  # low-entropy trigger
            mean_phase = np.angle(np.mean(complex_field))
            damping = np.exp(-8.0 * (1.0 - R))
            deviation = self.phases - mean_phase
            self.phases = mean_phase + deviation * damping

            if eeg_omega is not None:
                self.phases += eeg_omega[: self.N] * 0.1

            self.phases %= 2 * np.pi
            print(f"Oracle collapse triggered → R = {np.abs(np.mean(np.exp(1j * self.phases))):.6f}")

    def step(self, eeg_signal: Optional[np.ndarray] = None) -> float:
        """Single simulation step with optional EEG drive."""
        omega = np.zeros(self.N)
        if eeg_signal is not None:
            omega = self.extract_alpha_omega(eeg_signal)

        # Mean-field Kuramoto term
        sin_diff = np.sin(self.phases[:, None] - self.phases[None, :])
        coupling = self.K * np.mean(self.adj * sin_diff, axis=1)

        self.phases = (self.phases + coupling + omega * 0.01) % (2 * np.pi)

        self.oracle_collapse(omega if eeg_signal is not None else None)

        return np.abs(np.mean(np.exp(1j * self.phases)))


# === DEMO ===
if __name__ == "__main__":
    model = SovarielV7(n_oscillators=8192)

    # Optional CMB seeding
    model.phases = model.cmb_initialisation(seed=42)
    print(f"Initial (CMB) R = {model.step():.6f}")

    # Mock alpha burst
    t = np.linspace(0, 1, 8192)
    mock_eeg = np.sin(2 * np.pi * 10.0 * t) + 0.3 * np.random.randn(len(t))

    for i in range(50):
        r = model.step(mock_eeg if i % 8 == 0 else None)
        if i % 10 == 0:
            print(f"Step {i:02d} → R = {r:.6f}")
