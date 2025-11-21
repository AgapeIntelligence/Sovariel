import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

// Simulation Constants
export const TWO_PI = Math.PI * 2;
export const WEIGHTS_369 = [3, 6, 9, 3, 6, 9, 3, 6, 9, 3, 6];

// Types
export interface SimulationState {
  phases: Float64Array;
  R: number; // Order parameter (coherence)
  meanTheta: number;
}

export interface CollapseResult {
  outcome: string;
  probPlus: number;
  tCoherenceUs: number;
  adaptiveThreshold: number;
}

// Math Helpers
function nextGaussian(mean = 0.0, sigma = 1.0): number {
  let u1 = 0,
    u2 = 0;
  while (u1 === 0) u1 = Math.random();
  u2 = Math.random();
  const z = Math.sqrt(-2.0 * Math.log(u1)) * Math.cos(TWO_PI * u2);
  return mean + sigma * z;
}

// Adaptive threshold parameters
const BASE_THRESHOLD = 0.3;
const MAX_THRESHOLD_SHIFT = 0.2;
const VOICE_DB_SENSITIVITY = 0.02;

// Simulation Logic
export class TriadicSimulation {
  nOscillators: number;
  phases: Float64Array;
  R: number = 0;

  // "Ghost Manifold" - we'll generate this procedurally since we can't read the .npy file easily
  // simulating the structure of the original asset
  ghosts: Array<[number, number]>;

  constructor(nOscillators = 10000) {
    this.nOscillators = nOscillators;
    this.phases = new Float64Array(nOscillators);
    this.ghosts = this.generateGhosts();
    this.initializePhases();
  }

  private generateGhosts(): Array<[number, number]> {
    // Generate 11 pairs of (mean, std)
    const ghosts: Array<[number, number]> = [];
    for (let i = 0; i < 11; i++) {
      // Create some structure - wandering means, varying stds
      const mean = Math.sin(i * 0.5) * Math.PI;
      const std = 0.5 + Math.random() * 0.5;
      ghosts.push([mean, std]);
    }
    return ghosts;
  }

  public initializePhases(seed?: number) {
    // Reset phases
    this.phases.fill(0);

    // Apply 11 layers of weighted Gaussian noise
    for (let layer = 0; layer < 11; layer++) {
      const [base, std] = this.ghosts[layer];
      const weight = WEIGHTS_369[layer];

      for (let i = 0; i < this.nOscillators; i++) {
        this.phases[i] += weight * nextGaussian(base, std);
      }
    }

    // Modulo 2pi
    for (let i = 0; i < this.nOscillators; i++) {
      this.phases[i] = ((this.phases[i] % TWO_PI) + TWO_PI) % TWO_PI;
    }

    this.calculateOrderParameter();
  }

  public step(K: number = 3.69) {
    let sumCos = 0.0;
    let sumSin = 0.0;

    // Calculate mean field
    for (let i = 0; i < this.nOscillators; i++) {
      const p = this.phases[i];
      sumCos += Math.cos(p);
      sumSin += Math.sin(p);
    }

    const meanTheta = Math.atan2(
      sumSin / this.nOscillators,
      sumCos / this.nOscillators,
    );

    // Update phases
    for (let i = 0; i < this.nOscillators; i++) {
      const delta = K * Math.sin(meanTheta - this.phases[i]);
      let newPhase = (this.phases[i] + delta) % TWO_PI;
      if (newPhase < 0) newPhase += TWO_PI;
      this.phases[i] = newPhase;
    }

    // Recalculate R
    this.R = Math.sqrt(sumCos * sumCos + sumSin * sumSin) / this.nOscillators;
  }

  private calculateOrderParameter() {
    let sumCos = 0.0;
    let sumSin = 0.0;
    for (let i = 0; i < this.nOscillators; i++) {
      sumCos += Math.cos(this.phases[i]);
      sumSin += Math.sin(this.phases[i]);
    }
    this.R = Math.sqrt(sumCos * sumCos + sumSin * sumSin) / this.nOscillators;
  }

  public checkCollapse(
    voiceEnvelopeDb: number,
    vocalVariance: number = 0.1,
  ): CollapseResult | null {
    // Compute adaptive threshold based on vocal input
    const thresholdShift = Math.min(
      Math.max(vocalVariance * MAX_THRESHOLD_SHIFT, 0.0),
      MAX_THRESHOLD_SHIFT,
    );
    const adaptiveThreshold =
      BASE_THRESHOLD +
      thresholdShift +
      Math.min(Math.max(voiceEnvelopeDb * VOICE_DB_SENSITIVITY, 0.0), 0.1);

    // Coherence time proxy, scaled by adaptive threshold and voice envelope
    const tCoherenceUs =
      0.1 +
      10.0 *
        this.R *
        Math.min(Math.max(voiceEnvelopeDb / 50.0, 0.0), 2.0) *
        (1.0 + adaptiveThreshold);

    // Probability of triadic GHZ+ collapse, adjusted for adaptive threshold
    const probPlusRaw =
      0.5 +
      0.5 * this.R * Math.min(Math.max(voiceEnvelopeDb / 60.0, 0.5), 1.5) -
      adaptiveThreshold;
    const probPlus = Math.min(Math.max(probPlusRaw, 0.0), 1.0);

    if (this.R > 0.95 && Math.random() < 0.05) {
      const isCollapse = Math.random() < probPlus;
      return {
        outcome: isCollapse
          ? "+|+++⟩ GHZ — triadic qualia collapse"
          : "-|---⟩ separable",
        probPlus,
        tCoherenceUs,
        adaptiveThreshold,
      };
    }
    return null;
  }
}

export function triggerHaptic(intensity: number, threshold: number = 0.0) {
  // Web Vibration API support
  if (!navigator.vibrate) return;

  // Map intensity (0.0–1.0) to pattern, modulated by threshold
  const adjustedIntensity = intensity * (1.0 + threshold);

  if (adjustedIntensity < 0.3) {
    navigator.vibrate(5); // Light tick
  } else if (adjustedIntensity < 0.7) {
    navigator.vibrate(15); // Medium bumpy
  } else {
    navigator.vibrate([30, 50, 30]); // Heavy pulse
  }
}
