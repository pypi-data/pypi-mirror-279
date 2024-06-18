from inspect import signature
from typing import Callable, List, Self, Tuple, Union


class EntitySelector:

    def __init__(self, entities_with_paths: List[Tuple[Self, List[Self]]]):
        self.entities_with_paths = entities_with_paths

    def __iter__(self):
        return iter(self.entities_with_paths)

    def __and__(self, value: Union[Self, Callable[[Self, List[Self]], Self]]):
        """
        Examples
        --------
        >>> from openscad_py.objects_2d import Circle, Square
        >>> from openscad_py.transformations import Translate
        >>> example = (Square(40)
        ...     | Circle(5)
        ...     | Translate.X(40) << Circle(7)
        ...     | Translate.Y(40) << Circle(9)
        ...     | Translate([40, 40, 0]) << Circle(11))
        >>> example[lambda x: isinstance(x, Circle)] &= Square(12, center=True)
        >>> example
        union() {
            square(size=[40, 40]);
            intersection() {
                circle(r=5);
                square(size=[12, 12], center=true);
            }
            translate(v=[40, 0, 0])
            intersection() {
                circle(r=7);
                square(size=[12, 12], center=true);
            }
            translate(v=[0, 40, 0])
            intersection() {
                circle(r=9);
                square(size=[12, 12], center=true);
            }
            translate(v=[40, 40, 0])
            intersection() {
                circle(r=11);
                square(size=[12, 12], center=true);
            }
        }
        >>> example = (Square(40)
        ...     | Circle(5)
        ...     | Translate.X(40) << Circle(7)
        ...     | Translate.Y(40) << Circle(9)
        ...     | Translate([40, 40, 0]) << Circle(11))
        >>> example[lambda x: isinstance(x, Circle)] &= lambda x: Square(x.r * 2 * 0.9, center=True)
        >>> example
        union() {
            square(size=[40, 40]);
            intersection() {
                circle(r=5);
                square(size=[9.0, 9.0], center=true);
            }
            translate(v=[40, 0, 0])
            intersection() {
                circle(r=7);
                square(size=[12.6, 12.6], center=true);
            }
            translate(v=[0, 40, 0])
            intersection() {
                circle(r=9);
                square(size=[16.2, 16.2], center=true);
            }
            translate(v=[40, 40, 0])
            intersection() {
                circle(r=11);
                square(size=[19.8, 19.8], center=true);
            }
        }
        """
        return self.__apply_operator("__and__", value)

    def __or__(self, value: Union[Self, Callable[[Self, List[Self]], Self]]):
        """
        Examples
        --------
        >>> from openscad_py.objects_2d import Circle, Square
        >>> from openscad_py.objects_3d import Cylinder
        >>> from openscad_py.transformations import Translate
        >>> example = (Square(40)
        ...     | Circle(5)
        ...     | Translate.X(40) << Circle(7)
        ...     | Translate.Y(40) << Circle(9)
        ...     | Translate([40, 40, 0]) << Circle(11))
        >>> example[lambda x: isinstance(x, Circle)] |= Cylinder(h=5, r=4)
        >>> example
        union() {
            square(size=[40, 40]);
            union() {
                circle(r=5);
                cylinder(h=5, r=4);
            }
            translate(v=[40, 0, 0])
            union() {
                circle(r=7);
                cylinder(h=5, r=4);
            }
            translate(v=[0, 40, 0])
            union() {
                circle(r=9);
                cylinder(h=5, r=4);
            }
            translate(v=[40, 40, 0])
            union() {
                circle(r=11);
                cylinder(h=5, r=4);
            }
        }
        >>> example = (Square(40)
        ...     | Circle(5)
        ...     | Translate.X(40) << Circle(7)
        ...     | Translate.Y(40) << Circle(9)
        ...     | Translate([40, 40, 0]) << Circle(11))
        >>> example[lambda x: isinstance(x, Circle)] |= lambda x: Cylinder(h=5, r=x.r - 1)
        >>> example
        union() {
            square(size=[40, 40]);
            union() {
                circle(r=5);
                cylinder(h=5, r=4);
            }
            translate(v=[40, 0, 0])
            union() {
                circle(r=7);
                cylinder(h=5, r=6);
            }
            translate(v=[0, 40, 0])
            union() {
                circle(r=9);
                cylinder(h=5, r=8);
            }
            translate(v=[40, 40, 0])
            union() {
                circle(r=11);
                cylinder(h=5, r=10);
            }
        }
        """
        return self.__apply_operator("__or__", value)

    def __sub__(self, value: Union[Self, Callable[[Self, List[Self]], Self]]):
        """
        Examples
        --------
        >>> from openscad_py.objects_2d import Circle, Square
        >>> from openscad_py.transformations import Translate
        >>> example = (Square(40)
        ...     | Circle(5)
        ...     | Translate.X(40) << Circle(7)
        ...     | Translate.Y(40) << Circle(9)
        ...     | Translate([40, 40, 0]) << Circle(11))
        >>> example[lambda x: isinstance(x, Circle)] -= Circle(4)
        >>> example
        union() {
            square(size=[40, 40]);
            difference() {
                circle(r=5);
                circle(r=4);
            }
            translate(v=[40, 0, 0])
            difference() {
                circle(r=7);
                circle(r=4);
            }
            translate(v=[0, 40, 0])
            difference() {
                circle(r=9);
                circle(r=4);
            }
            translate(v=[40, 40, 0])
            difference() {
                circle(r=11);
                circle(r=4);
            }
        }
        >>> example = (Square(40)
        ...     | Circle(5)
        ...     | Translate.X(40) << Circle(7)
        ...     | Translate.Y(40) << Circle(9)
        ...     | Translate([40, 40, 0]) << Circle(11))
        >>> example[lambda x: isinstance(x, Circle)] -= lambda x: Circle(x.r - 1)
        >>> example
        union() {
            square(size=[40, 40]);
            difference() {
                circle(r=5);
                circle(r=4);
            }
            translate(v=[40, 0, 0])
            difference() {
                circle(r=7);
                circle(r=6);
            }
            translate(v=[0, 40, 0])
            difference() {
                circle(r=9);
                circle(r=8);
            }
            translate(v=[40, 40, 0])
            difference() {
                circle(r=11);
                circle(r=10);
            }
        }
        """
        return self.__apply_operator("__sub__", value)

    def __xor__(self, value: Union[Self, Callable[[Self, List[Self]], Self]]):
        """
        Examples
        --------
        >>> from openscad_py.objects_2d import Circle, Square
        >>> from openscad_py.transformations import Translate
        >>> example = (Square(40)
        ...     | Circle(5)
        ...     | Translate.X(40) << Circle(7)
        ...     | Translate.Y(40) << Circle(9)
        ...     | Translate([40, 40, 0]) << Circle(11))
        >>> example[lambda x: isinstance(x, Circle)] ^= Square(12, center=True)
        >>> example
        union() {
            square(size=[40, 40]);
            union() {
                difference() {
                    circle(r=5);
                    square(size=[12, 12], center=true);
                }
                difference() {
                    square(size=[12, 12], center=true);
                    circle(r=5);
                }
            }
            translate(v=[40, 0, 0])
            union() {
                difference() {
                    circle(r=7);
                    square(size=[12, 12], center=true);
                }
                difference() {
                    square(size=[12, 12], center=true);
                    circle(r=7);
                }
            }
            translate(v=[0, 40, 0])
            union() {
                difference() {
                    circle(r=9);
                    square(size=[12, 12], center=true);
                }
                difference() {
                    square(size=[12, 12], center=true);
                    circle(r=9);
                }
            }
            translate(v=[40, 40, 0])
            union() {
                difference() {
                    circle(r=11);
                    square(size=[12, 12], center=true);
                }
                difference() {
                    square(size=[12, 12], center=true);
                    circle(r=11);
                }
            }
        }
        >>> example = (Square(40)
        ...     | Circle(5)
        ...     | Translate.X(40) << Circle(7)
        ...     | Translate.Y(40) << Circle(9)
        ...     | Translate([40, 40, 0]) << Circle(11))
        >>> example[lambda x: isinstance(x, Circle)] ^= lambda x: Square(x.r * 2 - 2, center=True)
        >>> example
        union() {
            square(size=[40, 40]);
            union() {
                difference() {
                    circle(r=5);
                    square(size=[8, 8], center=true);
                }
                difference() {
                    square(size=[8, 8], center=true);
                    circle(r=5);
                }
            }
            translate(v=[40, 0, 0])
            union() {
                difference() {
                    circle(r=7);
                    square(size=[12, 12], center=true);
                }
                difference() {
                    square(size=[12, 12], center=true);
                    circle(r=7);
                }
            }
            translate(v=[0, 40, 0])
            union() {
                difference() {
                    circle(r=9);
                    square(size=[16, 16], center=true);
                }
                difference() {
                    square(size=[16, 16], center=true);
                    circle(r=9);
                }
            }
            translate(v=[40, 40, 0])
            union() {
                difference() {
                    circle(r=11);
                    square(size=[20, 20], center=true);
                }
                difference() {
                    square(size=[20, 20], center=true);
                    circle(r=11);
                }
            }
        }
        """
        return self.__apply_operator("__xor__", value)

    def __lshift__(self, value: Union[Self, Callable[[Self, List[Self]], Self]]):
        return self.__apply_operator("__lshift__", value)

    def __apply_operator(
        self, operator: str, value: Union[Self, Callable[[Self, List[Self]], Self]]
    ):
        result = []
        for x, path in self.entities_with_paths:
            v = value
            if callable(value):
                if len(signature(value).parameters) == 1:
                    v = value(x)
                elif len(signature(value).parameters) == 2:
                    v = value(x, path)

            for i, child in enumerate(path[-1].children):
                if child is x:
                    path[-1].children[i] = getattr(child, operator)(v)
                    break
            result.append((v, path))
        return EntitySelector(result)
