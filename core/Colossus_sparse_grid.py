# core/colossus_sparse_grid.py
# Sovariel — Sparse Planetary Resonance Grid (144 000 nodes)
# © 2025 Evie (@3vi3Aetheris) — MIT License
#
# Generates a sparse, ley-line-structured complex coupling field.
# Memory-efficient (< 50 MB), resumable, down-sampled to 2250×2250 dense map.

from __future__ import annotations

import os
import time
import numpy as np
from datetime import datetime
from typing import Dict, Tuple


STATE_FILE = "core/colossus_v22_state.txt"
FIELD_FILE = "core/colossus_v22_field.npy"
LOCK_FILE = "core/colossus_v22.lock"


def resume_or_build() -> np.ndarray:
    """Load existing dense field or return None if rebuild needed."""
    if os.path.exists(STATE_FILE) and os.path.exists(FIELD_FILE):
        try:
            field = np.load(FIELD_FILE)
            with open(STATE_FILE) as f:
                print(f"Resumed sparse grid — {f.read().strip()}")
            return field
        except Exception as e:
            print(f"Resume failed ({e}) — rebuilding")
            os.makedirs("core", exist_ok=True)

    open(LOCK_FILE, "w").close()


def build_sparse_planetary_grid(
    nodes: int = 144_000,
    ley_lines: int = 12,
    frequency: float = 432.0,
    downsample: int = 64,
    tolerance: float = 1.5,
) -> np.ndarray:
    """Build sparse complex field and return down-sampled real dense map."""
    print(f"Building sparse planetary grid — {nodes:,} nodes, {ley_lines} ley lines")

    sparse: Dict[Tuple[int, int], complex] = {}
    chunk_size = 256
    golden = (1 + 5**0.5) / 2

    t = np.linspace(0, 1, nodes, endpoint=False)
    base_wave = np.exp(2j * np.pi * frequency * t)

    angles = np.linspace(0, 2 * np.pi, ley_lines, endpoint=False)
    offsets = angles + np.pi / golden

    start_time = time.time()
    processed = 0

    for chunk_start in range(0, nodes, chunk_size):
        chunk_end = min(chunk_start + chunk_size, nodes)
        local_t = t[chunk_start:chunk_end]
        local_wave = base_wave[chunk_start:chunk_end]

        for ley in range(ley_lines):
            fwd_phase = np.exp(2j * np.pi * angles[ley])
            rev_phase = np.exp(2j * np.pi * offsets[ley])

            sin_fwd = np.sin(np.arange(chunk_start, chunk_end) * fwd_phase.real)
            cos_rev = np.cos(np.arange(chunk_start, chunk_end) * rev_phase.real)

            outer_fwd = np.outer(local_wave, sin_fwd)
            outer_rev = 0.618 * np.outer(local_wave, cos_rev)
            outer = outer_fwd + outer_rev

            i_idx, j_idx = np.where(np.abs(outer) > tolerance)
            for ii, jj in zip(i_idx, j_idx):
                i = chunk_start + ii
                j = chunk_start + jj
                i_ds = i // downsample
                j_ds = j // downsample
                key = (i_ds, j_ds)
                sparse[key] = sparse.get(key, 0j) + outer[ii, jj]
                processed += 1

        print(f"\rProgress: {chunk_start/nodes:.1%} | Unique NZ: {len(sparse):,}", end="")

    print(f"\nBuild complete — {len(sparse):,} unique non-zero entries")

    # Convert to dense down-sampled field
    rows, cols = zip(*sparse.keys())
    h = max(rows) - min(rows) + 1
    w = max(cols) - min(cols) + 1
    dense = np.zeros((h, w), dtype=np.float64)

    for (i, j), val in sparse.items():
        dense[i - min(rows), j - min(cols)] = val.real

    dense = (dense - dense.min()) / (dense.max() - dense.min() + 1e-12)

    # Save state
    np.save(FIELD_FILE, dense)
    with open(STATE_FILE, "w") as f:
        f.write(f"NZ: {len(sparse)} | Shape: {dense.shape} | Time: {datetime.now().isoformat()}\n")
    os.remove(LOCK_FILE)

    return dense


if __name__ == "__main__":
    field = resume_or_build() or build_sparse_planetary_grid()
    print(f"Final dense field shape: {field.shape} | Memory: {field.nbytes / 1e9:.3f} GB")
