from Scripts.Utils.containers import ContainerFactory, Container
from Scripts.Utils.port_objects_definition import *
from Scripts.YardPlanner.blocks import Block, BlockFactory
from typing import List, Any, Tuple, Optional
import simpy
from Scripts.YardPlanner.container_placement_rule import ContainerPlacementStrategy
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from matplotlib.animation import FuncAnimation

class YardPlanner:
    """
    The class is for the functionality of Yard Planner in the port simulation.
    """
    def __init__(self, env:simpy.Environment):
        self.env = env
        self.blocks:BlockFactory = BlockFactory()  # List to store blocks
        self.block_list:List[Block] = []  # List to store block instances
        self.container_placement_rule:ContainerPlacementStrategy = ContainerPlacementStrategy()
        self.container_factory:ContainerFactory = ContainerFactory()

    def add_block(self,
                  capacity:int, 
                  block_name:str) -> None:
        """
        This function add the block object to the Block factory.

        @@params capacity: The maximum capacity the block can hold
        @@params block_name: The name of the block to be added
        """
        new_block = self.blocks.add_block(self.env,
                                        capacity=capacity,
                                        name=block_name)
        self.block_list.append(new_block)

    def get_block(self,
                  block_name:str) -> Block:
        """
        This function retrieves the block from the Block factory.

        @@params block_name: The name of the block to be retrieved

        returns: Block Object
        """
        block = self.blocks.get_block(block_name)
        if block is not None:
            return block
        return None
        
    def yard_place_container(self,
                             container:Container,
                             block_name:str,
                             bay:int,
                             cell:int) -> None:
        """
        This function place the container in the yard.

        @@params container: The container Object to be placed
        @@params block_name: The name of the block where the container to be placed.
        @@params bay: The bay number.
        @@params cell: The cell number.
        """
        block = self.get_block(block_name)
        block.store_container(container,
                              container._size,
                              bay,
                              cell)
    
    def update_blocks(self, num, ax, block_spacing):
        ax.clear()
        for block_index, block in enumerate(self.block_list):
            num_bays = block._num_bays
            num_cells = block._num_cells
            matrix = block._matrix

            for bay in range(num_bays):
                for cell in range(num_cells):
                    stack_height = len(matrix[bay][cell])
                    if stack_height > 0:
                        ax.bar3d(bay + block_index * block_spacing, cell, 0, 1, 1, stack_height, color='blue', shade=True)

        ax.set_xlabel('Bays (with block offset)')
        ax.set_ylabel('Cells')
        ax.set_zlabel('Tiers (Stack Height)')
        ax.set_title('3D Visualization of Multiple Blocks')

    def visualize_multiple_blocks_updating(self, block_spacing=10, interval=1000):
        #plt.ion()  # Turn on interactive mode
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        
        ani = FuncAnimation(fig, self.update_blocks, fargs=(ax, block_spacing), interval=interval, cache_frame_data=False)

        #plt.show(block=False)
        plt.show()

    
    # def visualize_multiple_blocks(self, 
    #                               block_spacing:Optional[int]=10):
    #     fig = plt.figure()
    #     ax = fig.add_subplot(111, projection='3d')

    #     for block_index, block in enumerate(self.block_list):
    #         num_bays = block._num_bays
    #         num_cells = block._num_cells
    #         matrix = block._matrix

    #         for bay in range(num_bays):
    #             for cell in range(num_cells):
    #                 stack_height = len(matrix[bay][cell])  # Get the height of the stack
    #                 if stack_height > 0:
    #                     # Plot the stack height as a bar
    #                     # Adding an offset for each block (block_index * block_spacing)
    #                     ax.bar3d(bay + block_index * block_spacing, cell, 0, 1, 1, stack_height, color='blue', shade=True)

    #     ax.set_title('3D Visualization of Multiple Blocks')
    #     ax.set_xlabel('Bays (with block offset)')
    #     ax.set_ylabel('Cells')
    #     ax.set_zlabel('Tiers (Stack Height)')
    #     plt.show()


