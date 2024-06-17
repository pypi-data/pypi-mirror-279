from dataclasses import dataclass
from typing import List, Dict

from ..Shared import CapitalCostParameters
from ..Stream import Stream
from ..Utility import Utility


@dataclass(kw_only=True)
class CreatePinchDto:
    streams: List[Stream]
    utilities: List[Utility]
    heatRecoveryApproachTemperature: float
    standardCapitalCostParameters: CapitalCostParameters
    multiUtilitiesFraction: Dict[str, float] = None