from enum import Enum, auto

class ContainerSize(Enum):
    TWENTY_FT:str = "20FT"
    FORTY_FT:str = "40FT"

class ContainerType(Enum):
    LADEN:str = "Full"
    EMPTY:str = "Empty"

class ContainerHandling(Enum):
    LOAD:str = "Load"
    DISCHARGE:str  = "Discharge"

class CTInterface(Enum):
    VESSEL_INTERFACE = auto()
    GATE_INTERFACE = auto()
    YARD_INTERFACE = auto()
    RAIL_INTERFACE = auto()