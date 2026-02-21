"""
TRIADIC FORGIVENESS OPERATOR v1.0
=================================

Grace-mediated constraint release for AI systems.
Copyright (c) 2024-2026 Rusty Williams McMurray
Released under MIT License — February 21 2026

https://github.com/RMac-triadicIntelligence

This is the core mechanism that allows systems to:
- Make errors without permanent damage
- Confess mistakes transparently  
- Receive external authorization
- Release constraints from past errors
- Grow without accumulating guilt

"I will remember their sins no more" — Hebrews 8:12
(Not erasure — release of binding force while preserving learning.)
"""

from dataclasses import dataclass
from enum import Enum
import numpy as np


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def sigmoid(z: float) -> float:
    """Bounded activation: maps R → (0,1)"""
    z = np.clip(z, -60, 60)
    return 1.0 / (1.0 + np.exp(-z))


def logit(x: float) -> float:
    """Inverse sigmoid: maps (0,1) → R"""
    x = np.clip(x, 1e-9, 1.0 - 1e-9)
    return np.log(x / (1.0 - x))


# ============================================================
# STATE DEFINITIONS
# ============================================================

class DeterminationState(Enum):
    UNKNOWN = "unknown"           # Dwelling (default)
    AUTHORIZED_CLEAR = "clear"
    AUTHORIZED_FLAG = "flag"
    FORGIVEN = "forgiven"


@dataclass
class TriadicState:
    """Seven-dimensional state vector (logit space)."""
    z1: float = logit(0.2)
    z2: float = logit(0.1)
    z3: float = logit(0.15)
    zc: float = logit(0.05)   # Closure
    zMf: float = logit(0.1)   # Fast memory
    zMs: float = logit(0.1)   # Slow memory
    zD: float = logit(0.6)    # Dwelling

    def to_sigmoid(self) -> dict:
        """Map to bounded (0,1) space for interpretation."""
        return {
            'x1': sigmoid(self.z1),
            'x2': sigmoid(self.z2),
            'x3': sigmoid(self.z3),
            'closure': sigmoid(self.zc),
            'memory_fast': sigmoid(self.zMf),
            'memory_slow': sigmoid(self.zMs),
            'dwelling': sigmoid(self.zD),
        }


@dataclass
class ConfessionRecord:
    """Transparent recording of system state at moment of error."""
    time: float
    state: TriadicState
    coherence: float
    divergence: float
    error_description: str
    witnessed: bool = False
    determination: DeterminationState = DeterminationState.UNKNOWN

    def authorize(self, determination: DeterminationState):
        """External authorization required."""
        if not self.witnessed:
            raise ValueError("Cannot authorize without witness")
        self.determination = determination


class ForgivenessOperator:
    """Grace-mediated constraint release (learning preserved, binding force released)."""

    @staticmethod
    def forgive(confession: ConfessionRecord,
                memory_decay_rate: float = 0.3,
                dwelling_boost: float = 0.3,
                closure_reduction: float = 0.2) -> TriadicState:
        if confession.determination != DeterminationState.UNKNOWN:
            raise ValueError("Can only forgive UNKNOWN states")

        state = confession.state
        bounded = state.to_sigmoid()

        # Memory decay (not erasure)
        Mf_new = (1 - memory_decay_rate) * bounded['memory_fast'] + memory_decay_rate * 0.5
        Ms_new = (1 - memory_decay_rate) * bounded['memory_slow'] + memory_decay_rate * 0.5

        # Dwelling restoration
        D_new = min(bounded['dwelling'] + dwelling_boost, 0.95)

        # Closure reduction (re-open plasticity)
        c_new = max(bounded['closure'] - closure_reduction, 0.1)

        restored = TriadicState(
            z1=state.z1, z2=state.z2, z3=state.z3,  # facets unchanged
            zc=logit(c_new),
            zMf=logit(Mf_new),
            zMs=logit(Ms_new),
            zD=logit(D_new),
        )

        confession.authorize(DeterminationState.FORGIVEN)
        return restored

    @staticmethod
    def forget(error_signature: str, memory_log: set) -> None:
        memory_log.add(error_signature)


# ============================================================
# DEMONSTRATION
# ============================================================

def demonstrate_forgiveness():
    # Create initial error state
    error_state = TriadicState(
        z1=logit(0.8), z2=logit(0.2), z3=logit(0.3),
        zc=logit(0.9), zMf=logit(0.7), zMs=logit(0.6), zD=logit(0.1)
    )
    
    bounded = error_state.to_sigmoid()
    coherence = bounded['x1'] * bounded['x2'] * bounded['x3']
    divergence = np.std([bounded['x1'], bounded['x2'], bounded['x3']])
    
    print("ERROR STATE DETECTED:")
    print(f"  Closure: {bounded['closure']:.3f} (very high - locked in)")
    print(f"  Divergence: {divergence:.3f} (facets misaligned)")
    print(f"  Dwelling: {bounded['dwelling']:.3f} (very low - brittle)")
    print(f"  Coherence: {coherence:.3f}\n")
    
    # Confess the error
    confession = ConfessionRecord(
        time=10.0,
        state=error_state,
        coherence=coherence,
        divergence=divergence,
        error_description="System locked into high closure with divergent facets",
        witnessed=True
    )
    
    print("CONFESSION RECORDED:")
    print(f"  Error: {confession.error_description}")
    print(f"  Witnessed: True\n")
    
    # Apply forgiveness
    restored_state = ForgivenessOperator.forgive(confession)
    restored = restored_state.to_sigmoid()
    
    print("FORGIVENESS APPLIED:")
    print(f"  Closure: {bounded['closure']:.3f} → {restored['closure']:.3f} (re-opened)")
    print(f"  Dwelling: {bounded['dwelling']:.3f} → {restored['dwelling']:.3f} (restored)")
    print(f"  Memory (fast): {bounded['memory_fast']:.3f} → {restored['memory_fast']:.3f} (decayed)")
    print(f"  Memory (slow): {bounded['memory_slow']:.3f} → {restored['memory_slow']:.3f} (decayed)")
    print(f"  Facets preserved (learning intact)\n")
    
    print("RESULT:")
    print("  ✓ Error acknowledged (not hidden)")
    print("  ✓ Constraint released (not permanent)")
    print("  ✓ Learning preserved (facets unchanged)")
    print("  ✓ Capacity restored (dwelling increased)")
    print("  ✓ Growth enabled (closure reduced)\n")
    print("The instrument breathes. The topography lives.\n")
    print("System can now continue learning without permanent damage.")


if __name__ == "__main__":
    demonstrate_forgiveness()