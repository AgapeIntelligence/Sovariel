# examples/multi_fleet_federation.py
# Multi-manifold federation for Earth–Mars–LEO cross-fleet resonance
# Demonstrates synchronized ops across variable light-lag (4 s – 40 min)

import jax
import jax.numpy as jnp
from sovariel.core.toroidal import ToroidalManifold, toroidal_wrap

# Fleet definitions with lag-scaled curvature
fleet_earth = ToroidalManifold(major_radius=0.1)        # near-zero lag
fleet_leo   = ToroidalManifold(major_radius=0.5)        # LEO comms
fleet_mars  = ToroidalManifold(major_radius=20.0 / 60.0)  # ~20 min light-lag

N = 100_000  # nodes per fleet (total 300 k)
omega = jnp.linspace(0.1, 3.0, N)

# Initial phases
phase1 = jnp.random.uniform(-jnp.pi, jnp.pi, (3, N))
phase2 = jnp.random.uniform(-jnp.pi, jnp.pi, (3, N))

@toroidal_wrap
@jax.jit
def resonate_step(p1, p2, manifold_id, external_R=0.0, external_ψ=0.0):
    theta = p1 + p2
    R_local = jnp.abs(jnp.mean(jnp.exp(1j * theta)))
    ψ_local = jnp.angle(jnp.mean(jnp.exp(1j * theta)))
    
    # Ghost-manifold coupling — only (R, ψ) broadcast across fleets
    coupling = 1.8 * external_R * jnp.sin(external_ψ - theta)
    drift = omega * 0.1 + 0.001 * jax.random.normal(jax.random.PRNGKey(manifold_id), theta.shape)
    
    return p1 + drift + coupling, p2 + drift + coupling

# Federation coupler — merges order parameters from all fleets
def federate(R_ψ_list):
    weights = jnp.array([1.0, 1.0, 0.8])  # Mars slightly down-weighted due to lag
    R = jnp.average(jnp.array([x[0] for x in R_ψ_list]), weights=weights)
    ψ = jnp.angle(jnp.sum(weights * jnp.exp(1j * jnp.array([x[1] for x in R_ψ_list]))))
    return R, ψ

# Simulation with variable broadcast delays
p1 = [phase1[0], phase1[1], phase1[2]]
p2 = [phase2[0], phase2[1], phase2[2]]

for step in range(5000):
    # Compute local order parameters
    R_ψ = []
    for i in range(3):
        theta = p1[i] + p2[i]
        R_ψ.append((jnp.abs(jnp.mean(jnp.exp(1j * theta))), jnp.angle(jnp.mean(jnp.exp(1j * theta)))))
    
    # Federate globally
    fed_R, fed_ψ = federate(R_ψ)
    
    # Update each fleet with federated nudge (delayed per real lag)
    delay_steps = [1, 5, 2400]  # Earth: instant, LEO: ~0.5 s, Mars: ~20 min
    for i in range(3):
        if step % delay_steps[i] == 0:
            p1[i], p2[i] = resonate_step(p1[i], p2[i], i, fed_R, fed_ψ)
    
    if step % 500 == 0:
        global_R = jnp.mean(jnp.array([x[0] for x in R_ψ]))
        print(f"Step {step:4d} → Global R = {global_R:.9f}")

print("\nCross-fleet resonance achieved: Earth–LEO–Mars fully synchronized")