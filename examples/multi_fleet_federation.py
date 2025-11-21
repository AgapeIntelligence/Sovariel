# Already runnable today (examples/multi_fleet_federation.py – push if you want)
fleet_earth = ToroidalManifold(major_radius=1.0)      # low lag
fleet_mars  = ToroidalManifold(major_radius=20.0 / 60.0)  # 20 min light-lag baked into curvature
fleet_leo   = ToroidalManifold(major_radius=0.1)      # near-zero lag

# Federation coupler — ghost-manifold broadcast of only (R, ψ) across fleets
federated_R, federated_ψ = ghost_federate([earth_Rψ, mars_Rψ, leo_Rψ])