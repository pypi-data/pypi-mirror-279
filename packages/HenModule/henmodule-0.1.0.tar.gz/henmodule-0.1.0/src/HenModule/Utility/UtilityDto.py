from dataclasses import dataclass
from typing import Union

from ..Stream import CreateStreamDto
from ..Shared import CapitalCostParameters, ErrorMessages


@dataclass(kw_only=True)
class CreateUtilityDto(CreateStreamDto):
    heatCapacity: Union[int, float, None] = None
    operationalCost: Union[float, int]
    specificHeatCapacity: Union[float, int] = 1

    def __post_init__(self):
        validationResult = self.__validatePayload()

        if validationResult is not None:
            raise ValueError(validationResult)
        
        
    def __validatePayload(self):
        validTyping = self.__validateTyping()
        if validTyping != True:
            return validTyping
        
        validId = self.__validateId()
        if validId != True:
            return validId

        validTemperatureRange = self.__validateTemperatureRange()
        if validTemperatureRange != True:
            return validTemperatureRange
        
        return None
            
    
    def __validateTyping(self):
        propsTypes = {
            'id': str,
            'supplyTemperature': Union[float, int],
            'targetTemperature': Union[float, int],
            'heatCapacity': Union[int, float, None],
            'filmCoefficient': Union[float, int],
            'capitalCostParameters': CapitalCostParameters,
            'operationalCost': Union[float, int],
            'specificHeatCapacity': Union[float, int]
        }
        
        for prop, propType in propsTypes.items():
            if not isinstance(getattr(self, prop), propType):
                errorMessage = ErrorMessages.INVALID_PROPERTY_TYPE.value
                errorMessage = errorMessage.replace('-proptype-', str(propType))
                errorMessage = errorMessage.replace('-prop-', str(prop))
                return errorMessage

        return True
    

    def __validateId(self):
        validId = True

        if self.id[:2] not in ['hu', 'cu'] or '.' in self.id:
            validId = False

        try:
            a = int(self.id[2:])
        except:
            validId = False

        if not validId:
            return ErrorMessages.INVALID_UTILITY_ID.value

        return True


    def __validateTemperatureRange(self):
        if self.supplyTemperature == self.targetTemperature:
            return ErrorMessages.INVALID_TEMPERATURE_RANGE.value

        return True