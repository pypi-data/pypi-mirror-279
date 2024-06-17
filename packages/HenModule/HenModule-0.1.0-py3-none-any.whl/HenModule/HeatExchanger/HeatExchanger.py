from math import log

from ..Stream import Stream
from .HeatExchangerDto import CreateHeatExchangerDto


class HeatExchanger:
    def __init__(self, createHeatExchangetDto: CreateHeatExchangerDto):
        self.id: int = createHeatExchangetDto.id
        
        self.hotStream: Stream = createHeatExchangetDto.hotStream
        self.coldStream: Stream = createHeatExchangetDto.coldStream

        if createHeatExchangetDto.heatLoad == 'max':
            self.setMaximumHeatLoad()
        
        else:
            self.heatLoad: float = createHeatExchangetDto.heatLoad
        
        self.setInletAndCalculateOutletTemperatures(
            createHeatExchangetDto.inletHotTemperature,
            createHeatExchangetDto.inletColdTemperature,
        )

        self.heatExchangeGlobalCoefficient: float
        self.calculateHeatExchangeGlobalCoefficient()

        self.logarithmicMeanTemperatureDifference: float
        self.calculateLogarithmicMeanTemperatureDifference()

        self.heatExchangeArea: float
        self.calculateHeatExchangeArea()
        
        # TODO: fix this (boolean to special HE or areaCorrection)
        self.capitalCostParameters = createHeatExchangetDto.hotStream.capitalCostParameters
        self.capitalCost: float
        self.calculateCapitalCost()
    
    
    def setMaximumHeatLoad(self):
        hotStreamDuty = self.hotStream.remainingDuty
        coldStreamDuty = self.coldStream.remainingDuty

        self.heatLoad = min(hotStreamDuty, coldStreamDuty)

    
    def setInletAndCalculateOutletTemperatures(self, inletHotTemp: float, inletColdTemp: float):
        self.inletHotTemperature = inletHotTemp
        self.inletColdTemperature = inletColdTemp

        self.outletHotTemperature = self.inletHotTemperature
        self.outletHotTemperature -= self.heatLoad / self.hotStream.heatCapacity

        self.outletColdTemperature = self.inletColdTemperature
        self.outletColdTemperature += self.heatLoad / self.coldStream.heatCapacity


    def calculateHeatExchangeGlobalCoefficient(self):
        self.heatExchangeGlobalCoefficient = 1 / self.hotStream.filmCoefficient        
        self.heatExchangeGlobalCoefficient += 1 / self.coldStream.filmCoefficient
        self.heatExchangeGlobalCoefficient **= -1

        
    def calculateLogarithmicMeanTemperatureDifference(self):
        hotTerminalTemperatureDifference: float = self.inletHotTemperature
        hotTerminalTemperatureDifference -= self.outletColdTemperature

        coldTerminalTemperatureDifference: float = self.outletHotTemperature
        coldTerminalTemperatureDifference -= self.inletColdTemperature

        if hotTerminalTemperatureDifference != coldTerminalTemperatureDifference:
            self.logarithmicMeanTemperatureDifference = hotTerminalTemperatureDifference
            self.logarithmicMeanTemperatureDifference -= coldTerminalTemperatureDifference
            denominator: float = log(hotTerminalTemperatureDifference / coldTerminalTemperatureDifference)
            self.logarithmicMeanTemperatureDifference /= denominator

        else:
            self.logarithmicMeanTemperatureDifference = hotTerminalTemperatureDifference


    def calculateHeatExchangeArea(self):
        self.heatExchangeArea = self.heatLoad
        self.heatExchangeArea /= self.heatExchangeGlobalCoefficient
        self.heatExchangeArea /= self.logarithmicMeanTemperatureDifference

        
    def calculateCapitalCost(self):
        self.capitalCost = self.capitalCostParameters.areaCoefficient
        self.capitalCost *= self.heatExchangeArea ** self.capitalCostParameters.areaExponent
        self.capitalCost += self.capitalCostParameters.instalationCost

        
    def __str__(self) -> str:
        return 'e' + str(self.id)    
        
        
    def getInfo(self):
        return {
            'id': self.id,
            'Hot Stream': self.hotStream.id,
            'Cold Stream': self.coldStream.id,
            'Heat Load': self.heatLoad,

            'Inlet Hot Temperature': self.inletHotTemperature,
            'Inlet Cold Temperature': self.inletColdTemperature,
            'Outlet Hot Temperature': self.outletHotTemperature,
            'Outlet Cold Temperature': self.outletColdTemperature,
 
            'Heat Exchange Global Coefficient': self.heatExchangeGlobalCoefficient,
            'Logarithmic Mean Temperature Difference': self.logarithmicMeanTemperatureDifference,
            'Heat Exchange Area': self.heatExchangeArea,
            'Capital Cost': self.capitalCost
        }