from openscad_py.complex import Complex
from openscad_py.pirimitive import Primitive
from openscad_py.typing import Numeric
from typing import List, Optional, Tuple, Union


class Color(Primitive):
    """
    Wrapper for the color() object in OpenSCAD.\n
    See also official OpenSCAD `color documentation <https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/Transformations#color>`_.
    
    Examples
    --------
    >>> from openscad_py.transformations import Color
    >>> print(Color("red"))
    color(c="red");
    
    >>> from openscad_py.transformations import Color
    >>> print(Color([1, 0, 0], alpha=0.5))
    color(c=[1, 0, 0], alpha=0.5);
    """
    def __init__(
        self,
        c: Union[List[Numeric], str],
        alpha: Optional[Numeric] = None,
    ) -> None:
        self.c = c
        self.alpha = alpha
        super().__init__("color")
        
    def render_params(self) -> List[str]:
        # Create the list of parameters, including only those that are not None
        params = [
            f"c=\"{self.c}\"" if isinstance(self.c, str) else f"c={self.c}",
            f"alpha={self.alpha}" if self.alpha is not None else None,
        ]
        # Filter out None values
        return [param for param in params if param is not None]


class Minkowski(Primitive):
    """
    Wrapper for the minkowski() object in OpenSCAD.\n
    See also official OpenSCAD `minkowski documentation <https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/Transformations#minkowski>`_.
    
    Examples
    --------
    >>> from openscad_py.transformations import Minkowski
    >>> print(Minkowski())
    minkowski();
    
    >>> from openscad_py.transformations import Minkowski
    >>> print(Minkowski(convexity=10))
    minkowski(convexity=10);
    """
    def __init__(self, convexity: Optional[Numeric] = None) -> None:
        self.convexity = convexity
        super().__init__("minkowski")

    def render_params(self) -> List[str]:
        # Create the list of parameters, including only those that are not None
        params = [
            f"convexity={self.convexity}" if self.convexity is not None else None,
        ]
        # Filter out None values
        return [param for param in params if param is not None]

class Mirror(Primitive):
    """
    Wrapper for the mirror() object in OpenSCAD.\n
    See also official OpenSCAD `mirror documentation <https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/Transformations#mirror>`_.
    
    Examples
    --------
    >>> from openscad_py.transformations import Mirror
    >>> print(Mirror(v=[0, 0, 1]))
    mirror(v=[0, 0, 1]);
    """
    def __init__(self, v: Tuple[Numeric, Numeric, Numeric]) -> None:
        self.v = v
        super().__init__("mirror")
        
    def render_params(self) -> List[str]:
        return [f"v={self.v}"]


class Multmatrix(Primitive):
    """
    Wrapper for the multmatrix() object in OpenSCAD.\n
    See also official OpenSCAD `multmatrix documentation <https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/Transformations#multmatrix>`_.
    
    Examples
    --------
    >>> from openscad_py.transformations import Multmatrix
    >>> print(Multmatrix(m=[[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0]]))
    multmatrix(m=[[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0]]);
    """
    def __init__(
        self,
        m: List[List[Numeric]],
    ) -> None:
        self.m = m
        super().__init__("multmatrix")
        
    def render_params(self) -> List[str]:
        return [f"m={self.m}"]


class Offset(Primitive):
    """
    Wrapper for the offset() object in OpenSCAD.\n
    See also official OpenSCAD `offset documentation <https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/Transformations#offset>`_.
    
    Examples
    --------
    >>> from openscad_py.transformations import Offset
    >>> print(Offset(r=1))
    offset(r=1);
    
    >>> from openscad_py.transformations import Offset
    >>> print(Offset(delta=1, chamfer=True, fn=10, fa=10, fs=10))
    offset(delta=1, chamfer=true, $fn=10, $fa=10, $fs=10);
    """
    def __init__(
        self,
        r: Optional[Numeric] = None,
        delta: Optional[Numeric] = None,
        chamfer: Optional[bool] = None,
        fn: Optional[int] = None,
        fa: Optional[int] = None,
        fs: Optional[int] = None,
    ) -> None:
        self.r = r
        self.delta = delta
        self.chamfer = chamfer
        self.fn = fn
        self.fa = fa
        self.fs = fs
        super().__init__("offset")
        
    def render_params(self) -> List[str]:
        params = [
            f"r={self.r}" if self.r is not None else None,
            f"delta={self.delta}" if self.delta is not None else None,
            f"chamfer={str(self.chamfer).lower()}" if self.chamfer is not None else None,
            f"$fn={self.fn}" if self.fn is not None else None,
            f"$fa={self.fa}" if self.fa is not None else None,
            f"$fs={self.fs}" if self.fs is not None else None,
        ]
        # Filter out None values
        return [param for param in params if param is not None]


class Resize(Primitive):
    """
    Wrapper for the resize() object in OpenSCAD.\n
    See also official OpenSCAD `resize documentation <https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/Transformations#resize>`_.
    
    Examples
    --------
    >>> from openscad_py.transformations import Resize
    >>> print(Resize(newsize=[10, 20, 30]))
    resize(newsize=[10, 20, 30]);
    
    >>> from openscad_py.transformations import Resize
    >>> print(Resize(newsize=[10, 20, 30], auto=True))
    resize(newsize=[10, 20, 30], auto=true);
    """
    def __init__(
        self,
        newsize: Tuple[Numeric, Numeric, Numeric],
        auto: Optional[bool] = None,
    ) -> None:
        self.newsize = newsize
        self.auto = auto
        super().__init__("resize")
        
    def render_params(self) -> List[str]:
        # Create the list of parameters, including only those that are not None
        params = [
            f"newsize={self.newsize}",
            f"auto={str(self.auto).lower()}" if self.auto is not None else None,
        ]
        # Filter out None values
        return [param for param in params if param is not None]


class Rotate(Primitive):
    """
    Wrapper for the rotate() object in OpenSCAD.\n
    See also official OpenSCAD `rotate documentation <https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/Transformations#rotate>`_.
    
    Examples
    --------
    >>> from openscad_py.transformations import Rotate
    >>> print(Rotate(a=90, v=[0, 0, 1]))
    rotate(a=90, v=[0, 0, 1]);
    
    >>> from openscad_py.transformations import Rotate
    >>> print(Rotate(a=(90, 0, 0)))
    rotate(a=(90, 0, 0));
    """
    def __init__(
        self,
        a: Union[Numeric, Tuple[Numeric, Numeric, Numeric]],
        v: Optional[Tuple[Numeric, Numeric, Numeric]] = None,
    ) -> None:
        self.a = a
        self.v = v
        super().__init__("rotate")
        
    def render_params(self) -> List[str]:
        # Create the list of parameters, including only those that are not None
        params = [
            f"a={self.a}",
            f"v={self.v}" if self.v is not None else None,
        ]
        return [param for param in params if param is not None]


class Scale(Primitive):
    """
    Wrapper for the scale() object in OpenSCAD.\n
    See also official OpenSCAD `scale documentation <https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/Transformations#scale>`_.
    
    Examples
    --------
    >>> from openscad_py.transformations import Scale
    >>> print(Scale(v=[10, 20, 30]))
    scale(v=[10, 20, 30]);
    """
    def __init__(self, v: Tuple[Numeric, Numeric, Numeric]) -> None:
        self.v = v
        super().__init__("scale")
        
    def render_params(self) -> List[str]:
        return [f"v={self.v}"]


class Translate(Primitive):
    """
    Wrapper for the translate() object in OpenSCAD.\n
    See also official OpenSCAD `translate documentation <https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/Transformations#translate>`_.

    Examples
    --------
    >>> from openscad_py.transformations import Translate
    >>> print(Translate(v=[10, 20, 30]))
    translate(v=[10, 20, 30]);
    """

    def __init__(self, v: Tuple[Numeric, Numeric, Numeric]) -> None:
        self.v = v
        super().__init__("translate")
        
    def render_params(self) -> List[str]:
        return [f"v={self.v}"]


    class X(Complex):
        """
        Syntax sugar for Translate(v=[...]) with only x translation.

        Examples
        --------
        >>> from openscad_py.transformations import Translate
        >>> print(Translate.X(10))
        translate(v=[10, 0, 0]);
        """

        def __init__(self, x: Numeric) -> None:
            self.x = x
            super().__init__()

        def unpack(self) -> Primitive:
            return Translate(v=[self.x, 0, 0]) << self.children


    class Y(Complex):
        """
        Syntax sugar for Translate(v=[...]) with only y translation.

        Examples
        --------
        >>> from openscad_py.transformations import Translate
        >>> print(Translate.Y(10))
        translate(v=[0, 10, 0]);
        """

        def __init__(self, y: Numeric) -> None:
            self.y = y
            super().__init__()

        def unpack(self) -> Primitive:
            return Translate(v=[0, self.y, 0]) << self.children


    class Z(Complex):
        """
        Syntax sugar for Translate(v=[...]) with only z translation.

        Examples
        --------
        >>> from openscad_py.transformations import Translate
        >>> print(Translate.Z(10))
        translate(v=[0, 0, 10]);
        """

        def __init__(self, z: Numeric) -> None:
            self.z = z
            super().__init__()

        def unpack(self) -> Primitive:
            return Translate(v=[0, 0, self.z]) << self.children
