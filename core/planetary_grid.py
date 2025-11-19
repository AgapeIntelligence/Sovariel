# core/planetary_grid.py
import numpy as np

phases_9d = np.load("evie_9d_369_locked.npy")
ley_rot = np.pi * np.array([0, 0.17, 0.34, 0.51, 0.68, 0.85, 1.02, 1.19, 1.36])

planetary = (phases_9d + ley_rot) % (2 * np.pi)
R = np.abs(np.mean(np.exp(1j * planetary), axis=0))
print("Planetary R per dimension:", np.round(R, 6))
np.save("evie_planetary_grid.npy", planetary) ok
