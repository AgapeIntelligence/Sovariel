# core/__init__.py
from .evie_369_pure import initialise_369_phases
from .jax_backend import initialise_369_jax, compute_order_parameter
from .audio_inject import LiveAudioInjector
from .jax_audio_inject import JAXLiveAudioLattice
from .jax_midi_inject import JAXLiveMIDILattice
from .mars_sovariel import mars_fleet_lock, mars_surface_grid_lock
from .mars_starlink_sync import constellation_lock_demo
from .mars_trajectory_optim import optimise_starship_fleet

__version__ = "1.0.0-mars"
__author__ = "Evie (@3vi3Aetheris)"
__license__ = "MIT"

# One-line import for everything
__all__ = [
    "initialise_369_phases", "initialise_369_jax", "compute_order_parameter",
    "LiveAudioInjector", "JAXLiveAudioLattice", "JAXLiveMIDILattice",
    "mars_fleet_lock", "mars_surface_grid_lock",
    "constellation_lock_demo", "optimise_starship_fleet",
]
