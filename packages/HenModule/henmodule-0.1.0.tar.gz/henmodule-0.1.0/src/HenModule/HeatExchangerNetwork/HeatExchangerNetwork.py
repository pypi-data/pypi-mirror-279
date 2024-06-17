from typing import List, Dict

from ..Stream import Stream
from ..Utility import Utility

from .HeatExchangerNetworkDto import CreateHeatExchangerNetworkDto
from .AddHeatExchangerDto import AddHeatExchangerDto
from .HENHeatExchanger import HENHeatExchanger, CreateHENHeatExchangerDto


class HeatExchangerNetwork:
    def __init__(self, createHeatExchangerNetworkDto: CreateHeatExchangerNetworkDto):
        self.setStreamsAndUtilities(
            createHeatExchangerNetworkDto.streams, 
            createHeatExchangerNetworkDto.utilities
        )
        
        self.heatExchangers: Dict[str, HENHeatExchanger] = {}
        
        
    def setStreamsAndUtilities(self, streams: List[Stream], utilities: List[Utility]):
        self.hotStreams: Dict[str, Stream] = {}
        self.coldStreams: Dict[str, Stream] = {}

        for stream in streams:
            if 'hot' in stream.streamType:
                self.hotStreams[stream.id] = stream

            elif 'cold' in stream.streamType:
                self.coldStreams[stream.id] = stream

        self.hotUtilities: Dict[str, Utility] = {}
        self.coldUtilities: Dict[str, Utility] = {}

        for utility in utilities:
            if 'hot' in utility.streamType:
                self.hotUtilities[utility.id] = utility

            elif 'cold' in utility.streamType:
                self.coldUtilities[utility.id] = utility


    def addHeatExchanger(self, addHeatExchangerDto: AddHeatExchangerDto):
        # TODO: return an invalid status
        if addHeatExchangerDto.id in self.heatExchangers:
            return
            
        hotStream: Stream = self.hotStreams[addHeatExchangerDto.hotStreamId]
        coldStream: Stream = self.coldStreams[addHeatExchangerDto.coldStreamId]

        inletHotTemperature, leftHeatExchanger = self.getInletTemperatureAndReferenceHeatExchanger(
            hotStream, 
            addHeatExchangerDto.leftHeatExchangerId
        )
        
        inletColdTemperature, rightHeatExchanger = self.getInletTemperatureAndReferenceHeatExchanger(
            coldStream, 
            addHeatExchangerDto.rightHeatExchangerId
        )
        
        heatExchanger = HENHeatExchanger(CreateHENHeatExchangerDto(
            id=addHeatExchangerDto.id,
            hotStream=hotStream,
            coldStream=coldStream,
            heatLoad=addHeatExchangerDto.heatLoad,
            inletHotTemperature=inletHotTemperature,
            inletColdTemperature=inletColdTemperature,
            leftHeatExchanger=leftHeatExchanger,
            rightHeatExchanger=rightHeatExchanger
        ))
        
        self.heatExchangers[heatExchanger.id] = heatExchanger


    def getInletTemperatureAndReferenceHeatExchanger(self, stream: Stream, heatExchangerReferenceId: str):
        # TODO: throw error if reference doesnt have the same stream
        hasHeatExchangerReference = heatExchangerReferenceId != None

        if hasHeatExchangerReference:
            heatExchanger: HENHeatExchanger = self.heatExchangers[heatExchangerReferenceId]

            if 'hot' in stream.streamType:
                return heatExchanger.outletHotTemperature, heatExchanger           

            return heatExchanger.outletColdTemperature, heatExchanger

        return stream.supplyTemperature, None


    def getHeatExchangersInfo(self):
        heInfo = {}

        for heId in self.heatExchangers:
            heInfo[heId] = self.heatExchangers[heId].getInfo()

        return heInfo