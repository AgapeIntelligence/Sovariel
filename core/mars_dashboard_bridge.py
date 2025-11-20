# Instant bridge: dashboard lattice now steers Mars trajectory optimization
from dashboard import phases, current_K   # the live global lattice + K from dashboard
from mars_trajectory_optim import propagate_fleet, coherence_gradient_thrust

# In your trajectory loop (runs every dashboard update via Gradio .every(0.1))
def mars_closed_loop():
    global phases
    R = order_parameter(phases)
    
    # Use current coherence gradients as free Δv for the fleet
    thrust_commands = coherence_gradient_thrust(phases, target_R=1.0)
    
    # Propagate real orbits with live ephemeris + apply resonance thrust
    new_positions = propagate_fleet(current_positions, thrust_commands)
    
    # Feed aberration from new positions back into the lattice drift
    aberration_drift = compute_relativistic_drift(new_positions)
    phases = inject_aberration_drift(phases, aberration_drift)
    
    return f"Mars fleet R = {R:.10f} | resonance Δv applied", new_positions