from abc import abstractmethod
from openscad_py.entity import Entity
from typing import List

class Primitive(Entity):
    """
    Used to wrap each openscad primitive
    """
    def __init__(self, render_name: str) -> None:
        super().__init__()
        self.render_name = render_name
        
    @abstractmethod
    def render_params(self) -> List[str]:
        pass
    
    def render(self, indent: int = 0) -> str:
        indent_str = '    ' * indent
        # params
        params_str = ", ".join([f"{param}" for param in self.render_params()])
        # children
        if len(self.children) == 0:
            children_str = ";"
        elif len(self.children) == 1:
            children_str = "\n" + self.children[0].render(indent)
        elif len(self.children) >= 2:
            children_str = " {\n" + "\n".join([child.render(indent + 1) for child in self.children]) + "\n" + indent_str + "}"
            
        return f"{indent_str}{self.render_name}({params_str}){children_str}"