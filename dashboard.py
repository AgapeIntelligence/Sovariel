# sovariel/dashboard.py
# Live Voice → Planetary Lattice Steering + OSC
# Requires: jax[cuda], gradio, python-osc, sounddevice
# © 2025 Evie + Grok — MIT

import jax
import jax.numpy as jnp
from jax import jit
import numpy as np
import sounddevice as sd
import gradio as gr
from pythonosc import udp_client
import threading
import time
from jax_core import init_369, kuramoto_step, order_parameter  # from previous file

# === Global lattice state ===
N = 500_000_000  # 500 million — feels instant, looks insane
key = jax.random.PRNGKey(42)
phases = init_369(key, N)
K_base = 0.1
current_K = K_base

# OSC client (change IP/port if controlling external software/hardware)
osc_client = udp_client.SimpleUDPClient("127.0.0.1", 5005)

def audio_thread():
    global current_K
    def callback(indata, frames, time_info, status):
        global current_K
        volume_norm = np.linalg.norm(indata) * 12
        current_K = K_base + volume_norm * 8.0
        current_K = np.clip(current_K, 0.1, 10.0)
        # Send OSC instantly
        osc_client.send_message("/K", float(current_K))
        osc_client.send_message("/R", float(order_parameter(phases)))
    with sd.InputStream(callback=callback, channels=1, samplerate=44100):
        while True:
            time.sleep(0.01)

threading.Thread(target=audio_thread, daemon=True).start()

# Jitted step for max speed
@jit
def lattice_step(phases, K):
    return kuramoto_step(phases, K)

def update_lattice(voice_boost=0.0):
    global phases, current_K
    K = current_K + voice_boost  # manual slider fallback
    phases = lattice_step(phases, K)
    R = float(order_parameter(phases))
    osc_client.send_message("/R", R)
    return (
        f"R = {R:.10f} | K = {K:.3f}",
        f"data:image/png;base64,{phase_circle_plot(phases)}"
    )

def phase_circle_plot(phases):
    import matplotlib.pyplot as plt
    plt.figure(figsize=(6,6), facecolor="#000")
    plt.scatter(jnp.cos(phases[::1000]), jnp.sin(phases[::1000]), c='cyan', s=1, alpha=0.6)
    plt.xlim(-1.1,1.1); plt.ylim(-1.1,1.1)
    plt.axis('off')
    import io, base64
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', facecolor='#000')
    buf.seek(0)
    return base64.b64encode(buf.read()).decode()

# Gradio interface
with gr.Blocks(css="footer{display:none} body{background:#000} .gr-button{background:#0ff}") as demo:
    gr.Markdown("# Sovariel Live — Speak to the Planet")
    with gr.Row():
        with gr.Column(scale=2):
            plot = gr.Image(label="Phase Circle", height=500)
        with gr.Column():
            r_display = gr.Markdown("### R = 0.0000000000\nK = 0.100")
            gr.Markdown("🎤 Speak, hum, or sing → the lattice responds instantly")
            boost = gr.Slider(0, 10, label="Manual K Boost", value=0)
    boost.change(update_lattice, boost, [r_display, plot])
    demo.load(update_lattice, None, [r_display, plot], every=0.05)

if __name__ == "__main__":
    demo.launch(share=True, server_name="0.0.0.0")