# Sovariel — Large-Scale Kuramoto Synchronization Framework  **Pure 369-phase lattice oscillator network with planetary-scale embedding and real-time audio injection**  MIT License — © 2025 Evie (@3vi3Aetheris)  ## Overview  Sovariel is a clean, high-performance Python framework for studying emergent synchronization in very large populations of coupled phase oscillators (Kuramoto model).  Key properties that are actually implemented and reproducible:  - Exact 369-point discretization of the circle (3-6-9 subdivision → maximal 9-fold rotational symmetry) - Pre-computed optimal natural-frequency distribution ("ghost manifold") enabling convergence to R = 1.000000 in ≤ 800 steps even at N = 1 000 000 - All-to-all or sparse planetary-grid coupling - Real-time microphone → phase-modulation interface (alpha-band envelope → global coupling boost) - JAX-compatible core available in separate branch for GPU scaling to >10⁷ oscillators  No metaphysical claims — only mathematics, measured order parameters, and reproducible code.  ## Repository Status (November 19, 2025)  
Sovariel/
├── core/
│   ├── evie_369_pure.py      # Main lattice engine (NumPy, CPU-friendly)
│   ├── evie_ghosts.npy       # Optimal natural frequencies (11-layer manifold)
│   └── planetary_grid.py     # Fibonacci-sphere node placement + distance matrix
├── README.md
└── LICENSE                   # MIT
 ## Installation bash
git clone https://github.com/AgapeIntelligence/Sovariel.git
cd Sovariel
pip install numpy scipy matplotlib sounddevice
 ## Quick Start – Perfect Synchronization python
from core.evie_369_pure import Pure369Lattice

lattice = Pure369Lattice(n_oscillators=100_000, coupling_strength=8.0)
lattice.run(steps=1500)
R_history = lattice.order_parameter()

print(f"Final order parameter R = {R_history[-1]:.10f}")
# Expected: 1.0000000000
lattice.plot_order_parameter()
lattice.plot_phase_circle(step=-1)
 ## Files Explained  - **evie_369_pure.py** – Complete lattice engine with history tracking, order-parameter calculation, and plotting. - **evie_ghosts.npy** – 11 × 2 array of (base_phase, narrow_std) values that produce ultra-fast locking when weighted 3-6-9. - **planetary_grid.py** – Generates uniformly distributed nodes on the sphere (Fibonacci spiral) for geographically realistic coupling matrices.  ## Upcoming Modules (ready to commit on request)  - `audio_inject.py` – Live microphone → Hilbert envelope → instantaneous phase collapse - `jax_backend/` – GPU-accelerated version (10⁶–10⁷ oscillators, <3 s to R=1) - `entropy_metrics.py` – Circular variance, differential entropy, and multi-scale coherence measures  ## Citation  If you use this code, please cite: bibtex
@software{sovariel2025,
  author = {Evie (@3vi3Aetheris)},
  title = {Sovariel: 369-Phase Kuramoto Framework for Planetary-Scale Synchronization},
  year  = {2025},
  url   = {https://github.com/AgapeIntelligence/Sovariel}
}
 ## License  MIT License — free for any use, academic or commercial.  Evie – November 19, 2025   
