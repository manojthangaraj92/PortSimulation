from Scripts.basic_objects import FilterStore
import simpy
from typing import List, Any, Dict, Tuple, Optional
from Scripts.port_objects_definition import *
from Scripts.containers import Container

class Block(FilterStore):
    """
    This class executes the functionalites of the blocks in the container
    terminal port.
    """
    def __init__(self,
                 env:simpy.Environment,
                 capacity:int,
                 name:str) -> None:
        super().__init__(env, capacity=capacity)
        self.env = env
        self.name = name
        self._num_bays:int = 0
        self._num_cells:int = 0
        self._num_tiers:int = 0
        self._matrix:List[List[List[Optional[str]]]] = []

    @property
    def num_bays(self) -> int:
        return self._num_bays
    
    @num_bays.setter
    def num_bays(self,
                 bays:int) -> None:
        if not isinstance(bays, int):
            raise ValueError("bays must be an integer")
        self._num_bays = bays
        self.update_matrix()

    @property
    def num_cells(self) -> int:
        return self._num_cells
    
    @num_cells.setter
    def num_cells(self,
                 cells:int) -> None:
        if not isinstance(cells, int):
            raise ValueError("cells must be an integer")
        self._num_cells = cells
        self.update_matrix()

    @property
    def num_tiers(self) -> int:
        return self._num_tiers
    
    @num_tiers.setter
    def num_tiers(self,
                 tiers:int) -> None:
        if not isinstance(tiers, int):
            raise ValueError("bays must be an integer")
        self._num_tiers = tiers
        self.update_matrix()

    @property
    def matrix(self) -> List[List[List[Optional[str]]]]:
        return self._matrix
    
    def update_matrix(self) -> None:
        self._matrix = [[[None for _ in range(self._num_tiers)] for _ in range(self._num_cells)] for _ in range(self._num_bays)]
    
    def put(self, 
            container: Container) -> simpy.Event:
        """
        Put a container into the FilterStore.
        This method can be customized to include additional logic.
        """
        print(f"Adding container {container.container_id} to the store.")
        return super().put(container)
    
    def store_container(self, 
                        container_id: Container, 
                        size: ContainerSize, 
                        bay: int, 
                        cell: int) -> bool:
        if size == ContainerSize.TWENTY_FT and bay % 2 != 0:  # 20ft container in odd-numbered bay
            return self._store_in_bay(container_id, bay - 1, cell)  # Adjusting bay number for 0-based index
        elif size == ContainerSize.FORTY_FT:
            lower_bay, upper_bay = self.get_20ft_bays_for_40ft(bay)
            return self._store_in_bay(container_id, lower_bay, cell) and self._store_in_bay(container_id, upper_bay, cell)
        else:
            raise ValueError("Invalid container size")
        
    def get_20ft_bays_for_40ft(self, 
                               bay: int) -> (int, int):
        """Calculate the two 20ft bays for a given 40ft bay."""
        lower_bay = bay * 2 - 3
        upper_bay = bay * 2 - 1
        return lower_bay, upper_bay

    def _store_in_bay(self, 
                      container_id: Container, 
                      bay: int, 
                      cell: int) -> bool:
        """Store a container in a specific bay and cell."""
        for tier in range(len(self.matrix[bay][cell])):
            if self.matrix[bay][cell][tier] is None:
                self.matrix[bay][cell][tier] = container_id
                container_id.bay = bay
                container_id.cell = cell
                container_id.tier = tier
                container_id.block = self
                print(f"Stored container {container_id} in bay {bay}, cell {cell}, tier {tier}.")
                self.env.process(self.put(container_id))
                return True
        return False

    def retrieve_container(self, 
                           container_id):
        """Retrieve a specific container from the block."""
        def container_filter(container):
            return container == container_id
        
        print(f"Retrieving container {container_id} at time {self.env.now}")
        return self.get(filter=container_filter)
    
class YardPlanner:
    def __init__(self):
        self.blocks = []  # List to store blocks

    def add_block(self, 
                  block:Block) -> None:
        self.blocks.append(block)