from dataclasses import dataclass
from typing import Optional

from ..HeatExchanger import HeatExchanger, CreateHeatExchangerDto


@dataclass(kw_only=True)
class CreateHENHeatExchangerDto(CreateHeatExchangerDto):
    leftHeatExchanger: Optional['HENHeatExchanger'] = None
    rightHeatExchanger: Optional['HENHeatExchanger'] = None
    
    
class HENHeatExchanger(HeatExchanger):
    def __init__(self, createHeatExchangerDto: CreateHENHeatExchangerDto):
        self.leftHeatExchanger = createHeatExchangerDto.leftHeatExchanger
        self.rightHeatExchanger = createHeatExchangerDto.rightHeatExchanger
        
        dto_dict = createHeatExchangerDto.__dict__.copy()
        dto_dict.pop('leftHeatExchanger')
        dto_dict.pop('rightHeatExchanger')
        
        filtered_dto = CreateHeatExchangerDto(**dto_dict)
        super().__init__(filtered_dto)
        
        self.updateHotStreamsHeatExchangers()
        self.updateColdStreamsHeatExchangers()
        
        
    def updateHotStreamsHeatExchangers(self):
        """
            when a HE is added to the left or right of an existing one,
            the existing one must point to the newly added HE
            
            particularly, if there is a HE on the right of the newly added one,
            its properties must be recalculated
            
            this must be recursive since the update props of the right HE will
            affect the props of its right HE and so on...
        """
        
        if self.leftHeatExchanger:
            self.leftHeatExchanger.rightHeatExchanger = self

        if self.rightHeatExchanger:
            self.rightHeatExchanger.leftHeatExchanger = self
            self.rightHeatExchanger.recalculateProps(
                inletHotTemp=self.outletHotTemperature,
                inletColdTemp=self.rightHeatExchanger.inletColdTemperature,
                updatingType='hot',
            )


    def updateColdStreamsHeatExchangers(self):
        if self.rightHeatExchanger:
            self.rightHeatExchanger.leftHeatExchanger = self

        if self.leftHeatExchanger:
            self.leftHeatExchanger.rightHeatExchanger = self
            self.leftHeatExchanger.recalculateProps(
                inletHotTemp=self.leftHeatExchanger.inletHotTemperature,
                inletColdTemp=self.outletColdTemperature,
                updatingType='cold',
            )
            
            
    def recalculateProps(self, inletHotTemp: float, inletColdTemp: float, updatingType: str):
        self.setInletAndCalculateOutletTemperatures(inletHotTemp, inletColdTemp)
        self.calculateLogarithmicMeanTemperatureDifference()
        self.calculateHeatExchangeArea()
        self.calculateCapitalCost()
        
        if 'hot' in updatingType and self.rightHeatExchanger:
            self.rightHeatExchanger.recalculateProps(
                inletHotTemp=self.outletHotTemperature,
                inletColdTemp=self.rightHeatExchanger.inletColdTemperature,
                updatingType='hot',
            )
            
        if 'cold' in updatingType and self.leftHeatExchanger:
            self.leftHeatExchanger.recalculateProps(
                inletHotTemp=self.leftHeatExchanger.inletHotTemperature,
                inletColdTemp=self.outletColdTemperature,
                updatingType='cold',
            )
        
        
    def getInfo(self):
        currentInfo = super().getInfo()

        leftId = None
        rightId = None

        if self.leftHeatExchanger:
            leftId = self.leftHeatExchanger.id

        if self.rightHeatExchanger:
            rightId = self.rightHeatExchanger.id
            
        currentInfo['leftHeatExchangerId'] = leftId
        currentInfo['rightHeatExchangerId'] = rightId

        return currentInfo