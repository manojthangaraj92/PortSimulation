from Scripts.Utils.basic_objects import FilterStore
import simpy
from typing import List, Any, Dict, Tuple, Optional
from Scripts.Utils.port_objects_definition import *
from Scripts.Utils.containers import Container, ContainerLocationRegistry
from Scripts.Utils.basic_data_structures import OneIndexedList, Stack

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
        self.location_registry:ContainerLocationRegistry = ContainerLocationRegistry()
        self._matrix:OneIndexedList[OneIndexedList[Stack[Container]]] = None

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
        self._matrix = OneIndexedList([OneIndexedList([Stack(self._num_tiers) for _ in range(self._num_cells)]) for _ in range(self._num_bays * 2 - 1)])

    def put(self, 
            container: Container) -> simpy.Event:
        """
        Put a container into the FilterStore.
        This method can be customized to include additional logic.
        """
        print(f"Adding container {container.container_id} to the store.")
        return super().put(container)
    
    def store_container(self, 
                        container:Container, 
                        size:ContainerSize, 
                        bay:int, 
                        cell:int) -> bool:
        if size == ContainerSize.TWENTY_FT:
            if not self._is_20ft_bay_available(bay, cell):
                return False
        elif size == ContainerSize.FORTY_FT:
            if not self._is_40ft_bay_available(bay, cell):
                return False
        
        # Store container in the specified bay and cell, on the top of the stack
        self._matrix[bay][cell].push(container)
        container._bay = bay
        container._cell = cell
        container._tier = len(self._matrix[bay][cell])
        container.block = self.name
        self.location_registry.register_container(container.container_id, self.name, bay, cell, container.tier)
        #self.location_registry[container.container_id] = (self.name, bay, cell, container.tier)
        #self.env.process(self.put(container))
        self.put(container)
        return True
    
    def _is_20ft_bay_available(self, 
                               bay:int, 
                               cell:int) -> bool:
        # Check adjacent even bays
        if bay > 1 and self._matrix[bay - 1][cell]:  # Check lower even bay
            return False
        if bay < len(self._matrix) and self._matrix[bay + 1][cell]:  # Check upper even bay
            return False
        return True

    def _is_40ft_bay_available(self, 
                               bay:int, 
                               cell:int) -> bool:
        # Check lower and upper odd bays for 40ft container
        lower_bay = bay - 1
        upper_bay = bay + 1
        if lower_bay > 0 and self._matrix[lower_bay][cell]:
            return False
        if upper_bay <= len(self._matrix) and self._matrix[upper_bay][cell]:
            return False
        return True
    
    def retrieve_container(self, 
                           container_id:str, 
                           bay:int, 
                           cell:int) -> Container:
        # Define a filter function based on container ID
        def container_filter(container):
            return container.container_id == container_id

        # Use the get method with the filter function
        #get_event = self.get(container_filter)
        # Process the get event in the SimPy environment
        #yield get_event

        target_stack = self._matrix[bay][cell]

        # Dig for the container
        container_found = False
        while not container_found and target_stack.items:
            current_container = target_stack.pop()
            if current_container.container_id == container_id:
                container_found = True
            else:
                temp_cell = self._find_next_cell_with_space(bay, cell)
                # Allow temporary over-stacking in the temporary cell
                self._matrix[bay][temp_cell].allow_temp_overstack()
                self._matrix[bay][temp_cell].push(current_container)
                current_container._tier = len(self._matrix[bay][temp_cell])
                current_container._bay = self._matrix[bay]
                current_container._cell = self._matrix[bay][temp_cell]
                self.location_registry.register_container(current_container.container_id, self.name, current_container._bay, current_container._cell, current_container._tier)

                # Disallow temporary over-stacking after operation
                self._matrix[bay][temp_cell].disallow_temp_overstack()

        # # Handle case where container is not found
        if not container_found:
        #     # Move containers back from temp_cell to original cell
        #     while self._matrix[bay][temp_cell].items:
        #         target_stack.push(self._matrix[bay][temp_cell].pop())
             return None
        #print(f"Retrieving container {container_id} at time {self.env.now}")
        #return self.get(filter=container_filter)
        return current_container  # or return the container object

    def _find_next_cell_with_space(self, 
                                   bay:int, 
                                   current_cell:int) -> int:
        # Find the next cell with the fewest containers
        min_containers = float('inf')
        next_cell = current_cell
        for cell in range(len(self.matrix[bay])):
            if cell != current_cell and len(self.matrix[bay][cell]) < min_containers:
                min_containers = len(self.matrix[bay][cell])
                next_cell = cell
        return next_cell
    
class BlockFactory:
    _blocks = {}  # Dictionary to store block instances

    @staticmethod
    def get_block(env, 
                  capacity:int, 
                  name:str) -> Block:
        if name not in BlockFactory._blocks:
            BlockFactory._blocks[name] = Block(env, capacity, name)
        return BlockFactory._blocks[name]