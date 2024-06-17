from typing import List

from ..Stream import Stream


class CascadeInterval:
    def __init__(self, upperBoundTemp, lowerBoundTemp, streams, hrat):
        self.upperBoundTemperature: float = upperBoundTemp
        self.lowerBoundTemperature: float = lowerBoundTemp
        self.heatCapacity: float = 0
        
        self.presentStreams: List[Stream] = []
        self.findPresentStreams(streams, hrat)
        
        self.calculateIntervalHeatCapacity()
        
        self.temperatureVariation = self.upperBoundTemperature - self.lowerBoundTemperature
        self.enthalpyVariation = self.heatCapacity * self.temperatureVariation
        
        
    def findPresentStreams(self, streams: List[Stream], hrat: float):
        for stream in streams:
            hratSignal = 1 if stream.streamType == 'cold stream' else -1
            temps = [stream.supplyTemperature, stream.targetTemperature]

            streamLowerBoundTemp = min(temps) + hratSignal * hrat / 2
            streamUpperBoundTemp = max(temps) + hratSignal * hrat / 2

            if self.streamPresent(
                self.upperBoundTemperature,
                self.lowerBoundTemperature,
                streamUpperBoundTemp,
                streamLowerBoundTemp,
            ):
                self.presentStreams.append(stream)
                
    
    def streamPresent(self, ub, lb, stream_ub, stream_lb):
        return stream_lb <= lb and stream_lb <= ub and stream_ub >= ub and stream_ub >= lb


    def calculateIntervalHeatCapacity(self):
        for stream in self.presentStreams:
            if 'hot' in stream.streamType:
                self.heatCapacity -= stream.heatCapacity

            elif 'cold' in stream.streamType:
                self.heatCapacity += stream.heatCapacity