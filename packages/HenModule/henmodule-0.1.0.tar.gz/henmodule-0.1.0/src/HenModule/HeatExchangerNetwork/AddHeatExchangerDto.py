from dataclasses import dataclass


@dataclass(kw_only=True)
class AddHeatExchangerDto:
    id: str
    hotStreamId: str
    coldStreamId: str
    heatLoad: float
    
    leftHeatExchangerId: str = None
    rightHeatExchangerId: str = None