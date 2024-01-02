from typing import List, Dict, Any, Optional, Union

class StatsCollector:
    def __init__(self):
        self.data:Dict[str,List[Union[int, float]]] = {}

    def add_item(self, 
                 key, 
                 value):
        """ Add a value to a list under the given key in the dictionary. """
        if key not in self.data:
            self.data[key] = []
        self.data[key].append(value)

    def retrieve_items(self, 
                       key):
        """ Retrieve all values for a given key. """
        return self.data.get(key, [])

    def total(self, 
              key):
        """ Calculate the total of the values for a given key. """
        return sum(self.data.get(key, []))

    def min(self, 
            key):
        """ Find the minimum value for a given key. """
        return min(self.data.get(key, []), default=None)

    def max(self, 
            key):
        """ Find the maximum value for a given key. """
        return max(self.data.get(key, []), default=None)

    def average(self, 
                key):
        """ Calculate the average of the values for a given key. """
        values = self.data.get(key, [])
        return sum(values) / len(values) if values else None
