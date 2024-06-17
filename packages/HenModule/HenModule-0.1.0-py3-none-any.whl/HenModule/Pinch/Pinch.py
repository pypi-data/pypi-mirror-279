from ..Shared import CapitalCostParameters, Status, isStatusValid, ErrorMessages
from ..Stream import Stream
from ..Utility import Utility
from .CascadeInterval import CascadeInterval
from .AreaInterval import AreaInterval
from .PinchDto import CreatePinchDto

from typing import List, Dict


class Pinch:
    def __init__(self, createPinchDto: CreatePinchDto):
        self.status = Status.VALID

        self.streams = createPinchDto.streams
        self.utilities = createPinchDto.utilities
        self.hrat = createPinchDto.heatRecoveryApproachTemperature

        self.setMultiUtilitiesFractions(createPinchDto.multiUtilitiesFraction)
        self.setNumberOfStreams_and_fillStreamLists()

        self.areaCorrectionNeeded = self.needsAreaCorrection(createPinchDto.standardCapitalCostParameters)
        
        self.fillTemperaturesLists()
        
        self.setPinchPointAndUtilitiyDemands()
        self.calculateMinimumHeatExcahngeUnits()
        
        self.setUtilitiesHeatCapacity()

        self.calculateNonBalancedHotCompositeCurve()
        self.calculateNonBalancedColdCompositeCurve()
        self.calculateHotBalancedCompositeCurve()
        self.calculateColdBalacedCompositeCurve()
        
        self.checkFeasibilityForBalancedCompositeCurves()
        self.setTemperaturesForAllEnthalpyPoints()
        
        self.createAreaIntervals_and_calculateTotalArea()
        self.calculatePhisForAreaCorrection()
        self.correctArea()
        
        self.calculateTotalAnnualizedCost()
        
        
    @isStatusValid
    def setMultiUtilitiesFractions(self, multiUtilitiesFractions: Dict[str, float]):
        if multiUtilitiesFractions == None:
            self.multiUtilitiesFractions = {
                'hu1': 1,
                'cu1': 1
            }
            return

        self.multiUtilitiesFractions = {}

        hotSum: int = 0
        coldSum: int = 0

        for utilityId in multiUtilitiesFractions:
            fraction = multiUtilitiesFractions[utilityId]

            if fraction > 0.00001:
                self.multiUtilitiesFractions[utilityId] = fraction

            if 'h' in utilityId:
                hotSum += fraction

            if 'c' in utilityId:
                coldSum += fraction

        if round(hotSum, 6) != 1:
            self.status = ErrorMessages.MULTI_UTILITIES_FRACTION_SUM.value.replace('-type-', 'hot')
            return

        if round(coldSum, 6) != 1:
            self.status = ErrorMessages.MULTI_UTILITIES_FRACTION_SUM.value.replace('-type-', 'cold')
            return


    @isStatusValid        
    def setNumberOfStreams_and_fillStreamLists(self):
        self.hotStreams: List[Stream] = []
        self.coldStreams: List[Stream] = []
        self.hotUtilities: List[Utility] = []
        self.coldUtilities: List[Utility] = []
        
        self.numHotStreams_noPieces: int = 0
        self.numColdStreams_noPieces: int = 0
        
        streamsNoPieces = {}
        for stream in self.streams:
            streamId = stream.id
            streamType = stream.streamType
            
            if streamId not in streamsNoPieces:
                streamsNoPieces[streamId] = 0

            streamsNoPieces[streamId] += 1

            if 'hot' in streamType:
                self.hotStreams.append(stream)
                
                if streamsNoPieces[streamId] == 1:
                    self.numHotStreams_noPieces += 1
                
            if 'cold' in streamType:
                self.coldStreams.append(stream)

                if streamsNoPieces[streamId] == 1:
                    self.numColdStreams_noPieces += 1

        if self.numHotStreams_noPieces == 0:
            self.status = ErrorMessages.MISSING_STREAM_FROM_TYPE.value.replace('-type-', 'hot')
            return

        if self.numColdStreams_noPieces == 0:
            self.status = ErrorMessages.MISSING_STREAM_FROM_TYPE.value.replace('-type-', 'cold')
            return
                    
        self.numHotStreams = len(self.hotStreams)
        self.numColdStreams = len(self.coldStreams)

        self.numHotUtilities_noPieces: int = 0
        self.numColdUtilities_noPieces: int = 0

        utilitiesNoPieces = {}
        for utility in self.utilities:
            utilityId = utility.id
            utilityType = utility.streamType

            if utilityId not in utilitiesNoPieces:
                utilitiesNoPieces[utilityId] = 0

            utilitiesNoPieces[utilityId] += 1
                
            if 'hot' in utilityType and utilityId in self.multiUtilitiesFractions:
                self.hotUtilities.append(utility)

                if utilitiesNoPieces[utilityId] == 1:
                    self.numHotUtilities_noPieces += 1

            if 'cold' in utilityType and utilityId in self.multiUtilitiesFractions:
                self.coldUtilities.append(utility)

                if utilitiesNoPieces[utilityId] == 1:
                    self.numColdUtilities_noPieces += 1
                    
        self.numHotUtilities = len(self.hotUtilities)
        self.numColdUtilities = len(self.coldUtilities)
        
        if self.numHotUtilities_noPieces == 0:
            self.status = ErrorMessages.MISSING_UTILITY_FROM_TYPE.value.replace('-type-', 'hot')
            return

        if self.numColdUtilities_noPieces == 0:
            self.status = ErrorMessages.MISSING_UTILITY_FROM_TYPE.value.replace('-type-', 'cold')
            return
                    

    @isStatusValid                    
    def needsAreaCorrection(self, capitalCostParameters: CapitalCostParameters):
        self.stdCapitalCostParameters = capitalCostParameters
        self.stdInstalationCost = capitalCostParameters.instalationCost
        self.stdAreaCoefficient = capitalCostParameters.areaCoefficient
        self.stdAreaExponent = capitalCostParameters.areaExponent

        fullList = self.streams[:] + self.utilities[:]

        for stream in fullList:
            if stream.capitalCostParameters.instalationCost != self.stdInstalationCost:
                return True

            if stream.capitalCostParameters.areaCoefficient != self.stdAreaCoefficient:
                return True
            
            if stream.capitalCostParameters.areaExponent != self.stdAreaExponent:
                return True

        return False


    @isStatusValid
    def fillTemperaturesLists(self):
        self.hotTemperatures: List[float] = []
        self.dislocatedHotTemperatures: List[float] = []
        self.balancedHotTemperatures: List[float] = []

        self.coldTemperatures: List[float] = []
        self.dislocatedColdTemperatures: List[float] = []
        self.balancedColdTemperatures: List[float] = []

        self.allTemperatures: List[float] = []
        self.allDislocatedTemperatures: List[float] = []
        
        for stream in self.streams:
            if stream.streamType == 'hot stream':
                self.hotTemperatures.append(stream.supplyTemperature)
                self.hotTemperatures.append(stream.targetTemperature)
                self.dislocatedHotTemperatures.append(stream.supplyTemperature - self.hrat / 2)
                self.dislocatedHotTemperatures.append(stream.targetTemperature - self.hrat / 2)

            elif stream.streamType == 'cold stream':
                self.coldTemperatures.append(stream.supplyTemperature)
                self.coldTemperatures.append(stream.targetTemperature)
                self.dislocatedColdTemperatures.append(stream.supplyTemperature + self.hrat / 2)
                self.dislocatedColdTemperatures.append(stream.targetTemperature + self.hrat / 2)

        self.balancedHotTemperatures.extend(self.hotTemperatures)
        self.balancedColdTemperatures.extend(self.coldTemperatures)

        for utility in self.hotUtilities:
            self.balancedHotTemperatures.append(utility.supplyTemperature)
            self.balancedHotTemperatures.append(utility.targetTemperature)

        for utility in self.coldUtilities:
            self.balancedColdTemperatures.append(utility.supplyTemperature)
            self.balancedColdTemperatures.append(utility.targetTemperature)
               
               
        self.sortAndFilterTemperatureList(self.hotTemperatures) 
        self.sortAndFilterTemperatureList(self.dislocatedHotTemperatures) 
        self.sortAndFilterTemperatureList(self.balancedHotTemperatures)

        self.sortAndFilterTemperatureList(self.coldTemperatures) 
        self.sortAndFilterTemperatureList(self.dislocatedColdTemperatures) 
        self.sortAndFilterTemperatureList(self.balancedColdTemperatures)

        self.allTemperatures = self.hotTemperatures[:]
        self.allTemperatures.extend(self.coldTemperatures[:])
        self.sortAndFilterTemperatureList(self.allTemperatures)

        self.allDislocatedTemperatures = self.dislocatedHotTemperatures[:]
        self.allDislocatedTemperatures.extend(self.dislocatedColdTemperatures[:])
        self.sortAndFilterTemperatureList(self.allDislocatedTemperatures)
        

    @isStatusValid        
    def sortAndFilterTemperatureList(self, temperatureList):
        tempMap = {}

        for temp in temperatureList:
            tempMap[str(temp)] = 1

        temperatureList.clear()
        for temp in tempMap:
            temperatureList.append(float(temp))
            
        temperatureList.sort(reverse=True)
        
        return temperatureList
            

    @isStatusValid            
    def setCascadeIntervals(self, streams, temperaturesList: List[float], hrat):
        cascade: List[CascadeInterval] = []

        for i, temp in enumerate(temperaturesList):
            if i == 0:
                continue
            
            temps = [temperaturesList[i - 1], temp]
            upperBoundTemp = max(temps)
            lowerBoundTemp = min(temps)
            
            cascade.append(CascadeInterval(upperBoundTemp, lowerBoundTemp, streams, hrat))

        return cascade


    @isStatusValid
    def setPinchPointAndUtilitiyDemands(self):
        self.pinchCascade = self.setCascadeIntervals(
            streams=self.streams, 
            temperaturesList=self.allDislocatedTemperatures,
            hrat=self.hrat
        )
        
        enthalpyPoints, temperaturePoints = self.calculateCascade(
            startEnthalpy=0, 
            cascadeIntervals=self.pinchCascade
        )
        
        self.firstCascade = {
            'enthalpyPoints': enthalpyPoints[:],
            'temperaturePoints': temperaturePoints[:]
        }

        minEnthalpy = abs(min(enthalpyPoints))

        enthalpyPoints, temperaturePoints = self.calculateCascade(
            startEnthalpy=minEnthalpy, 
            cascadeIntervals=self.pinchCascade
        )

        self.secondCascade = {
            'enthalpyPoints': enthalpyPoints[:],
            'temperaturePoints': temperaturePoints[:]
        }

        self.hotUtilityDemand = enthalpyPoints[0]
        self.coldUtilityDemand = enthalpyPoints[-1]
        
        pinchPoint = enthalpyPoints.index(min(enthalpyPoints))
        self.pinchTemperature = temperaturePoints[pinchPoint]
        
        self.hotPinchTemperature = self.pinchTemperature + self.hrat / 2
        self.coldPinchTemperature = self.pinchTemperature - self.hrat / 2


    @isStatusValid
    def calculateMinimumHeatExcahngeUnits(self):
        self.minimumUnits = self.numHotStreams_noPieces + self.numColdStreams_noPieces

        if self.hotUtilityDemand > 0.000001:
            self.minimumUnits += self.numHotUtilities_noPieces

        if self.coldUtilityDemand > 0.000001:
            self.minimumUnits += self.numColdUtilities_noPieces

        self.minimumUnits -= 1


    @isStatusValid
    def calculateCascade(self, startEnthalpy: float, cascadeIntervals: List[CascadeInterval], descending=True):
        enthalpyPoints = []
        temperaturePoints = []
        
        getTemperatureMethod = min if descending else max
        getFirstTemperatureMethod = max if descending else min

        for i, interval in enumerate(cascadeIntervals):
            temps = [interval.upperBoundTemperature, interval.lowerBoundTemperature]
            
            if i == 0:
                enthalpyPoints.append(startEnthalpy)
                temperaturePoints.append(getFirstTemperatureMethod(temps))
                
            enthalpyPoints.append(enthalpyPoints[-1] - interval.enthalpyVariation)
            temperaturePoints.append(getTemperatureMethod(temps))

        return enthalpyPoints, temperaturePoints
    

    @isStatusValid
    def setUtilitiesHeatCapacity(self):
        specificEnth = {}

        for utility in self.hotUtilities + self.coldUtilities:
            if utility.id not in specificEnth:
                specificEnth[utility.id] = 0

            specificEnth[utility.id] += utility.specificEnth

        for utility in self.hotUtilities + self.coldUtilities:
            specificEnthFraction = utility.specificEnth / specificEnth[utility.id]
            
            energyDemand = self.hotUtilityDemand if 'hot' in utility.streamType else self.coldUtilityDemand
            
            duty = specificEnthFraction * self.multiUtilitiesFractions[utility.id] * energyDemand
            utility.setDutiesAndHeatCapacity(duty)
            

    @isStatusValid                
    def calculateNonBalancedHotCompositeCurve(self):
        self.hotCascade = self.setCascadeIntervals(
            streams=self.hotStreams,
            temperaturesList=self.hotTemperatures,
            hrat=0,
        )

        enthalpyPoints, temperaturePoints = self.calculateCascade(
            cascadeIntervals=list(reversed(self.hotCascade)),
            startEnthalpy=0,
            descending=False
        )
        
        self.nonBalancedHotCompositeCurve = {
            'enthalpyPoints': enthalpyPoints[:],
            'temperaturePoints': temperaturePoints[:]
        }


    @isStatusValid
    def calculateNonBalancedColdCompositeCurve(self):
        self.coldCascade = self.setCascadeIntervals(
            streams=self.coldStreams,
            temperaturesList=self.coldTemperatures,
            hrat=0,
        )

        enthalpyPoints, temperaturePoints = self.calculateCascade(
            cascadeIntervals=list(reversed(self.coldCascade)),
            startEnthalpy=-self.coldUtilityDemand,
            descending=False
        )

        self.nonBalancedColdCompositeCurve = {
            'enthalpyPoints': [abs(enth) for enth in enthalpyPoints],
            'temperaturePoints': temperaturePoints[:]
        }


    @isStatusValid
    def calculateHotBalancedCompositeCurve(self):
        streams = self.hotStreams + self.hotUtilities
        
        self.balancedHotCascade = self.setCascadeIntervals(
            streams=streams,
            temperaturesList=self.balancedHotTemperatures,
            hrat=0,
        )
        
        enthalpyPoints, temperaturePoints = self.calculateCascade(
            cascadeIntervals=list(reversed(self.balancedHotCascade)),
            startEnthalpy=0,
            descending=False
        )
        
        self.balancedHotCompositeCurve = {
            'enthalpyPoints': enthalpyPoints[:],
            'temperaturePoints': temperaturePoints[:]
        }


    @isStatusValid    
    def calculateColdBalacedCompositeCurve(self):
        streams = self.coldStreams + self.coldUtilities

        self.balancedColdCascade = self.setCascadeIntervals(
            streams=streams,
            temperaturesList=self.balancedColdTemperatures,
            hrat=0,
        )
        
        enthalpyPoints, temperaturePoints = self.calculateCascade(
            cascadeIntervals=list(reversed(self.balancedColdCascade)),
            startEnthalpy=0,
            descending=False
        )
        
        self.balancedColdCompositeCurve = {
            'enthalpyPoints': [abs(enth) for enth in enthalpyPoints],
            'temperaturePoints': temperaturePoints[:]
        }
        
        
    @isStatusValid
    def checkFeasibilityForBalancedCompositeCurves(self):
        greatestHotEnth = self.balancedHotCompositeCurve['enthalpyPoints'][-1]
        greatestColdEnth = self.balancedColdCompositeCurve['enthalpyPoints'][-1]
        
        if abs(greatestHotEnth - greatestColdEnth) > 0.000001:
            self.status = ErrorMessages.CURVES_NOT_BALANCED.value
            return

        leastHotEnth = self.balancedHotCompositeCurve['enthalpyPoints'][0]
        leastColdEnth = self.balancedColdCompositeCurve['enthalpyPoints'][0]

        if leastHotEnth > 0.000001 or leastColdEnth > 0.000001:
            self.status = ErrorMessages.CURVES_NOT_BALANCED.value
            return


    @isStatusValid        
    def setTemperaturesForAllEnthalpyPoints(self):
        hotEnths: List[float] = self.balancedHotCompositeCurve['enthalpyPoints']
        hotTemps: List[float] = self.balancedHotCompositeCurve['temperaturePoints']
        
        coldEnths: List[float] = self.balancedColdCompositeCurve['enthalpyPoints']
        coldTemps: List[float] = self.balancedColdCompositeCurve['temperaturePoints']

        newHotTemps: List[float] = self.interpolateTemperaturesForTheOtherStreamType(
            enths=coldEnths, 
            otherTypeEnths=hotEnths,
            otherTypeTemps=hotTemps,
        )

        newColdTemps: List[float] = self.interpolateTemperaturesForTheOtherStreamType(
            enths=hotEnths,
            otherTypeEnths=coldEnths,
            otherTypeTemps=coldTemps,
        )
        
        allEnths = hotEnths + coldEnths
        allHotTemps = hotTemps + newHotTemps
        allColdTemps = coldTemps + newColdTemps
        
        allEnths.sort(reverse=True)
        allHotTemps.sort(reverse=True)
        allColdTemps.sort(reverse=True)
        
        baseLength = len(allEnths)
        if len(allHotTemps) != baseLength or len(allColdTemps) != baseLength:
            self.status = ErrorMessages.INTERPOLATION_ERROR.value
            return

        self.areaPoints = []
        for i in range(len(allEnths)):
            self.areaPoints.append({
                'enthalpy': allEnths[i],
                'hotTemperature': allHotTemps[i],
                'coldTemperature': allColdTemps[i],
            })
        

    @isStatusValid        
    def interpolateTemperaturesForTheOtherStreamType(
        self, 
        enths: List[float],
        otherTypeEnths: List[float],
        otherTypeTemps: List[float]
    ):
        newOtherTypeTemps = []

        currentOtherTypeIndex = 0
        otherTypeEnth = otherTypeEnths[currentOtherTypeIndex]
        for i in range(len(enths)):
            enth = enths[i]

            while otherTypeEnth < enth and round(abs(otherTypeEnth - enth), 6) > 0:
                currentOtherTypeIndex += 1
                
                try:
                    otherTypeEnth = otherTypeEnths[currentOtherTypeIndex]

                except:
                    self.status = ErrorMessages.INTERPOLATION_ERROR.value
                    return

            upperBoundOtherTypeTemp = otherTypeTemps[currentOtherTypeIndex]
            lowerBoundOtherTypeTemp = otherTypeTemps[currentOtherTypeIndex - 1]

            upperBountOtherTypeEnth = otherTypeEnths[currentOtherTypeIndex]
            lowerBoundOtherTypeEnth = otherTypeEnths[currentOtherTypeIndex - 1]

            newOtherTypeTemp = (enth - lowerBoundOtherTypeEnth)
            newOtherTypeTemp /= (upperBountOtherTypeEnth - lowerBoundOtherTypeEnth)
            newOtherTypeTemp *= (upperBoundOtherTypeTemp - lowerBoundOtherTypeTemp)
            newOtherTypeTemp += lowerBoundOtherTypeTemp
            
            newOtherTypeTemps.append(newOtherTypeTemp)
            
        return newOtherTypeTemps
    

    @isStatusValid    
    def createAreaIntervals_and_calculateTotalArea(self):
        self.areaIntervals: List[AreaInterval] = []
        self.totalArea = 0

        for i in range(len(self.areaPoints)):
            if i == 0:
                continue

            areaInterval = AreaInterval(
                upperBountEnth=self.areaPoints[i - 1]['enthalpy'],
                lowerBoundEnth=self.areaPoints[i]['enthalpy'],
                upperBoundHotTemp=self.areaPoints[i - 1]['hotTemperature'],
                lowerBoundHotTemp=self.areaPoints[i]['hotTemperature'],
                upperBoundColdTemp=self.areaPoints[i - 1]['coldTemperature'],
                lowerBoundColdTemp=self.areaPoints[i]['coldTemperature'],
                streams = self.streams + self.hotUtilities + self.coldUtilities,
            )
            
            if areaInterval.heatLoad == None:
                self.status = ErrorMessages.TEMPERATURE_CROSSOVER.value
                return

            self.areaIntervals.append(areaInterval)
            self.totalArea += self.areaIntervals[-1].area


    @isStatusValid
    def calculatePhi(self, stream):
        phi = (self.stdAreaCoefficient / stream.capitalCostParameters.areaCoefficient) ** (1 / self.stdAreaExponent)
        phi *= (self.totalArea / self.minimumUnits) ** (1 - stream.capitalCostParameters.areaExponent / self.stdAreaExponent)

        return phi


    @isStatusValid
    def calculatePhisForAreaCorrection(self):
        if not self.areaCorrectionNeeded:
            return
        
        for i, stream in enumerate(self.streams):
            self.streams[i].capitalCostParameters.areaCorrectionFactor = self.calculatePhi(stream)

        for i, utility in enumerate(self.hotUtilities):
            self.hotUtilities[i].capitalCostParameters.areaCorrectionFactor = self.calculatePhi(utility)
            
        for i, utility in enumerate(self.coldUtilities):
            self.coldUtilities[i].capitalCostParameters.areaCorrectionFactor = self.calculatePhi(utility)


    @isStatusValid
    def correctArea(self):
        if not self.areaCorrectionNeeded:
            self.correctedArea = self.totalArea
            return

        self.correctedArea = 0
        for areaInterval in self.areaIntervals:
            areaInterval.calculateCorrectedArea()
            self.correctedArea += areaInterval.correctedArea
                        

    @isStatusValid            
    def calculateTotalAnnualizedCost(self):
        self.capitalCosts = (self.correctedArea / self.minimumUnits) ** self.stdAreaExponent
        self.capitalCosts *= self.stdAreaCoefficient
        self.capitalCosts += self.stdInstalationCost
        self.capitalCosts *= self.minimumUnits

        self.operationalCosts = 0
        for utility in self.hotUtilities + self.coldUtilities:
            self.operationalCosts += utility.operationalCost * utility.totalDuty

        self.totalAnnualizedCost = self.capitalCosts + self.operationalCosts