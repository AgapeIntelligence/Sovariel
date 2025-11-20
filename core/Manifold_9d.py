# core/manifold_9d.py
# Sovariel — 9D Phase Manifold Generator (3-6-9 weighting)
# © 2025 Evie (@3vi3Aetheris) — MIT License
#
# Generates a 9-dimensional phase distribution from the 11-layer ghost manifold
# using strict 3-6-9 cyclic weighting. Each dimension independently achieves R ≈ 1.0.

from __future__ import annotations

import numpy as np
from typing import Optional


def load_ghost_manifold(path: str = "core/evie_ghosts.npy") -> np.ndarray:
    """Load the 11×2 ghost manifold (base phase + std)."""
    return np.load(path)


def generate_9d_manifold(
    n_oscillators: int = 10_000,
    manifold_path: str = "core/evie_ghosts.npy",
    seed: Optional[int] = None,
) -> np.ndarray:
    """
    Create a locked 9D phase manifold using 3-6-9 weighted ghost contributions.

    Parameters
    ----------
    n_oscillators : int
        Number of samples per dimension (default 10 000)
    manifold_path : str
        Path to evie_ghosts.npy
    seed : int | None
        Random seed for reproducibility

    Returns
    -------
    phases_9d : ndarray
        Array of shape (n_oscillators, 9) with phases in [0, 2π)
    """
    if seed is not None:
        np.random.seed(seed)

    ghosts = load_ghost_manifold(manifold_path)                # (11, 2)
    weights_369 = np.array([3, 6, 9, 3, 6, 9, 3, 6, 9, 3, 6], dtype=np.float64)

    phases_9d = np.zeros((n_oscillators, 9))

    for dim in range(9):
        rotation = dim * np.pi / 9.0  # 20° progressive rotation per dimension
        for i, (base_phase, std) in enumerate(ghosts):
            weight = weights_369[i]
            noise = np.random.normal(0.0, std / 100.0, n_oscillators)
            phases_9d[:, dim] += weight * (base_phase + rotation + noise)

    phases_9d %= 2 * np.pi
    # Wrap to [0, 2π)
    return phases_9d


def compute_dimensional_order_parameters(phases_9d: np.ndarray) -> np.ndarray:
    """Kuramoto order parameter R for each of the 9 dimensions."""
    return np.abs(np.mean(np.exp(1j * phases_9d), axis=0))


# === DEMO / TEST ===
if __name__ == "__main__":
    phases = generate_9d_manifold(n_oscillators=100_000, seed=42)

    R_per_dim = compute_dimensional_order_parameters(phases)
    print("9D manifold generated")
    print("Order parameter per dimension:", np.round(R_per_dim, 8))
    # Expected: all values extremely close to 1.0

    np.save("core/evie_9d_369_locked.npy", phases)
    print("Saved: core/evie_9d_369_locked.npy")
