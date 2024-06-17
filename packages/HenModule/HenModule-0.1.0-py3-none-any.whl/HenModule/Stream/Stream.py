from .StreamDto import CreateStreamDto

    
class Stream:
    def __init__(self, createStreamDto: CreateStreamDto):
        self.id: str = createStreamDto.id
        
        self.supplyTemperature: float = createStreamDto.supplyTemperature
        self.targetTemperature: float = createStreamDto.targetTemperature

        self.streamType: str
        self.setStreamType()
        
        self.heatCapacity: float = createStreamDto.heatCapacity
        self.filmCoefficient: float = createStreamDto.filmCoefficient
        
        self.totalDuty: float
        self.remainingDuty: float
        self.calculateTotalDuty()
        
        self.capitalCostParameters = createStreamDto.capitalCostParameters
        
        self.heatExchangers = {}
        
        
    def setStreamType(self):
        if self.supplyTemperature > self.targetTemperature:
            self.streamType = 'hot stream'

        elif self.supplyTemperature < self.targetTemperature:
            self.streamType = 'cold stream'


    def calculateTotalDuty(self):
        self.totalDuty = self.heatCapacity * abs(self.supplyTemperature - self.targetTemperature)
        self.remainingDuty = self.totalDuty


    def addHeatExchanger(self, heatExchanger):
        self.remainingDuty -= heatExchanger.heatLoad
        self.heatExchangers[heatExchanger.id] = heatExchanger

        
    def removeHeatExchanger(self, heatExchanger):
        self.remainingDuty += heatExchanger.heatLoad
        del self.heatExchangers[heatExchanger.id]

       
    def __str__(self) -> str:
        return self.id   

 
    def getInfo(self):
        return {
            'id': self.id,
            'type': self.streamType,
            'supply-temperature': self.supplyTemperature,
            'target-temperature': self.targetTemperature,
            'heat-capacity': self.heatCapacity,
            'film-coefficient': self.filmCoefficient,
            'total-duty': self.totalDuty,
            'remaining-duty': self.remainingDuty,
            'heat-exchangers': self.heatExchangers,
        }