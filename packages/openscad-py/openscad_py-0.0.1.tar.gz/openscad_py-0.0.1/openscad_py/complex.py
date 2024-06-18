from abc import abstractmethod
from openscad_py.entity import Entity


class Complex(Entity):
    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def unpack(self) -> Entity:
        pass

    def render(self, indent: int = 0) -> str:
        return self.unpack().render(indent)
