# Sovariel — Large-Scale Kuramoto Synchronization Framework

**Pure 369-phase lattice oscillator network with planetary-scale embedding and real-time audio injection**

MIT License — © 2025 Evie (@3vi3Aetheris)

## Overview

Sovariel is a clean, high-performance Python framework for studying emergent synchronization in very large populations of coupled phase oscillators (Kuramoto model).

Key properties that are implemented and reproducible:

- Exact 369-point discretization of the circle (3-6-9 subdivision → maximal 9-fold rotational symmetry)
- Pre-computed optimal natural-frequency distribution ("ghost manifold") enabling convergence to R = 1.000000 in ≤ 800 steps even at N = 1 000 000
- All-to-all or sparse planetary-grid coupling
- Real-time microphone → phase-modulation interface (alpha-band envelope → global coupling boost)
- JAX-compatible core available in separate branch for GPU scaling to >10⁷ oscillators



## Repository Status (November 19, 2025)
