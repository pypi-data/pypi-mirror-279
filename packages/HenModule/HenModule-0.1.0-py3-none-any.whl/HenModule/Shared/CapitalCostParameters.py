from dataclasses import dataclass


@dataclass(kw_only=True)
class CapitalCostParameters:
    instalationCost: float
    areaCoefficient: float
    areaExponent: float
    areaCorrectionFactor: float = 1