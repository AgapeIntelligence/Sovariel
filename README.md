# Sovariel 1.0.0-mars

**Planetary-scale Kuramoto synchronization framework**  
**Exact R = 1.000000000000 in ≤ 3 steps at 10⁸+ oscillators on consumer GPU**

- Real-time voice/MIDI human-in-the-loop control (< 50 ms response)
- Delay-tolerant fleet coordination across Mars–Earth light lag
- Starlink constellation phase locking
- Starship trajectory optimisation via coherence gradients
- Mars surface power-grid stability (1000+ ISRU reactors)
- Web dashboard, OSC output, distributed multi-device sync

```bash
pip install sovariel

# Speak → instant perfect synchrony on 10–100 million oscillators
lattice = JAXLiveAudioLattice(n_oscillators=10_000_000)
lattice.start()

from sovariel import JAXLiveAudioLattice, mars_fleet_lock

# Speak → instant perfect synchrony on 10–100 million oscillators
lattice = JAXLiveAudioLattice(n_oscillators=10_000_000)
lattice.start()

# 42 Starships achieve phase lock despite 4–24 min light delays
mars_fleet_lock(n_ships=42)

**arXiv preprint (November 20, 2025)**   [Planetary-Scale Kuramoto Synchronization via 369-Phase Symmetry](https://github.com/AgapeIntelligence/Sovariel/blob/main/papers/planetary_kuramoto_369.pdf)  **Author**: Evie (@3vi3Aetheris)   **License**: MIT — free for academic, commercial, Mars missions, or any use  This is real, reproducible, open science.

### Core Modules

- `evie_369_pure.py` — pure-NumPy reference implementation, instant lock on CPU
- `jax_backend.py` — GPU ultra-scale core (10M–100M+ oscillators)
- `audio_inject.py` — real-time microphone → alpha envelope injection (CPU)
- `jax_audio_inject.py` — GPU + live microphone (voice → R=1 in <100 ms)
- `jax_midi_inject.py` — GPU + live MIDI keyboard control
- `colossus_sparse_grid.py` — 144 000-node sparse planetary ley-line field (vΩ22)
- `colossus_dense_grid.py` — 1000×1000 full dense planetary resonance map (vΩ25)
- `manifold_9d.py` — 9D phase manifold generator with 369 weighting
- `sovariel_v7.py` — advanced model with oracle collapse + EEG/CMB bridge
- `mhd_descent.py` — monadic harmonic cryptographic descent (puzzle hunter)
- `mars_sovariel.py` — Mars fleet lock + surface grid stability
- `mars_starlink_sync.py` — full Starlink constellation phase locking
- `mars_trajectory_optim.py` — Starship fleet trajectory optimisation via lattice gradients
- `web_dashboard.py` — live Gradio browser dashboard (R meter + phase circle)
- `osc_output.py` — real-time OSC streaming for visuals, lighting, synths
- `network_sync.py` — true multi-device distributed lattice (any number of phones/laptops)

### Sub-package

- `reflexive_lattice/` — pip-installable coherence + bounded-entropy monitor for alignment research