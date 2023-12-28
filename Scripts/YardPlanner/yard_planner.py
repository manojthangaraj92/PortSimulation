from Scripts.Utils.containers import Container
from Scripts.Utils.port_objects_definition import *
from YardPlanner.blocks import Block, BlockFactory
from typing import List, Any, Tuple

class YardPlanner:
    def __init__(self):
        self.blocks = []  # List to store blocks

    def add_block(self, 
                  block:Block) -> None:
        self.blocks.append(block)

class ContainerPlacementStrategy:
    @staticmethod
    def find_placement(blocks:List[Block], 
                       container:Container):
        container_size = container._size
        start_bay = 1 if container_size == ContainerSize.TWENTY_FT else 2
        bay_increment = 2

        for block in blocks:
            for bay in range(start_bay, block.num_bays * 2, bay_increment):  # Adjusting for one-indexed list
                for cell in range(1, block._num_cells + 1):
                    if container_size == ContainerSize.TWENTY_FT and block._is_20ft_bay_available(bay, cell):
                        return block, bay, cell
                    elif container_size == ContainerSize.FORTY_FT and block._is_40ft_bay_available(bay, cell):
                        return block, bay, cell
        return None, None, None
