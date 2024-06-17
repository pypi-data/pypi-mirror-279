from dataclasses import dataclass
from typing import List

from ..Stream import Stream
from ..Utility import Utility


@dataclass(kw_only=True)
class CreateHeatExchangerNetworkDto:
    streams: List[Stream]
    utilities: List[Utility]

    exchangerMinimumTemperatureApproach: float