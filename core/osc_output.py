# core/osc_output.py
# Sovariel — Real-Time OSC Output
# © 2025 Evie (@3vi3Aetheris) — MIT License
#
# Streams R, mean phase, and frequency spectrum via OSC
# Use with TouchDesigner, Resolume, Ableton, VCVRack, or DMX lights

from __future__ import annotations

from pythonosc import udp_client
import numpy as np
import time
from .jax_backend import initialise_369_jax, compute_order_parameter

client = udp_client.SimpleUDPClient("127.0.0.1", 9000)  # default TouchDesigner port

phases = initialise_369_jax(10_000_000)

while True:
    R = compute_order_parameter(phases)
    mean_phase = np.angle(np.mean(np.exp(1j * phases)))
    
    client.send_message("/sovariel/R", float(R))
    client.send_message("/sovariel/phase", float(mean_phase))
    client.send_message("/sovariel/coherence", float(R**10))  # exaggerated for visuals
    
    # Simple frequency proxy for lighting/synth
    freq = 60 + 400 * R  # 60–460 Hz
    client.send_message("/sovariel/freq", float(freq))
    
    phases = kuramoto_step_jax(phases, K=8.0 + 40*R)  # self-modulating
    
    time.sleep(0.016)  # ~60 fps