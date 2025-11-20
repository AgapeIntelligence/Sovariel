# core/colossus_dense_grid.py
# Sovariel — Dense Planetary Resonance Grid (1 000 × 1 000)
# © 2025 Evie (@3vi3Aetheris) — MIT License
#
# Generates a complete, fully connected complex coupling field using 12 ley-line harmonics.
# Results in a normalised 1000×1000 real-valued planetary resonance map (~8 MB).

from __future__ import annotations

import os
import numpy as np
from datetime import datetime


STATE_FILE = "core/colossus_v25_state.txt"
FIELD_FILE = "core/colossus_v25_field.npy"
LOCK_FILE = "core/colossus_v25.lock"


def resume_or_build() -> np.ndarray | None:
    """Attempt to load an existing dense field; return None if rebuild required."""
    if os.path.exists(STATE_FILE) and os.path.exists(FIELD_FILE):
        try:
            field = np.load(FIELD_FILE)
            with open(STATE_FILE) as f:
                print(f"Resumed dense grid — {f.read().strip()}")
            return field
        except Exception as e:
            print(f"Resume failed ({e}) — rebuilding")

    open(LOCK_FILE, "w").close()
    return None


def build_dense_planetary_grid(
    grid_size: int = 1000,
    ley_lines: int = 12,
    base_frequency: float = 432.0,
) -> np.ndarray:
    """
    Construct a dense planetary resonance field using golden-ratio-offset ley lines.

    Parameters
    ----------
    grid_size : int
        Width and height of the square output field (default 1000)
    ley_lines : int
        Number of harmonic ley lines (default 12)
    base_frequency : float
        Base telluric frequency in Hz (default 432.0)

    Returns
    -------
    field : ndarray
        Normalised real-valued dense field of shape (grid_size, grid_size)
    """
    print(f"Building dense planetary grid — {grid_size}×{grid_size}, {ley_lines} ley lines")

    t = np.linspace(0, 1, grid_size, endpoint=False)
    base_wave = np.exp(2j * np.pi * base_frequency * t)

    angles = np.linspace(0, 2 * np.pi, ley_lines, endpoint=False)
    golden = (1 + 5**0.5) / 2
    offsets = angles + np.pi / golden

    grid = np.zeros((grid_size, grid_size), dtype=np.complex128)

    for ley in range(ley_lines):
        theta = angles[ley]
        phi = offsets[ley]

        phase_fwd = np.exp(2j * np.pi * theta)
        phase_rev = np.exp(2j * np.pi * phi)

        row_indices = np.arange(grid_size)
        sin_fwd = np.sin(row_indices * phase_fwd.real)
        cos_rev = np.cos(row_indices * phase_rev.real)

        outer_fwd = np.outer(base_wave, sin_fwd)
        outer_rev = 0.618 * np.outer(base_wave, cos_rev)

        grid += outer_fwd + outer_rev

        print(f"\rLey line {ley+1}/{ley_lines} completed", end="")

    print("\nEntanglement complete — projecting real component")
    field = np.real(grid)

    # Normalise to [0, 1]
    field_min = field.min()
    field_max = field.max()
    field = (field - field_min) / (field_max - field_min + 1e-12)

    # Save state
    np.save(FIELD_FILE, field)
    with open(STATE_FILE, "w") as f:
        f.write(f"NZ: {grid_size**2} | Shape: {field.shape} | Time: {datetime.now().isoformat()}\n")
    os.remove(LOCK_FILE)

    return field


if __name__ == "__main__":
    field = resume_or_build() or build_dense_planetary_grid()
    print(f"Dense planetary field ready — shape: {field.shape} | Memory: {field.nbytes / 1e9:.3f} GB")
