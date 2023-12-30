from Scripts.Utils.containers import ContainerFactory, Container
from Scripts.Utils.port_objects_definition import *
from Scripts.YardPlanner.blocks import Block, BlockFactory
from typing import List, Any, Tuple
import simpy
from Scripts.YardPlanner.container_placement_rule import ContainerPlacementStrategy

class YardPlanner:
    def __init__(self, env:simpy.Environment):
        self.env = env
        self.blocks:BlockFactory = BlockFactory()  # List to store blocks
        self.block_list:List[Block] = []  # List to store block instances
        self.container_placement_rule:ContainerPlacementStrategy = ContainerPlacementStrategy()
        self.container_factory:ContainerFactory = ContainerFactory()

    def add_block(self,
                  capacity:int, 
                  block_name:str) -> None:
        new_block = self.blocks.get_block(self.env,
                                        capacity=capacity,
                                        name=block_name)
        self.block_list.append(new_block)
        
    def yard_place_container(self,
                             container:Container,
                             block_name:str,
                             bay:int,
                             cell:int) -> None:
        block = self.blocks.get_block(block_name)
        block.store_container(container,
                              container._size,
                              bay,
                              cell)


