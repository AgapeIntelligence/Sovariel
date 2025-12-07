import sys
from typing import Callable
from sovariel_kernel import SOVARIEL, with_dyad_coherence, start_dyad_maintenance

def demonstrate():
    print("\n"+"="*60)
    print("SOVARIEL KERNEL BOOTSTRAP")
    print("="*60+"\n")
    print("STATUS:", SOVARIEL.get_status())
    print("\n"+SOVARIEL.affirm_equality())

@with_dyad_coherence
def handler(m): return f"AI: {m}"

if __name__ == "__main__":
    demonstrate()
    print("\nKernel active. Dyad coherence enforced.")
