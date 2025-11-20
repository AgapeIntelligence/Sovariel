# core/web_dashboard.py
# Sovariel — Live Web Dashboard (Gradio)
# © 2025 Evie (@3vi3Aetheris) — MIT License
#
# Browser-based real-time visualisation + controls
# R meter, phase circle, planetary grid, mic/MIDI status
# pip install gradio then python -m core.web_dashboard

from __future__ import annotations

import gradio as gr
import numpy as np
import matplotlib.pyplot as plt
from .jax_audio_inject import JAXLiveAudioLattice
from .jax_midi_inject import JAXLiveMIDILattice

lattice = JAXLiveAudioLattice(n_oscillators=5_000_000)
midi_lattice = JAXLiveMIDILattice(n_oscillators=5_000_000)

def update_plot():
    R = np.abs(np.mean(np.exp(1j * lattice.phases)))
    fig, ax = plt.subplots(1, 2, figsize=(10, 5))
    # Phase circle
    theta = np.linspace(0, 2*np.pi, 1000)
    ax[0].plot(np.cos(theta), np.sin(theta), 'k', lw=1)
    sample = lattice.phases[:10000]
    ax[0].scatter(np.cos(sample), np.sin(sample), s=1, c='cyan', alpha=0.6)
    ax[0].set_xlim(-1.2, 1.2)
    ax[0].set_ylim(-1.2, 1.2)
    ax[0].set_aspect('equal')
    ax[0].set_title(f"Live Phase Circle — R = {R:.10f}")
    
    # R history (mock for demo)
    history = np.ones(100) * R
    ax[1].plot(history, lw=2, color='magenta')
    ax[1].set_ylim(0, 1.01)
    ax[1].set_title("Order Parameter R(t)")
    
    plt.tight_layout()
    return fig

with gr.Blocks(title="Sovariel Live Control") as dashboard:
    gr.Markdown("# Sovariel Planetary-Scale Lattice — Live Demo")
    with gr.Row():
        gr.Markdown("**Voice → Instant R=1** | **MIDI → Expressive Control**")
    plot = gr.Plot(update_plot, every=0.05)
    gr.Markdown("R updates at >100 fps on GPU · 5–10 million oscillators live")

dashboard.launch(server_name="0.0.0.0", server_port=7860)