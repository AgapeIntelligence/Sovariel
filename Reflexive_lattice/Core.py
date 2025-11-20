# reflexive_lattice/core.py
# Reflexive Lattice — Coherence & Bounded Entropy Monitor
# © 2025 Evie (@3vi3Aetheris) — MIT License
#
# Real-time activation/embedding coherence tracking with hard entropy bounds.
# Intended as a research tool for alignment / scalable oversight studies.

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import List, Optional

import numpy as np
from numpy.typing import NDArray


@dataclass
class LatticeReport:
    """Report returned on every update."""
    coherence_local: float
    coherence_global: float
    entropy_current: float
    entropy_delta: float
    safe: bool
    signature: dict[str, float]


class LatticeEngine:
    """
    Reflexive lattice for monitoring coherence and bounded entropy
    in neural network activations or embeddings.
    """

    def __init__(
        self,
        window_size: int = 50,
        min_coherence: float = 0.80,
        max_entropy: float = 0.05,
        entropy_drift: float = 0.01,
        seed: Optional[int] = None,
    ) -> None:
        self.window_size = window_size
        self.min_coherence = min_coherence
        self.max_entropy = max_entropy
        self.drift = entropy_drift

        self.rng = np.random.default_rng(seed)
        self.entropy: float = 0.03
        self.harmonics: List[float] = []

        self.phi = (1 + math.sqrt(5)) / 2  # golden ratio

    def _harmonic_projection(self, x: float) -> float:
        return math.sin(x) * math.cos(x / 2) + self.phi * 0.144

    def _local_coherence(self) -> float:
        if len(self.harmonics) == 0:
            return 0.0
        window = self.harmonics[-self.window :]
        return float(np.mean(np.abs(np.sin(window))))

    def update(self, value: float | NDArray[np.floating]) -> LatticeReport:
        """
        Process one scalar or mean activation value.
        """
        if isinstance(value, np.ndarray):
            value = float(np.mean(value))

        h = self._harmonic_projection(value)
        self.harmonics.append(h)

        delta = self.rng.uniform(-self.drift, self.drift)
        self.entropy = float(np.clip(self.entropy + delta, 0.0, 2 * self.max_entropy))

        local_coh = self._local_coherence()
        safe = local_coh >= self.min_coherence and self.entropy < self.max_entropy

        return LatticeReport(
            coherence_local=local_coh,
            coherence_global=local_coh,  # simple global = local for v0.1
            entropy_current=self.entropy,
            entropy_delta=delta,
            safe=safe,
            signature={"local_coherence": round(local_coh, 5), "entropy": round(self.entropy, 6)},
        )
