from typing import List, Dict, Any

class OneIndexedList:
    def __init__(self, 
                 initial_data=None) -> None:
        self.data:List[Any] = initial_data if initial_data is not None else []

    def __getitem__(self, 
                    index:int) -> Any:
        return self.data[index - 1]

    def __setitem__(self, 
                    index:int, 
                    value:Any) -> None:
        self.data[index - 1] = value

    def append(self, 
               value:Any) -> None:
        self.data.append(value)

    def __len__(self) -> int:
        return len(self.data)

    def __repr__(self) -> str:
        return self.data.__repr__()

class Stack:
    def __init__(self,
                 max_size:int) -> None:
        self.items:List[Any] = []
        self.max_size:int = max_size
        self.temp_overstack_allowed = False
        
    def push(self, 
             item:Any) -> None:
        if not self.temp_overstack_allowed and len(self.items) >= self.max_size:
            raise Exception("Stack overflow: Attempted to exceed stack max size")
        self.items.append(item)

    def pop(self) -> Any:
        return self.items.pop() if self.items else None
    
    def __len__(self) -> int:
        return len(self.items)
    
    def allow_temp_overstack(self):
        self.temp_overstack_allowed = True

    def disallow_temp_overstack(self):
        self.temp_overstack_allowed = False
