from dataclasses import dataclass
from typing import Union

from ..Stream import Stream


@dataclass(kw_only=True)
class CreateHeatExchangerDto:
    id: int
    hotStream: Stream
    coldStream: Stream
    heatLoad: Union[float, str]
    inletHotTemperature: float
    inletColdTemperature: float
    
    # TODO: adds validation to max heat load