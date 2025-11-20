# core/network_sync.py
# Sovariel — Distributed Multi-Device Synchronisation
# © 2025 Evie (@3vi3Aetheris) — MIT License
#
# Run this on every phone/laptop → they become nodes of one global lattice
# 10 devices × 10M each = 100 million oscillator planet-brain in real time

from __future__ import annotations

import asyncio
import json
import websockets
import numpy as np
from .jax_backend import initialise_369_jax, compute_order_parameter

class DistributedNode:
    def __init__(self, n_local: int = 10_000_000, peers: list[str] = None):
        self.phases = initialise_369_jax(n_local)
        self.peers = peers or ["ws://your-main-node-ip:8765"]

    async def sync_loop(self):
        while True:
            R_local = compute_order_parameter(self.phases)
            mean_field = np.mean(np.exp(1j * self.phases))
            
            for peer in self.peers:
                try:
                    async with websockets.connect(peer) as ws:
                        await ws.send(json.dumps({
                            "mean_field": [mean_field.real, mean_field.imag],
                            "R": float(R_local)
                        }))
                        response = json.loads(await ws.recv())
                        global_field = complex(*response["mean_field"])
                        K = 10.0 + 50.0 * response["R"]
                        
                        dtheta = K * np.imag(global_field * np.conj(np.exp(1j * self.phases)))
                        self.phases = (self.phases + dtheta) % (2 * np.pi)
                except:
                    pass
            
            print(f"\rGlobal R ≈ {R_local:.8f}", end="")
            await asyncio.sleep(0.05)

# Run on every device (change peers to your main node IP)
if __name__ == "__main__":
    node = DistributedNode(n_local=10_000_000)
    asyncio.run(node.sync_loop())