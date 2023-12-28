from typing import List, Dict, Any

class OneIndexedList:
    def __init__(self, 
                 initial_data=None) -> None:
        self.data:List[Any] = initial_data if initial_data is not None else []

    def __getitem__(self, 
                    index:int) -> List[Any]:
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
    def __init__(self) -> None:
        self.items:List[Any] = []

    def push(self, 
             item:Any) -> None:
        self.items.append(item)

    def pop(self) -> Any:
        return self.items.pop() if self.items else None
    
    def __len__(self) -> int:
        return len(self.items)
