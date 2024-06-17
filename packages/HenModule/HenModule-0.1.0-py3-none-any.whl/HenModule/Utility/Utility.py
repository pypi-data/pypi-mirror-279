from ..Stream import Stream
from .UtilityDto import CreateUtilityDto

    
class Utility(Stream):
    def __init__(self, createUtilityDto: CreateUtilityDto):
        super().__init__(createUtilityDto)
        self.operationalCost = createUtilityDto.operationalCost
        self.specificHeatCapacity = createUtilityDto.specificHeatCapacity
        
        self.specificEnth = self.specificHeatCapacity * abs(self.supplyTemperature - self.targetTemperature)


    def setStreamType(self):
        super().setStreamType()
        self.streamType = self.streamType.replace('stream', 'utility')

    
    def calculateTotalDuty(self):
        pass


    def setDutiesAndHeatCapacity(self, energyDemand: float):
        self.remainingDuty = energyDemand
        self.totalDuty = energyDemand

        self.heatCapacity = energyDemand / abs(self.supplyTemperature - self.targetTemperature)