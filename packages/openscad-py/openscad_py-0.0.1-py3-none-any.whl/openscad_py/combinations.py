from typing import List
from openscad_py.pirimitive import Primitive


class Union(Primitive):
    """
    Wrapper for the union() object in OpenSCAD.\n
    See also official OpenSCAD `union documentation <https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/CSG_Modelling#union>`_.

    Examples
    --------
    >>> from openscad_py.combinations import Union
    >>> from openscad_py.objects_2d import Circle, Square
    >>> print(Union() << Circle(10) << Square(20))
    union() {
        circle(r=10);
        square(size=[20, 20]);
    }
    """

    def __init__(self) -> None:
        super().__init__("union")

    def render_params(self) -> List[str]:
        return []


class Difference(Primitive):
    """
    Wrapper for the difference() object in OpenSCAD.\n
    See also official OpenSCAD `difference documentation <https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/CSG_Modelling#difference>`_.

    Examples
    --------
    >>> from openscad_py.combinations import Difference
    >>> from openscad_py.objects_2d import Circle, Square
    >>> print(Difference() << Circle(10) << Square(20))
    difference() {
        circle(r=10);
        square(size=[20, 20]);
    }
    """

    def __init__(self) -> None:
        super().__init__("difference")

    def render_params(self) -> List[str]:
        return []


class Intersection(Primitive):
    """
    Wrapper for the intersection() object in OpenSCAD.\n
    See also official OpenSCAD `intersection documentation <https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/CSG_Modelling#intersection>`_.

    Examples
    --------
    >>> from openscad_py.combinations import Intersection
    >>> from openscad_py.objects_2d import Circle, Square
    >>> print(Intersection() << Circle(10) << Square(20))
    intersection() {
        circle(r=10);
        square(size=[20, 20]);
    }
    """

    def __init__(self) -> None:
        super().__init__("intersection")

    def render_params(self) -> List[str]:
        return []
