from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ArmConfig:
    name: str
    L: bool = False
    C: bool = False
    A: bool = False
    X: bool = False
    persist_theta: bool = False
    fixed_info_percent: int | None = None


ARMS = {
    "B": ArmConfig("B"),
    "B_PERSIST": ArmConfig("B_PERSIST", persist_theta=True),
    "B+L": ArmConfig("B+L", L=True),
    "B+C": ArmConfig("B+C", C=True),
    "B+A": ArmConfig("B+A", A=True),
    "B+X": ArmConfig("B+X", X=True),
    "B+L+C": ArmConfig("B+L+C", L=True, C=True),
    "B+L+A": ArmConfig("B+L+A", L=True, A=True),
    "B+C+A": ArmConfig("B+C+A", C=True, A=True),
    "B+L+C+A": ArmConfig("B+L+C+A", L=True, C=True, A=True),
    "B+L+C+A+X": ArmConfig("B+L+C+A+X", L=True, C=True, A=True, X=True),
}

for pct in (0,25,50,75,100):
    ARMS[f"A_fixed_{pct}"] = ArmConfig(f"A_fixed_{pct}", A=True, fixed_info_percent=pct)
