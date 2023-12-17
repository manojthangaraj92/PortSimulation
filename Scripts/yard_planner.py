from Scripts.basic_objects import FilterStore
import simpy
from typing import List, Any, Dict, Tuple

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
        self.name = name
        self._num_bays:int = 0
        self._num_cells:int = 0
        self._num_tiers:int = 0

    @property
    def num_bays(self) -> int:
        return self._num_bays
    
    @num_bays.setter
    def num_bays(self,
                 bays:int) -> None:
        if not isinstance(bays, float):
            raise ValueError("bays must be an integer")
        self._prePcat = bays

    @property
    def num_cells(self) -> int:
        return self._num_cells
    
    @num_cells.setter
    def num_cells(self,
                 cells:int) -> None:
        if not isinstance(cells, float):
            raise ValueError("cells must be an integer")
        self._prePcat = cells

    @property
    def num_tiers(self) -> int:
        return self._num_tiers
    
    @num_tiers.setter
    def num_tiers(self,
                 tiers:int) -> None:
        if not isinstance(tiers, float):
            raise ValueError("bays must be an integer")
        self._prePcat = tiers
    
    def store_container(self, 
                        container):
        """Store a container in the block."""
        print(f"Storing container {container} at time {self.env.now}")
        return self.put(container)

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