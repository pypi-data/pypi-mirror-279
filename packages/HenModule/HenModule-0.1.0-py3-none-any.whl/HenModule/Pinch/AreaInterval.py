from typing import List
from math import log as ln

from ..Stream import Stream


class AreaInterval:
    def __init__(
        self, 
        upperBountEnth: float, 
        lowerBoundEnth: float,
        upperBoundHotTemp: float,
        lowerBoundHotTemp: float,
        upperBoundColdTemp: float,
        lowerBoundColdTemp: float,
        streams: List[Stream]
    ):
        self.upperBoundHotTemp = upperBoundHotTemp
        self.lowerBoundHotTemp = lowerBoundHotTemp

        self.upperBoundColdTemp = upperBoundColdTemp
        self.lowerBoundColdTemp = lowerBoundColdTemp
        
        self.hotTerminalTempDiff = self.upperBoundHotTemp - self.upperBoundColdTemp
        self.coldTerminalTempDiff = self.lowerBoundHotTemp - self.lowerBoundColdTemp

        self.heatLoad = None

        if self.hotTerminalTempDiff < 0 or self.coldTerminalTempDiff < 0:
            return

        self.heatLoad = upperBountEnth - lowerBoundEnth

        self.presentHotStreams: List[Stream] = []
        self.presentColdStreams: List[Stream] = []
        self.findPresentStreams(streams=streams)

        self.heatExchanged_over_filmCoefficient_hotRatio = 0
        self.heatExchanged_over_filmCoefficient_coldRatio = 0
        self.calculateHeatExchangedByEachStream()
        
        self.calculateArea()

        
    def findPresentStreams(self, streams: List[Stream]):
        for stream in streams:
            if 'hot' in stream.streamType:
                currentStreamList = self.presentHotStreams
                upperBoundTemp = self.upperBoundHotTemp
                lowerBoundTemp = self.lowerBoundHotTemp

            elif 'cold' in stream.streamType:
                currentStreamList = self.presentColdStreams
                upperBoundTemp = self.upperBoundColdTemp
                lowerBoundTemp = self.lowerBoundColdTemp

            streamTemps = [stream.supplyTemperature, stream.targetTemperature]
            streamUpperBoundTemp = max(streamTemps)
            streamLowerBoundTemp = min(streamTemps)

            if self.streamPresent(
                ub=upperBoundTemp,
                lb=lowerBoundTemp,
                stream_ub=streamUpperBoundTemp,
                stream_lb=streamLowerBoundTemp
            ):
                currentStreamList.append(stream)


    def streamPresent(self, ub, lb, stream_ub, stream_lb):
        return stream_lb <= lb and stream_lb <= ub and stream_ub >= ub and stream_ub >= lb


    def calculateHeatExchangedByEachStream(self):
        self.heatExchanged = {}

        for i, hotStream in enumerate(self.presentHotStreams):
            heatExchanged = hotStream.heatCapacity * (self.upperBoundHotTemp - self.lowerBoundHotTemp)
            self.heatExchanged[hotStream.id] = heatExchanged
            
            self.heatExchanged_over_filmCoefficient_hotRatio += heatExchanged / hotStream.filmCoefficient

        for i, coldStream in enumerate(self.presentColdStreams):
            heatExchanged = coldStream.heatCapacity * (self.upperBoundColdTemp - self.lowerBoundColdTemp)
            self.heatExchanged[coldStream.id] = heatExchanged

            self.heatExchanged_over_filmCoefficient_coldRatio += heatExchanged / coldStream.filmCoefficient


    def calculateArea(self):
        self.area = self.heatExchanged_over_filmCoefficient_hotRatio + self.heatExchanged_over_filmCoefficient_coldRatio
        self.lmdt = self.calculateLogarithmicMeanTemperatureDifference()
        self.area /= self.lmdt


    def calculateLogarithmicMeanTemperatureDifference(self):
        hotTerminalTempDiff = self.upperBoundHotTemp - self.upperBoundColdTemp
        coldTerminalTempDiff = self.lowerBoundHotTemp - self.lowerBoundColdTemp

        if hotTerminalTempDiff == coldTerminalTempDiff:
            return hotTerminalTempDiff

        return (hotTerminalTempDiff - coldTerminalTempDiff) / ln(hotTerminalTempDiff / coldTerminalTempDiff)
    
    
    def calculateCorrectedArea(self):
        self.corrected_heatExch_over_filmCoeff_hotRatio = 0
        self.corrected_heatExch_over_filmCoeff_coldRatio = 0

        for stream in self.presentHotStreams:
            heatExchanged = self.heatExchanged[stream.id]
            q_over_h = heatExchanged / stream.capitalCostParameters.areaCorrectionFactor / stream.filmCoefficient
            self.corrected_heatExch_over_filmCoeff_hotRatio += q_over_h

        for stream in self.presentColdStreams:
            heatExchanged = self.heatExchanged[stream.id]
            q_over_h = heatExchanged / stream.capitalCostParameters.areaCorrectionFactor / stream.filmCoefficient
            self.corrected_heatExch_over_filmCoeff_coldRatio += q_over_h
            
        self.correctedArea = self.corrected_heatExch_over_filmCoeff_hotRatio + self.corrected_heatExch_over_filmCoeff_coldRatio
        self.correctedArea /= self.lmdt