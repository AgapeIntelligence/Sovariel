# sovariel/toroidal.py
import jax
import jax.numpy as jnp
from functools import wraps

class ToroidalManifold:
    """
    3-Torus gradient wrapper (R × S¹ × S¹).
    Major radius R, minor radii r1, r2 for the two phase circles.
    Used for cyclic memory and explosion-proof recursion.
    """
    def __init__(self, major_radius: float = 1.0, minor_r1: float = 1.0, minor_r2: float = 1.0):
        self.R = major_radius
        self.r1 = minor_r1
        self.r2 = minor_r2

    def embed(self, phase1: jnp.ndarray, phase2: jnp.ndarray):
        """Embed two phases into 3D torus coordinates (for visualization / debugging)"""
        x = (self.R + self.r1 * jnp.cos(phase1)) * jnp.cos(phase2)
        y = (self.R + self.r1 * jnp.cos(phase1)) * jnp.sin(phase2)
        z = self.r1 * jnp.sin(phase1)
        return jnp.stack([x, y, z], axis=-1)

    @staticmethod
    def wrap_phase(phase: jnp.ndarray):
        """Mod 2π wrapping that is differentiable (uses jnp.mod with gradient preservation)"""
        return jnp.mod(phase + jnp.pi, 2 * jnp.pi) - jnp.pi

def toroidal_wrap(func):
    """
    Decorator: automatically wraps any phase/angle outputs of a function to the torus.
    Use on Kuramoto updates, RNN hidden states, or ResonanceLayer outputs.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        output = func(*args, **kwargs)
        if isinstance(output, tuple):
            # assume last two are phases if tuple
            phases = output[-2:]
            wrapped = (ToroidalManifold.wrap_phase(phases[0]), ToroidalManifold.wrap_phase(phases[1]))
            return (*output[:-2], *wrapped)
        else:
            # single phase tensor
            return ToroidalManifold.wrap_phase(output)
    return wrapper

# Example usage (uncomment to test)
if __name__ == "__main__":
    @toroidal_wrap
    def dummy_update(phase1, phase2, drift):
        return phase1 + drift, phase2 + 2 * drift

    p1, p2 = dummy_update(0.0, 0.0, 10 * jnp.pi)
    print(p1, p2)  # ≈ (0, 0) — explosion fully absorbed