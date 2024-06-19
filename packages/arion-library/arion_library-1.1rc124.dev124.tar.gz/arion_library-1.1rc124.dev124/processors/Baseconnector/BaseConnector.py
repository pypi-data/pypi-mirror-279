from abc import (
    ABC, abstractmethod
)

class BaseConnector(ABC): 
    def __init__(self):
        pass

    def __repr__(self) -> str:
        return super().__repr__()

    def __str__(self) -> str:
        return super().__str__()
