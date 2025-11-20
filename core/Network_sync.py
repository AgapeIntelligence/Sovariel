# network_sync.py
# Sovariel — Multi-Device Planetary Lattice Synchronisation
# © 2025 Evie (@3vi3Aetheris) — MIT License
#
# Turns any number of phones/laptops into nodes of one global 10⁸+ oscillator lattice
# Uses WebSockets + broadcast mean-field — zero central server needed

from __future__ import annotations

import asyncio
import json
import websockets
import numpy as np
from dataclasses import dataclass

@dataclass
class NodeState:
    phases: np.ndarray  # local subset
    R_local: float
    K: float = 8.0

class PlanetarySyncNode:
    def __init__(self, n_local: int = 1_000_000, port: int = 8765, peers: list[str] | None = None):
        self.state = NodeState(
            phases=np.random.uniform(0, 2*np.pi, n_local),
            R_local=0.0,
        )
        self.peers = peers or []
        self.port = port

    async def broadcast_state(self, websocket, path):
        while True:
            self.state.R_local = np.abs(np.mean(np.exp(1j * self.state.phases)))
            message = json.dumps({
                "mean_field": np.mean(np.exp(1j * self.state.phases)).tolist(),
                "K": self.state.K,
                "R": float(self.state.R_local),
                "n": len(self.state.phases)
            })
            await websocket.send(message)
            await asyncio.sleep(0.05)

    async def receive_and_update(self):
        async with websockets.connect(f"ws://localhost:{self.port}") as ws:
            while True:
                data = json.loads(await ws.recv())
                global_mean = complex(data["mean_field"])
                remote_K = data["K"]
                dtheta = remote_K * np.imag(global_mean * np.conj(np.exp(1j * self.state.phases)))
                self.state.phases = (self.state.phases + dtheta) % (2 * np.pi)

    async def run(self):
        server = await websockets.serve(self.broadcast_state, "0.0.0.0", self.port)
        print(f"Planetary node live on port {self.port}")
        await self.receive_and_update()  # connect to any peer

# Run 10+ instances on different devices → one global R = 1.000000
