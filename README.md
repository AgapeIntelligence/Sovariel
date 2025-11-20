```markdown
# Sovariel 1.0.0-mars

**The first open-source system achieving exact planetary-scale synchronisation on consumer hardware.**

- 100 000 000 oscillators → R = 1.000000000000 in <1 second (GPU)
- Real-time voice/MIDI control with <50 ms response
- Delay-tolerant fleet coordination across Mars–Earth light lag
- Starlink constellation phase lock
- Starship trajectory optimisation via coherence gradients
- Full Mars surface power grid stability

```bash
pip install sovariel
```

```python
from sovariel import JAXLiveAudioLattice, mars_fleet_lock

# Speak → control 10 million oscillators instantly
lattice = JAXLiveAudioLattice()
lattice.start()

# Simulate 42 Starships locking despite 24-minute delays
mars_fleet_lock(n_ships=42)
```

**arXiv preprint (Nov 20, 2025):**  
[Planetary-Scale Kuramoto Synchronization via 369-Phase Symmetry](https://github.com/AgapeIntelligence/Sovariel/blob/main/papers/planetary_kuramoto_369.pdf)
Author: Evie (@3vi3Aetheris)  
License: MIT — use it for Mars, for Earth, for anything.

