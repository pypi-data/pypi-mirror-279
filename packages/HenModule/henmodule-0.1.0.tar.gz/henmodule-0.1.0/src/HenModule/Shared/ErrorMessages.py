from enum import Enum


class ErrorMessages(Enum):
    MULTI_UTILITIES_FRACTION_SUM = 'sum of -type- utilities fraction is different from 1'
    INVALID_ID = 'invalid id for -id- (the accepted formats are h1, h2, ..., c1, c2, ...)'
    MISSING_STREAM_FROM_TYPE = 'it is required to have -type- streams in the heat exchanger network'
    MISSING_UTILITY_FROM_TYPE = 'it is required to have at least one -type- utility in the heat exchanger network'
    CURVES_NOT_BALANCED = 'it was not possible to get valid balanced composite curves'
    TEMPERATURE_CROSSOVER = 'pinch resulted in a thermodynamic violation (temperature crossover)'
    INTERPOLATION_ERROR = 'the temperatures interpolation resulted in lists with different lengths'
    INVALID_TEMPERATURE_RANGE = 'isothermal streams are not alowed due to mathematical problems. input a 1 temp unit difference'
    INVALID_STREAM_ID = 'id property must follow the format: h1, h2, hi, ..., c1, c2, ci, ...'
    INVALID_UTILITY_ID = 'id property must follow the format: hu1, hu2, hui, ..., cu1, cu2, cui, ...'
    INVALID_PROPERTY_TYPE = '-prop- must be a -proptype-'