#from Scripts.YardPlanner import Block
#from Scripts.Utils import *
from UnitTest import *
import unittest
import simpy

class TestBlock(unittest.TestCase):
    def setUp(self):
        self.env = simpy.Environment()
        self.block = Block(self.env, capacity=100, name="TestBlock")
        self.block.num_bays = 3  # Assuming 3 bays
        self.block.num_cells = 2  # Assuming 2 cells per bay
        self.block.num_tiers = 2  # Assuming 2 tiers per cell

    def test_initialization(self):
        self.assertEqual(self.block.name, "TestBlock")
        self.assertEqual(self.block._num_bays, 3)
        self.assertEqual(self.block._num_cells, 2)
        self.assertEqual(self.block._num_tiers, 2)

    def test_store_and_retrieve_container(self):
        container_20ft = Container("C20FT", ContainerSize.TWENTY_FT)
        self.block.store_container(container_20ft, ContainerSize.TWENTY_FT, 1, 1)
        self.assertEqual(len(self.block.matrix[1][1]), 1)  # Container should be stored

        # Run the environment to process the retrieval
        #retrieve_process 
        retrieved_container = self.block.retrieve_container(container_20ft.container_id, 1, 1)
        # Run the environment for a set amount of time
        #self.env.run(until=100)  # Adjust the time as needed

        # Extract the result from the generator
        #retrieved_container = next(retrieve_process)
        self.assertEqual(retrieved_container, container_20ft)
        # More tests can be added as needed

if __name__ == '__main__':
    unittest.main()
