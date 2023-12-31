import scipy.stats as stats
from typing import Any, Dict, Union
from scipy.stats import rv_continuous

class RandomTimeGenerator:
    def __init__(self, 
                 distribution: str = 'norm', 
                 **params: Any) -> None:
        """
        Initialize the random time generator with a specific distribution and parameters.

        Args:
            distribution (str): The type of distribution to use ('normal', 'uniform', 'exponential', etc.).
            **params: Parameters required for the specified distribution (e.g., mean and std for normal distribution).
        """
        self.distribution:str = distribution
        self.params:Any = params
        self.distribution_function:rv_continuous = getattr(stats, distribution)

    def generate(self, 
                 size: int = 1) -> Union[float, list]:
        """
        Generate random times based on the specified distribution and parameters.

        Args:
            size (int): The number of random times to generate.

        Returns:
            Union[float, list]: A single generated random time if size is 1, otherwise a list of generated random times.
        """
        return self.distribution_function.rvs(size=size, **self.params)