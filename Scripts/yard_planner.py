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
                        container: Container, 
                        bay: int, 
                        cell: int) -> bool:
        """Store a container object in the specified bay and cell."""
        container_size = container.size
        # Determine the size (20FT or 40FT) for the container
        size = 20 if container_size == ContainerSize.TWENTY_FT else 40

        # Find the first available tier
        available_tier = None
        for tier in range(self._num_tiers):
            if self._matrix[bay][cell][tier] is None:
                available_tier = tier
                break

        if available_tier is None:
            print(f"No space available in bay {bay}, cell {cell}.")
            return False

        # Check for space for a 40ft container
        if size == 40:
            if bay >= self._num_bays - 1 or self._matrix[bay + 1][cell][available_tier] is not None:
                print(f"Not enough space for a 40ft container in bay {bay}, cell {cell}.")
                return False
            # Occupy the adjacent bay as well
            self._matrix[bay + 1][cell][available_tier] = container.container_id

        # Place the container
        self._matrix[bay][cell][available_tier] = container.container_id
        print(f"Stored container {container.container_id} in bay {bay}, cell {cell}, tier {available_tier}.")
        self.env.process(self.put(container))
        return True


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