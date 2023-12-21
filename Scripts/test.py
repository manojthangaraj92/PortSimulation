class ContainerBlock:
    def __init__(self, num_bays, num_cells, num_tiers):
        self.matrix = [[[None for _ in range(num_tiers)] for _ in range(num_cells)] for _ in range(num_bays)]
        self.num_tiers = num_tiers

    def store_container_specific(self, container_id, container_size, bay, cell):
        """Store a container in a specified bay and cell if possible."""
        # Check if the bay and cell can accommodate the container size
        if container_size == 40 and bay >= len(self.matrix) - 1:
            print("No space available for a 40ft container in the last bay.")
            return False

        # Find the first empty tier in the specified bay and cell
        for tier in range(self.num_tiers):
            if self.matrix[bay][cell][tier] is None:
                if container_size == 40 and self.matrix[bay + 1][cell][tier] is not None:
                    continue  # Skip if adjacent bay for 40ft container is not empty
                # Store the container
                self.matrix[bay][cell][tier] = container_id
                if container_size == 40:
                    # Mark the adjacent bay as occupied by the same 40ft container
                    self.matrix[bay + 1][cell][tier] = container_id
                print(f"Stored {container_id} in bay {bay}, cell {cell}, tier {tier}")
                return True
        print("No space available at the specified location.")
        return False

    def total_TEUs(self):
        """Calculate the total TEUs in the block."""
        total_teu = 0
        seen_containers = set()  # To handle 40ft containers spanning two bays
        for bay in self.matrix:
            for cell in bay:
                for tier in cell:
                    if tier and tier not in seen_containers:
                        seen_containers.add(tier)
                        if "-40" in tier:
                            total_teu += 2
                        else:
                            total_teu += 1
        return total_teu
    
    def total_containers(self):
        """Count the actual number of containers in the block."""
        seen_containers = set()  # Keep track of counted containers
        total_containers = 0

        for bay_index, bay in enumerate(self.matrix):
            for cell in bay:
                for tier_index, tier in enumerate(cell):
                    if tier and tier not in seen_containers:
                        seen_containers.add(tier)
                        # Check if the container spans two bays (40ft container)
                        if bay_index < len(self.matrix) - 1 and tier == self.matrix[bay_index + 1][cell.index(tier)][tier_index]:
                            seen_containers.add(self.matrix[bay_index + 1][cell.index(tier)][tier_index])
                        total_containers += 1

        return total_containers
    
    def retrieve_container(self, container_id):
        """Retrieve a container from the block given its ID."""
        for bay_index, bay in enumerate(self.matrix):
            for cell_index, cell in enumerate(bay):
                for tier_index, tier in enumerate(cell):
                    if tier == container_id:
                        # Container found, remove it
                        self.matrix[bay_index][cell_index][tier_index] = None
                        print(f"Removed container {container_id} from bay {bay_index}, cell {cell_index}, tier {tier_index}")

                        # Check and remove from adjacent bay if it's a 40ft container
                        if bay_index < len(self.matrix) - 1 and self.matrix[bay_index + 1][cell_index][tier_index] == container_id:
                            self.matrix[bay_index + 1][cell_index][tier_index] = None
                            print(f"Also removed container {container_id} from adjacent bay {bay_index + 1}")

                        return True

        print(f"Container {container_id} not found in the block.")
        return False

# Example Usage
block = ContainerBlock(num_bays=10, num_cells=2, num_tiers=3)
block.store_container_specific("C1-20", 20, 2, 1)
block.store_container_specific("C2-40", 40, 3, 1)
block.display()
