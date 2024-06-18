from openscad_py.combinations import Union
from openscad_py.complex import Complex
from openscad_py.pirimitive import Primitive
from openscad_py.typing import Numeric
from typing import List, Optional


class Import(Primitive):
    """
    Wrapper for the import() object in OpenSCAD.\n
    See also official OpenSCAD `import documentation <https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/Import>`_.

    Examples
    --------
    >>> from openscad_py.others import Import
    >>> print(Import("example.stl"))
    import("example.stl");

    >>> from openscad_py.others import Import
    >>> print(Import("example.stl", convexity=10))
    import("example.stl", convexity=10);
    """

    def __init__(
        self,
        file: str,
        convexity: Optional[Numeric] = None,
    ) -> None:
        self.file = file
        self.convexity = convexity
        super().__init__("import")
        
    def render_params(self) -> List[str]:
        # Create the list of parameters, including only those that are not None
        params = [
            f'"{self.file}"',
            f"convexity={self.convexity}" if self.convexity is not None else None,
        ]
        # Filter out None values
        return [param for param in params if param is not None]


class Render(Primitive):
    """
    Wrapper for the render() object in OpenSCAD.\n
    See also official OpenSCAD `render documentation <https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/Other_Language_Features#render>`_.

    Examples
    --------
    >>> from openscad_py.others import Render
    >>> print(Render(convexity=10))
    render(convexity=10);
    """

    def __init__(
        self,
        convexity: Optional[Numeric] = None,
    ) -> None:
        self.convexity = convexity
        super().__init__("render")

    def render_params(self) -> List[str]:
        # Create the list of parameters, including only those that are not None
        params = [
            f"convexity={self.convexity}" if self.convexity is not None else None,
        ]
        # Filter out None values
        return [param for param in params if param is not None]

class Surface(Primitive):
    """
    Wrapper for the surface() object in OpenSCAD.\n
    See also official OpenSCAD `surface documentation <https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/Other_Language_Features#surface>`_.

    Examples
    --------
    >>> from openscad_py.others import Surface
    >>> print(Surface(file="example.dat"))
    surface(file="example.dat");

    >>> from openscad_py.others import Surface
    >>> print(Surface(file="example.dat", center=True, convexity=10))
    surface(file="example.dat", center=true, convexity=10);
    """

    def __init__(
        self,
        file: str,
        center: Optional[bool] = None,
        convexity: Optional[Numeric] = None,
    ) -> None:
        self.file = file
        self.center = center
        self.convexity = convexity
        super().__init__("surface")
        
    def render_params(self) -> List[str]:
        # Create the list of parameters, including only those that are not None
        params = [
            f'file="{self.file}"',
            f"center={str(self.center).lower()}" if self.center is not None else None,
            f"convexity={self.convexity}" if self.convexity is not None else None,
        ]
        # Filter out None values
        return [param for param in params if param is not None]


class Tag(Complex):
    """
    In the object tree, it tags a group of objects with a name.\n
    It is especially useful when you want to select a group of objects by name and then apply processing to them.

    Examples
    --------
    >>> from openscad_py.others import Tag
    >>> from openscad_py.objects_2d import Circle, Square
    >>> print(Tag("example") << Circle(10) << Square(20))
    union() {
        circle(r=10);
        square(size=[20, 20]);
    }
    
    >>> from openscad_py.others import Tag
    >>> from openscad_py.objects_2d import Circle
    >>> print(Tag("example") << Circle(10))
    circle(r=10);
    """

    def __init__(
        self,
        name: str
    ) -> None:
        self.name = name
        super().__init__()
        
    def unpack(self) -> Primitive:
        # if there is only one child, return it
        if len(self.children) == 1:
            return self.children[0]
        # if there are more than one children, return a union of them
        if len(self.children) > 1:
            result = Union()
            for child in self.children:
                result <<= child
            return result
        # if there are no children, return an empty union
        return Union()