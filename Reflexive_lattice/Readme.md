# Reflexive Lattice

Lightweight real-time coherence + bounded-entropy monitor for neural activations.

```bash
pip install git+https://github.com/AgapeIntelligence/Sovariel.git#subdirectory=reflexive_lattice

from reflexive_lattice import LatticeEngine

engine = LatticeEngine(min_coherence=0.80, max_entropy=0.05)

for value in activations:
    report = engine.update(value)
    if not report.safe:
        # trigger review / halt / corrigibility
        break
