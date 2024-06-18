from openscad_py.pirimitive import Primitive
from openscad_py.typing import Numeric
from typing import List, Optional, Union


class Circle(Primitive):
    """
    Wrapper for the circle() object in OpenSCAD.\n
    See also official OpenSCAD `circle documentation <https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/Using_the_2D_Subsystem#circle>`_.

    Examples
    --------
    >>> from openscad_py.objects_2d import Circle
    >>> print(Circle(10))
    circle(r=10);

    >>> from openscad_py.objects_2d import Circle
    >>> print(Circle(d=10, fn=5, fa=24, fs=4))
    circle(d=10, $fn=5, $fa=24, $fs=4);
    """

    def __init__(
        self,
        r: Optional[Numeric] = None,
        d: Optional[Numeric] = None,
        fn: Optional[Numeric] = None,
        fa: Optional[Numeric] = None,
        fs: Optional[Numeric] = None,
    ) -> None:
        self.r, self.d, self.fn, self.fa, self.fs = r, d, fn, fa, fs
        self.d = d
        self.fn = fn
        self.fa = fa
        self.fs = fs
        super().__init__("circle")
        
    def render_params(self) -> List[str]:
        # Create the list of parameters, including only those that are not None
        params = [
            f"r={self.r}" if self.r is not None else None,
            f"d={self.d}" if self.d is not None else None,
            f"$fn={self.fn}" if self.fn is not None else None,
            f"$fa={self.fa}" if self.fa is not None else None,
            f"$fs={self.fs}" if self.fs is not None else None,
        ]
        # Filter out None values
        return [param for param in params if param is not None]


class Square(Primitive):
    """
    Wrapper for the square() object in OpenSCAD.\n
    See also official OpenSCAD `square documentation <https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/Using_the_2D_Subsystem#square>`_.

    Examples
    --------
    >>> from openscad_py.objects_2d import Square
    >>> print(Square(10))
    square(size=[10, 10]);

    >>> from openscad_py.objects_2d import Square
    >>> print(Square(size=[10, 20], center=True))
    square(size=[10, 20], center=true);
    """

    def __init__(
        self,
        size: Optional[Union[Numeric, List[Numeric]]] = None,
        center: Optional[bool] = None,
    ) -> None:
        self.size = None
        if isinstance(size, list):
            self.size = size
        else:
            self.size = [size, size]
        self.center = center
        super().__init__("square")
        
    def render_params(self) -> List[str]:
        # Create the list of parameters, including only those that are not None
        params = [
            f"size={self.size}",
            f"center={str(self.center).lower()}" if self.center is not None else None,
        ]
        # Filter out None values
        return [param for param in params if param is not None]


class Polygon(Primitive):
    """
    Wrapper for the polygon() object in OpenSCAD.\n
    See also official OpenSCAD `polygon documentation <https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/Using_the_2D_Subsystem#polygon>`_.

    Examples
    --------
    >>> from openscad_py.objects_2d import Polygon
    >>> print(Polygon([[0, 0], [10, 0], [10, 10], [0, 10]]))
    polygon(points=[[0, 0], [10, 0], [10, 10], [0, 10]]);

    >>> from openscad_py.objects_2d import Polygon
    >>> print(Polygon([[0, 0], [10, 0], [10, 10], [0, 10]], paths=[[0, 1, 2, 3]]))
    polygon(points=[[0, 0], [10, 0], [10, 10], [0, 10]], paths=[[0, 1, 2, 3]]);

    >>> from openscad_py.objects_2d import Polygon
    >>> print(Polygon([[0, 0], [10, 0], [10, 10], [0, 10]], convexity=10))
    polygon(points=[[0, 0], [10, 0], [10, 10], [0, 10]], convexity=10);
    """

    def __init__(
        self,
        points: List[List[Numeric]],
        paths: Optional[List[List[Numeric]]] = None,
        convexity: Optional[Numeric] = None,
    ) -> None:
        self.points = points
        self.paths = paths
        self.convexity = convexity
        super().__init__("polygon")
        
    def render_params(self) -> List[str]:
        # Create the list of parameters, including only those that are not None
        params = [
            f"points={self.points}",
            f"paths={self.paths}" if self.paths is not None else None,
            f"convexity={self.convexity}" if self.convexity is not None else None,
        ]
        # Filter out None values
        return [param for param in params if param is not None]


class Projection(Primitive):
    """
    Wrapper for the projection() object in OpenSCAD.\n
    See also official OpenSCAD `projection documentation <https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/Using_the_2D_Subsystem#projection>`_.

    Examples
    --------
    >>> from openscad_py.objects_2d import Projection
    >>> print(Projection())
    projection();

    >>> from openscad_py.objects_2d import Projection
    >>> print(Projection(cut=True))
    projection(cut=true);
    """

    def __init__(self, cut: Optional[bool] = None) -> None:
        self.cut = cut
        super().__init__("projection")

    def render_params(self) -> List[str]:
        # Create the list of parameters, including only those that are not None
        params = [
            f"cut={str(self.cut).lower()}" if self.cut is not None else None,
        ]
        # Filter out None values
        return [param for param in params if param is not None]

class Text(Primitive):
    """
    Wrapper for the text() object in OpenSCAD.\n
    See also official OpenSCAD `text documentation <https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/Text>`_.

    Examples
    --------
    >>> from openscad_py.objects_2d import Text
    >>> print(Text("Hello, World!"))
    text(text="Hello, World!");

    >>> from openscad_py.objects_2d import Text
    >>> print(Text("Hello, World!", size=10, font="Arial", halign="center", valign="center", spacing=1, direction=0, language="en", script="latin", fn=10))
    text(text="Hello, World!", size=10, font="Arial", halign="center", valign="center", spacing=1, direction=0, language="en", script="latin", $fn=10);
    """

    def __init__(
        self,
        text: str,
        size: Optional[Numeric] = None,
        font: Optional[str] = None,
        halign: Optional[str] = None,
        valign: Optional[str] = None,
        spacing: Optional[Numeric] = None,
        direction: Optional[Numeric] = None,
        language: Optional[str] = None,
        script: Optional[str] = None,
        fn: Optional[Numeric] = None,
    ) -> None:
        self.text = text
        self.size = size
        self.font = font
        self.halign = halign
        self.valign = valign
        self.spacing = spacing
        self.direction = direction
        self.language = language
        self.script = script
        self.fn = fn
        super().__init__("text")

    def render_params(self) -> List[str]:
        # Create the list of parameters, including only those that are not None
        params = [
            f'text="{self.text}"',
            f"size={self.size}" if self.size is not None else None,
            f'font="{self.font}"' if self.font is not None else None,
            f'halign="{self.halign}"' if self.halign is not None else None,
            f'valign="{self.valign}"' if self.valign is not None else None,
            f"spacing={self.spacing}" if self.spacing is not None else None,
            f"direction={self.direction}" if self.direction is not None else None,
            f'language="{self.language}"' if self.language is not None else None,
            f'script="{self.script}"' if self.script is not None else None,
            f"$fn={self.fn}" if self.fn is not None else None,
        ]
        # Filter out None values
        return [param for param in params if param is not None]