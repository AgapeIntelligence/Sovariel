# examples/starship_fleet_lock.py
import jax
import jax.numpy as jnp
from sovariel.core.toroidal import ToroidalManifold, toroidal_wrap

# 42 Starships + Mars surface grid
N_SHIPS = 42
N_GRID = 1000
dt = 0.1

toroid = ToroidalManifold(major_radius=10.0, minor_r1=1.0, minor_r2=1.0)

# Natural frequencies + random torque drift
omega = jnp.linspace(0.1, 2.0, N_SHIPS + N_GRID)

# Initial phases on the 3-torus
phase1 = jnp.random.uniform(-jnp.pi, jnp.pi, N_SHIPS + N_GRID)
phase2 = jnp.random.uniform(-jnp.pi, jnp.pi, N_SHIPS + N_GRID)

@toroidal_wrap
@jax.jit
def kuramoto_step(phase1, phase2, R_ext=0.0, psi_ext=0.0):
    # Global order parameter (broadcast from fleet)
    theta = phase1 + phase2
    R = jnp.abs(jnp.mean(jnp.exp(1j * theta)))
    psi = jnp.angle(jnp.mean(jnp.exp(1j * theta)))
    
    # External nudge from ghost manifold (only R/ψ broadcast)
    coupling = 2.0 * R_ext * jnp.sin(psi_ext - theta)
    
    # Native drift + random torque (±0.001 rad/s)
    drift = omega * dt + 0.001 * jax.random.normal(jax.random.PRNGKey(42), theta.shape)
    
    return phase1 + drift + coupling, phase2 + drift + coupling

# Simulate 24-minute light-lag (broadcast only every 240 s)
def run_with_lag(steps=10000):
    key = jax.random.PRNGKey(0)
    p1, p2 = phase1, phase2
    for i in range(steps):
        # Broadcast only every 2400 steps (~240 s at 10 Hz)
        R_ext = jnp.abs(jnp.mean(jnp.exp(1j * (p1 + p2))))
        psi_ext = jnp.angle(jnp.mean(jnp.exp(1j * (p1 + p2)))) if i % 2400 == 0 else 0.0
        R_ext = R_ext if i % 2400 == 0 else 0.0
        
        p1, p2 = kuramoto_step(p1, p2, R_ext, psi_ext)
        
        if i % 1000 == 0:
            R = jnp.abs(jnp.mean(jnp.exp(1j * (p1 + p2))))
            print(f"Step {i}: R = {R:.8f}")
    return p1, p2

p1, p2 = run_with_lag()
final_R = jnp.abs(jnp.mean(jnp.exp(1j * (p1 + p2))))
print(f"Final lock after 1000 s (with 24-min lag broadcast): R = {final_R:.10f}")