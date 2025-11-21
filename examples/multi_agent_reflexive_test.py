# examples/prototype/multi_agent_reflexive_test.py
# Sovariel Prototype — Multi-Agent Lattice with Reflexive Feedback
# © 2025 Evie (@3vi3Aetheris)

from core.colossus_dense_grid import DenseLattice
from core.reflexive_lattice import ReflexiveLattice
import matplotlib.pyplot as plt
import numpy as np

# === CONFIGURATION ===
NUM_AGENTS = 4
LATTICE_SIZE = 64  # per agent
STEPS = 100
ENTROPY_THRESHOLD = 0.5
CORRECTION_MAG = 0.05

# === INITIALIZATION ===
agents = []
for i in range(NUM_AGENTS):
    lattice = DenseLattice(size=LATTICE_SIZE)
    lattice.randomize_state()
    reflexive = ReflexiveLattice(lattice)
    agents.append({
        "lattice": lattice,
        "reflexive": reflexive,
        "entropy_log": [],
        "coherence_log": []
    })

# === SIMULATION LOOP ===
global_coherence_log = []

for step in range(STEPS):
    global_state_snapshot = []

    for agent in agents:
        # Lattice evolution step
        agent["lattice"].update()

        # Compute local entropy & coherence
        entropy = agent["reflexive"].compute_entropy()
        coherence = agent["lattice"].compute_global_coherence()

        # Reflexive correction if needed
        if entropy > ENTROPY_THRESHOLD:
            agent["reflexive"].apply_correction(CORRECTION_MAG)

        # Log metrics
        agent["entropy_log"].append(entropy)
        agent["coherence_log"].append(coherence)
        global_state_snapshot.append(agent["lattice"].get_state_copy())

    # Compute global coherence across agents
    combined = np.array(global_state_snapshot)
    global_coherence = np.mean([np.mean(agent_state) for agent_state in combined])
    global_coherence_log.append(global_coherence)

    if step % 10 == 0:
        print(f"Step {step}: Global coherence = {global_coherence:.4f}")

# === VISUALIZATION ===
plt.figure(figsize=(12, 6))

for idx, agent in enumerate(agents):
    plt.plot(agent["coherence_log"], label=f"Agent {idx} coherence")
plt.plot(global_coherence_log, label="Global coherence", linewidth=2, color="k")
plt.xlabel("Step")
plt.ylabel("Coherence")
plt.title("Multi-Agent Lattice + Reflexive Feedback")
plt.legend()
plt.show()

# Optional: save log to file for further analysis
import pickle
with open("examples/prototype/multi_agent_reflexive_log.pkl", "wb") as f:
    pickle.dump({
        "agents": agents,
        "global_coherence": global_coherence_log
    }, f)

print("Experiment complete. Logs saved to 'multi_agent_reflexive_log.pkl'.")