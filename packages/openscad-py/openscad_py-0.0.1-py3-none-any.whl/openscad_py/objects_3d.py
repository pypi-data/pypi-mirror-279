from openscad_py.pirimitive import Primitive
from openscad_py.typing import Numeric
from typing import List, Optional, Union


class Cube(Primitive):
    """
    Wrapper for the cube() object in OpenSCAD.\n
    See also official OpenSCAD `cube documentation <https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/Primitive_Solids#cube>`_.

    Examples
    --------
    >>> from openscad_py.objects_3d import Cube
    >>> print(Cube(10))
    cube(size=[10, 10, 10]);

    >>> from openscad_py.objects_3d import Cube
    >>> print(Cube([10, 20, 30], center=True))
    cube(size=[10, 20, 30], center=true);
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
            self.size = [size, size, size]
        self.center = center
        super().__init__("cube")

    def render_params(self) -> List[str]:
        # Create the list of parameters, including only those that are not None
        params = [
            f"size={self.size}",
            f"center={str(self.center).lower()}" if self.center is not None else None,
        ]
        # Filter out None values
        return [param for param in params if param is not None]


class Cylinder(Primitive):
    """
    Wrapper for the cylinder() object in OpenSCAD.\n
    See also official OpenSCAD `cylinder documentation <https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/Primitive_Solids#cylinder>`_.

    Examples
    --------
    >>> from openscad_py.objects_3d import Cylinder
    >>> print(Cylinder(10, 20))
    cylinder(h=10, r=20);

    >>> from openscad_py.objects_3d import Cylinder
    >>> print(Cylinder(r1=10, r2=5, h=20, center=True))
    cylinder(h=20, r1=10, r2=5, center=true);

    >>> from openscad_py.objects_3d import Cylinder
    >>> print(Cylinder(d=10, h=20, center=True))
    cylinder(h=20, d=10, center=true);

    >>> from openscad_py.objects_3d import Cylinder
    >>> print(Cylinder(d1=10, d2=5, h=20, center=True))
    cylinder(h=20, d1=10, d2=5, center=true);

    >>> from openscad_py.objects_3d import Cylinder
    >>> print(Cylinder(r=10, h=20, center=True, fn=5, fa=24, fs=4))
    cylinder(h=20, r=10, center=true, $fn=5, $fa=24, $fs=4);
    """

    def __init__(
        self,
        h: Optional[Numeric] = None,
        r: Optional[Numeric] = None,
        r1: Optional[Numeric] = None,
        r2: Optional[Numeric] = None,
        d: Optional[Numeric] = None,
        d1: Optional[Numeric] = None,
        d2: Optional[Numeric] = None,
        center: Optional[bool] = None,
        fn: Optional[Numeric] = None,
        fa: Optional[Numeric] = None,
        fs: Optional[Numeric] = None,
    ) -> None:
        self.r = r
        self.r1 = r1
        self.r2 = r2
        self.d = d
        self.d1 = d1
        self.d2 = d2
        self.h = h
        self.center = center
        self.fn = fn
        self.fa = fa
        self.fs = fs
        super().__init__("cylinder")

    def render_params(self) -> List[str]:
        # Create the list of parameters, including only those that are not None
        params = [
            f"h={self.h}" if self.h is not None else None,
            f"r={self.r}" if self.r is not None else None,
            f"r1={self.r1}" if self.r1 is not None else None,
            f"r2={self.r2}" if self.r2 is not None else None,
            f"d={self.d}" if self.d is not None else None,
            f"d1={self.d1}" if self.d1 is not None else None,
            f"d2={self.d2}" if self.d2 is not None else None,
            f"center={str(self.center).lower()}" if self.center is not None else None,
            f"$fn={self.fn}" if self.fn is not None else None,
            f"$fa={self.fa}" if self.fa is not None else None,
            f"$fs={self.fs}" if self.fs is not None else None,
        ]
        # Filter out None values
        return [param for param in params if param is not None]


class LinearExtrude(Primitive):
    """
    Wrapper for the linear_extrude() object in OpenSCAD.\n
    See also official OpenSCAD `linear_extrude documentation <https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/Transformations#linear_extrude>`_.

    Examples
    --------
    >>> from openscad_py.objects_3d import LinearExtrude
    >>> print(LinearExtrude(height=10))
    linear_extrude(height=10);

    >>> from openscad_py.objects_3d import LinearExtrude
    >>> print(LinearExtrude(height=10, center=True, convexity=10, twist=20, slices=10, scale=[2, 0.5]))
    linear_extrude(height=10, center=true, convexity=10, twist=20, slices=10, scale=[2, 0.5]);
    """

    def __init__(
        self,
        height: Optional[Numeric] = None,
        center: Optional[bool] = None,
        convexity: Optional[Numeric] = None,
        twist: Optional[Numeric] = None,
        slices: Optional[Numeric] = None,
        scale: Optional[Union[Numeric, List[Numeric]]] = None,
        fn: Optional[Numeric] = None,
    ) -> None:
        self.height = height
        self.center = center
        self.convexity = convexity
        self.twist = twist
        self.slices = slices
        self.scale = scale
        self.fn = fn
        super().__init__("linear_extrude")

    def render_params(self) -> List[str]:
        # Create the list of parameters, including only those that are not None
        params = [
            f"height={self.height}" if self.height is not None else None,
            f"center={str(self.center).lower()}" if self.center is not None else None,
            f"convexity={self.convexity}" if self.convexity is not None else None,
            f"twist={self.twist}" if self.twist is not None else None,
            f"slices={self.slices}" if self.slices is not None else None,
            f"scale={self.scale}" if self.scale is not None else None,
            f"$fn={self.fn}" if self.fn is not None else None,
        ]
        # Filter out None values
        return [param for param in params if param is not None]


class Polyhedron(Primitive):
    """
    Wrapper for the polyhedron() object in OpenSCAD.\n
    See also official OpenSCAD `polyhedron documentation <https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/Primitive_Solids#polyhedron>`_.

    Examples
    --------
    >>> from openscad_py.objects_3d import Polyhedron
    >>> print(Polyhedron(points=[[0, 0, 0], [0, 10, 0], [10, 10, 0]], faces=[[0, 1, 2]]))
    polyhedron(points=[[0, 0, 0], [0, 10, 0], [10, 10, 0]], faces=[[0, 1, 2]]);

    >>> from openscad_py.objects_3d import Polyhedron
    >>> print(Polyhedron(
    ...     points=[[0, 0, 0], [0, 10, 0], [10, 10, 0]],
    ...     faces=[[0, 1, 2]],
    ...     convexity=10
    ... ))
    polyhedron(points=[[0, 0, 0], [0, 10, 0], [10, 10, 0]], faces=[[0, 1, 2]], convexity=10);
    """

    def __init__(
        self,
        points: List[List[Numeric]],
        faces: List[List[Numeric]],
        convexity: Optional[Numeric] = None,
    ) -> None:
        self.points = points
        self.faces = faces
        self.convexity = convexity
        super().__init__("polyhedron")

    def render_params(self) -> List[str]:
        # Create the list of parameters, including only those that are not None
        params = [
            f"points={self.points}",
            f"faces={self.faces}",
            f"convexity={self.convexity}" if self.convexity is not None else None,
        ]
        # Filter out None values
        return [param for param in params if param is not None]


class RotateExtrude(Primitive):
    """
    Wrapper for the rotate_extrude() object in OpenSCAD.\n
    See also official OpenSCAD `rotate_extrude documentation <https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/Transformations#rotate_extrude>`_.

    Examples
    --------
    >>> from openscad_py.objects_3d import RotateExtrude
    >>> print(RotateExtrude(angle=45, convexity=10, fa=10, fs=20, fn=5))
    rotate_extrude(angle=45, convexity=10, $fa=10, $fs=20, $fn=5);
    """

    def __init__(
        self,
        angle: Optional[Numeric] = None,
        convexity: Optional[Numeric] = None,
        fa: Optional[Numeric] = None,
        fs: Optional[Numeric] = None,
        fn: Optional[Numeric] = None,
    ) -> None:
        self.angle = angle
        self.convexity = convexity
        self.fa = fa
        self.fs = fs
        self.fn = fn
        super().__init__("rotate_extrude")

    def render_params(self) -> List[str]:
        # Create the list of parameters, including only those that are not None
        params = [
            f"angle={self.angle}" if self.angle is not None else None,
            f"convexity={self.convexity}" if self.convexity is not None else None,
            f"$fa={self.fa}" if self.fa is not None else None,
            f"$fs={self.fs}" if self.fs is not None else None,
            f"$fn={self.fn}" if self.fn is not None else None,
        ]
        # Filter out None values
        return [param for param in params if param is not None]


class Sphere(Primitive):
    """
    Wrapper for the sphere() object in OpenSCAD.\n
    See also official OpenSCAD `sphere documentation <https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/Primitive_Solids#sphere>`_.

    Examples
    --------
    >>> from openscad_py.objects_3d import Sphere
    >>> print(Sphere(10))
    sphere(r=10);

    >>> from openscad_py.objects_3d import Sphere
    >>> print(Sphere(d=10, fn=5, fa=24, fs=4))
    sphere(d=10, $fn=5, $fa=24, $fs=4);
    """

    def __init__(
        self,
        r: Optional[Numeric] = None,
        d: Optional[Numeric] = None,
        fn: Optional[Numeric] = None,
        fa: Optional[Numeric] = None,
        fs: Optional[Numeric] = None,
    ) -> None:
        self.r = r
        self.d = d
        self.fn = fn
        self.fa = fa
        self.fs = fs
        super().__init__("sphere")

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
