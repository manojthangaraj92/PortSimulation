from typing import Optional, List, Dict, Tuple
from Scripts.Utils.port_objects_definition import *

class Container:
    """
    This class is the base class for a containers in the port terminals.
    """
    counter = 0  # this counter is for generating container ids

    def __init__(self, 
                 container_type:ContainerType, 
                 size:ContainerSize,
                 dwell_time:Optional[float] = 10.0) -> None:
        """
        Constructor for container

        @param container_type: type of the container, eg: laden, empty etc.,
        @param size: size of the container. eg: 20FT, 40FT
        """
        self._container_type = container_type
        self._size = size
        self._dwell_time = dwell_time
        self.container_id = self.generate_id()
        self._block:str = None
        self._bay:int = None
        self._cell:int = None
        self._tier:int = None
        self._from_interface = None
        self._to_interface = None

    def generate_id(self)->str:
        """
        Generate a unique id for the container based on the counter variable.

        @return: A unique id for the container
        """
        Container.counter += 1
        return f'{self._size}-{Container.counter}'
    
    @property
    def block(self) -> str:
        return self._block
    
    @block.setter
    def block(self,
              block_name:str) -> None:
        if not isinstance(block_name, str):
            raise ValueError(f'{block_name} must of type string instead got {type(block_name)}.')
        self._block = block_name

    @property
    def bay(self) -> int:
        return self._bay
    
    @bay.setter
    def bay(self,
              bay:int) -> None:
        if not isinstance(bay, int):
            raise ValueError(f'{bay} must of type integer, instead got {type(bay)}.')
        self._bay = bay

    @property
    def cell(self) -> int:
        return self._cell
    
    @cell.setter
    def cell(self,
              cell:int) -> None:
        if not isinstance(cell, int):
            raise ValueError(f'{cell} must of type integer, instead got {type(cell)}.')
        self._cell = cell

    @property
    def tier(self) -> int:
        return self._tier
    
    @tier.setter
    def tier(self,
              tier:int) -> None:
        if not isinstance(tier, int):
            raise ValueError(f'{tier} must of type integer, instead got {type(tier)}.')
        self._tier = tier

    @property
    def to_interface(self) -> CTInterface:
        return self._to_interface
    
    @to_interface.setter
    def to_interface(self,
              to_interface:CTInterface) -> None:
        if not isinstance(to_interface, CTInterface):
            raise ValueError(f'{to_interface} must of type {CTInterface}, instead got {type(self._to_interface)}.')
        self._to_interface = to_interface

    @property
    def from_interface(self) -> CTInterface:
        return self._from_interface
    
    @from_interface.setter
    def from_interface(self,
              from_interface:CTInterface) -> None:
        if not isinstance(from_interface, CTInterface):
            raise ValueError(f'{from_interface} must of type {CTInterface}, instead got {type(self._from_interface)}.')
        self._from_interface = from_interface

    def __str__(self):
        return f"Container ID: {self.container_id}, Type: {self._container_type}, Size: {self._size}"
    
class ContainerList:
    def __init__(self):
        self._containers:List[Container] = []
        self.size = 0

    @property
    def containers(self) -> List[Container]:
        return self._containers
    
    @containers.setter
    def containers(self,
                   container:Container) -> None:
        if not isinstance(container, Container):
            raise ValueError(f'{container} must of type {Container}, instead got {type(container)}.')
        self._containers.append(container)
        self.size = len(self._containers)

    def remove_container(self,
                         idx:Optional[int]=0) -> Container:
        if not idx:
            container = self._containers.pop()
        else:
            container = self._containers.pop(self.size)
        self.size = len(self._containers)
        return container
    
class ContainerLocationRegistry:
    _instance = None
    location_registry:Dict[str,Tuple[str, int, int, int]] = {}
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ContainerLocationRegistry, cls).__new__(cls)
        return cls._instance

    @classmethod
    def register_container(cls, 
                           container_id:str, 
                           block:str, 
                           bay:int, 
                           cell:int, 
                           tier:int) -> None:
        cls.location_registry[container_id] = (block, bay, cell, tier)

    @classmethod
    def get_container_location(cls, 
                               container_id:str) -> Tuple[str, int, int, int]:
        return cls.location_registry.get(container_id, None)

    @classmethod
    def remove_container(cls, 
                         container_id:str) -> None:
        if container_id in cls.location_registry:
            del cls.location_registry[container_id]