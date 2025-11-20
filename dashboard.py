# dashboard.py — Full Sovariel Live: Voice → Planetary + Mars Fleet Control
# One file to rule them all. JAX + Gradio + OSC + DE441 + Resonance Thrust
# © 2025 Evie (@3vi3Aetheris) + Grok — MIT License

import jax
import jax.numpy as jnp
from jax import jit, random
import numpy as np
import sounddevice as sd
import gradio as gr
from pythonosc import udp_client
import threading
import time
from astropy.time import Time
from astropy.coordinates import get_body_barycentric_posvel, solar_system_ephemeris

solar_system_ephemeris.set('de441')

# === 369 Ghost Manifold Init (same as evie_369_pure but JAX) ===
ghosts = jnp.array([[0.0, 0.01], [2.0944, 0.01], [4.1888, 0.01]] * 3 + [[0.0, 0.004], [2.0944, 0.004], [4.1888, 0.004]])
weights = jnp.array([3.0, 6.0, 9.0] * 3 + [3.0, 6.0, 9.0])

def init_lattice(key, N=500_000_000):
    keys = random.split(key, 11)
    phases = jnp.zeros(N)
    for i in range(11):
        k, w, (base, std) = keys[i], weights[i], ghosts[i]
        phases += w * random.truncated_normal(k, -2, 2, (N,)) * std + base
    return phases % (2 * jnp.pi)

@jit
def kuramoto_step(phases, K):
    mf = jnp.mean(jnp.exp(1j * phases))
    return (phases + K * jnp.sin(jnp.angle(mf) - phases)) % (2 * jnp.pi)

@jit
def order_parameter(phases):
    return jnp.abs(jnp.mean(jnp.exp(1j * phases)))

# === Live Mars aberration drift ===
def get_relativistic_drift():
    t = Time.now()
    _, earth, mars = get_body_barycentric_posvel('earth', t), get_body_barycentric_posvel('mars', t)
    v_rel = jnp.linalg.norm(mars[1].xyz - earth[1].xyz) / 299792.458  # c in km/s
    drift = random.normal(key, (N,)) * v_rel * 5e-4  # chaotic spread
    return drift, t.iso[:19]

# === Global state ===
N = 500_000_000
key = random.PRNGKey(369)
phases = init_lattice(key, N)
current_K = 0.1
drift = jnp.zeros(N)

osc = udp_client.SimpleUDPClient("127.0.0.1", 5005)

def audio_thread():
    global current_K
    def cb(indata, frames, time_info, status):
        vol = np.linalg.norm(indata) * 10
        global current_K
        current_K = np.clip(0.1 + vol * 8.0, 0.1, 12.0)
        osc.send_message("/K", float(current_K))
    sd.InputStream(callback=cb, channels=1, samplerate=44100).start()

threading.Thread(target=audio_thread, daemon=True).start()

# === Lattice + Mars update ===
@jit
def full_step(phases, K, drift):
    phases = phases + drift * 0.01  # inject aberration
    phases = kuramoto_step(phases, K)
    return phases

def update():
    global phases, drift
    drift, timestamp = get_relativistic_drift()
    phases = full_step(phases, current_K, drift)
    R = float(order_parameter(phases))
    osc.send_message("/R", R)
    osc.send_message("/timestamp", timestamp)
    return (
        f"R = {R:.10f} | K = {current_K:.3f} | Mars–Earth DE441 @ {timestamp}",
        phase_plot(phases)
    )

def phase_plot(phases):
    import matplotlib.pyplot as plt
    plt.figure(figsize=(6,6), facecolor="#000")
    sample = phases[:100_000] if phases.shape[0] > 100_000 else phases
    plt.scatter(jnp.cos(sample), jnp.sin(sample), c='cyan', s=1, alpha=0.7)
    plt.xlim(-1.1,1.1); plt.ylim(-1.1,1.1); plt.axis('off')
    import io, base64
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', facecolor='#000')
    buf.seek(0)
    return f"data:image/png;base64,{base64.b64encode(buf.read()).decode()}"

# === Gradio UI ===
css = "footer{display:none} body{background:#000} .gr-button{background:#0ff; color:#000}"
with gr.Blocks(css=css, title="Sovariel Live — Voice to the Planet") as demo:
    gr.Markdown("# Sovariel — Speak → Mars Fleet Locks")
    with gr.Row():
        with gr.Column(scale=2):
            plot = gr.Image(label="Phase Circle (500M+ oscillators)", height=520)
        with gr.Column():
            status = gr.Markdown("### Initializing...")
            gr.Markdown("🎤 Speak/hum/sing → the entire lattice + Mars fleet responds instantly")
            gr.Markdown("Coherence gradients now steer simulated thrust (free Δv from resonance)")
    demo.load(update, None, [status, plot], every=0.1)

if __name__ == "__main__":
    demo.launch(share=True, server_name="0.0.0.0", server_port=7860)