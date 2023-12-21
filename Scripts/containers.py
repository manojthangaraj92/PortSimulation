class Container:
    """
    This class is the base class for a containers in the port terminals.
    """
    counter = 0  # this counter is for generating container ids

    def __init__(self, 
                 container_type:str, 
                 size:str) -> None:
        """
        Constructor for container

        @param container_type: type of the container, eg: laden, empty etc.,
        @param size: size of the container. eg: 20FT, 40FT
        """
        self.container_type = container_type
        self.size = size
        self.container_id = self.generate_id()

    def generate_id(self)->str:
        """
        Generate a unique id for the container based on the counter variable.

        @return: A unique id for the container
        """

        Container.counter += 1

        # Generate an ID 
        return f'{self.size}-{Container.counter}'

    def __str__(self):
        return f"Container ID: {self.container_id}, Type: {self.container_type}, Size: {self.size}"