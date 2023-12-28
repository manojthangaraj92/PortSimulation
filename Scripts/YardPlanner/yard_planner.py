from Scripts.Utils.containers import Container
from Scripts.Utils.port_objects_definition import *
from YardPlanner.blocks import Block, BlockFactory
from typing import List, Any, Tuple
import simpy
from YardPlanner.container_placement_rule import ContainerPlacementStrategy

class YardPlanner:
    def __init__(self, env:simpy.Environment):
        self.env = env
        self.blocks:BlockFactory = BlockFactory()  # List to store blocks
        self.container_placement_rule:ContainerPlacementStrategy = ContainerPlacementStrategy()

    def add_block(self,
                  capacity:int, 
                  block_name:str) -> None:
        self.blocks.get_block(self.env,
                              capacity=capacity,
                              name=block_name)


