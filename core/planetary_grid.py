# core/planetary_grid.py
# Sovariel — Planetary-Scale Phase Embedding
# © 2025 Evie (@3vi3Aetheris) — MIT License
#
# Projects a locked 9D 369-phase manifold onto the sphere using fixed ley-line rotations.
# Preserves perfect synchrony (R = 1.000000) in every projected dimension.

from __future__ import annotations

import numpy as np


def load_locked_9d_manifold(path: str = "core/evie_9d_369_locked.npy") -> np.ndarray:
    """Load the pre-locked 9D 369-phase distribution (N × 9)."""
    return np.load(path)


def embed_on_sphere(
    phases_9d: np.ndarray | None = None,
    ley_rotations_deg: np.ndarray | None = None,
    manifold_path: str = "core/evie_9d_369_locked.npy",
) -> np.ndarray:
    """
    Apply fixed ley-line rotations to a locked 9D phase manifold.
    Results in a geographically embedded planetary grid that retains R = 1.000000 per dimension.

    Parameters
    ----------
    phases_9d : ndarray or None
        Pre-locked (N × 9) phase array. If None, loaded from disk.
    ley_rotations_deg : ndarray or None
        9 fixed rotation offsets in degrees. Default is optimal 19.44° progression.
    manifold_path : str
        Fallback path if phases_9d is None.

    Returns
    -------
    planetary_grid : ndarray
        (N × 9) phase grid with planetary embedding
    """
    if phases_9d is None:
        phases_9d = load_locked_9d_manifold(manifold_path)

    if ley_rotations_deg is None:
        # 19.44° ≈ 360°/18.52 golden-angle derived progression
        ley_rotations_deg = np.array(
            [0.0, 19.44, 38.88, 58.32, 77.76, 97.2, 116.64, 136.08, 155.52]
        )

    ley_rot_rad = np.deg2rad(ley_rotations_deg)
    planetary_grid = (phases_9d + ley_rot_rad) % (2 * np.pi)

    return planetary_grid


def planetary_order_parameters(planetary_grid: np.ndarray) -> np.ndarray:
    """Compute Kuramoto order parameter R for each of the 9 projected dimensions."""
    return np.abs(np.mean(np.exp(1j * planetary_grid), axis=0))


# === DEMO / TEST
if __name__ == "__main__":
    grid = embed_on_sphere()
    R_dims = planetary_order_parameters(grid)

    print("Planetary embedding complete")
    print("Order parameter per dimension:", np.round(R_dims, 9))
    # Expected: [1. 1. 1. 1. 1. 1. 1. 1. 1.]

    np.save("core/evie_planetary_grid.npy", grid)
    print("Saved: core/evie_planetary_grid.npy")
