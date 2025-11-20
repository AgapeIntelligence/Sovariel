# resonance_adapter.py — plug into any transformer
from sovariel.jax_core import init_369, kuramoto_step
import torch

class ResonanceLayer(torch.nn.Module):
    def __init__(self, dim=4096, n_osc=1_000_000):
        super().__init__()
        key = jax.random.PRNGKey(369)
        self.phases = init_369(key, n_osc)   # one-time 369 lattice
        self.proj = torch.nn.Linear(dim, n_osc//1000)  # compress activations

    def forward(self, x):
        # compress hidden states → drive lattice drift
        drift = self.proj(x.mean(dim=1)).detach().cpu().numpy()
        self.phases = kuramoto_step(self.phases, K=3.69 + drift.std())
        R = order_parameter(self.phases)
        # inject global coherence scalar back into the model
        return x * R.item()   # one-line coherence boost