from abc import ABCMeta, abstractmethod
import copy
from inspect import signature
from openscad_py.entity_selector import EntitySelector
from typing import Callable, List, Self, Union


class Entity:

    __metaclass__ = ABCMeta

    def __init__(self) -> None:
        self.children: List[Self] = []

    def append(self, child: Self):
        self.children.append(child)

    def __sub__(self, other: Self):
        """
        Examples
        --------
        >>> from openscad_py.objects_2d import Circle, Square
        >>> Circle(10) - Square(20)
        difference() {
            circle(r=10);
            square(size=[20, 20]);
        }
        """
        result = copy.deepcopy(self)
        result -= other
        return result

    def __isub__(self, other: Self):
        """
        Examples
        --------
        >>> from openscad_py.objects_2d import Circle, Square
        >>> circle = Circle(10)
        >>> circle -= Square(20)
        >>> circle
        difference() {
            circle(r=10);
            square(size=[20, 20]);
        }
        """
        from openscad_py.combinations import Difference

        other = copy.deepcopy(other)
        if isinstance(self, Difference):
            self <<= other
        else:
            self = Difference() << self << other
        return self

    def __and__(self, other: Self):
        """
        Examples
        --------
        >>> from openscad_py.objects_2d import Circle, Square
        >>> Circle(10) & Square(20)
        intersection() {
            circle(r=10);
            square(size=[20, 20]);
        }
        """
        result = copy.deepcopy(self)
        result &= other
        return result

    def __iand__(self, other: Self):
        """
        Examples
        --------
        >>> from openscad_py.objects_2d import Circle, Square
        >>> circle = Circle(10)
        >>> circle &= Square(20)
        >>> circle
        intersection() {
            circle(r=10);
            square(size=[20, 20]);
        }
        """
        from openscad_py.combinations import Intersection

        other = copy.deepcopy(other)
        if isinstance(self, Intersection):
            self <<= other
        else:
            self = Intersection() << self << other
        return self

    def __or__(self, other: Self) -> Self:
        """
        Examples
        --------
        >>> from openscad_py.objects_2d import Circle, Square
        >>> Circle(10) | Square(20)
        union() {
            circle(r=10);
            square(size=[20, 20]);
        }
        """
        result = copy.deepcopy(self)
        result |= other
        return result

    def __ior__(self, other: Self) -> Self:
        """
        Examples
        --------
        >>> from openscad_py.objects_2d import Circle, Square
        >>> circle = Circle(10)
        >>> circle |= Square(20)
        >>> circle
        union() {
            circle(r=10);
            square(size=[20, 20]);
        }
        """
        from openscad_py.combinations import Union

        other = copy.deepcopy(other)
        if isinstance(self, Union):
            self <<= other
        else:
            self = Union() << self << other
        return self

    def __xor__(self, other: Self) -> Self:
        """
        Examples
        --------
        >>> from openscad_py.objects_2d import Circle, Square
        >>> Circle(10) ^ Square(20)
        union() {
            difference() {
                circle(r=10);
                square(size=[20, 20]);
            }
            difference() {
                square(size=[20, 20]);
                circle(r=10);
            }
        }
        """
        result = copy.deepcopy(self)
        result ^= other
        return result

    def __ixor__(self, other: Self) -> Self:
        """
        Examples
        --------
        >>> from openscad_py.objects_2d import Circle, Square
        >>> circle = Circle(10)
        >>> circle ^= Square(20)
        >>> circle
        union() {
            difference() {
                circle(r=10);
                square(size=[20, 20]);
            }
            difference() {
                square(size=[20, 20]);
                circle(r=10);
            }
        }
        """
        return copy.deepcopy(self) - copy.deepcopy(other) | copy.deepcopy(
            other
        ) - copy.deepcopy(self)

    def __lshift__(self, other: Union[Self, List[Self]]):
        """
        Examples
        --------
        >>> from openscad_py.objects_2d import Circle
        >>> from openscad_py.transformations import Rotate
        >>> Rotate(90) << (Translate.X(10) << Circle(20))
        rotate(a=90)
        translate(v=[10, 0, 0])
        circle(r=20);
        """
        result = copy.deepcopy(self)
        result <<= other
        return result

    def __ilshift__(self, other: Union[Self, List[Self]]):
        if isinstance(other, list):
            for child in other:
                self.append(child)
        else:
            self.append(other)
        return self
    
    
    def __getitem__(self, filter: Callable[[Self], bool]) -> EntitySelector:
        """
        Examples
        --------
        >>> from openscad_py.objects_2d import Circle, Square
        >>> from openscad_py.transformations import Translate
        >>> example = Translate.X(20) << Circle(10) | Circle(30)
        >>> list(
        ...     map(
        ...         lambda x: (x[0], [p.__class__ for p in x[1]]),
        ...         example[lambda x: isinstance(x, Circle) and x.r <= 20]
        ...     )
        ... )
        [(circle(r=10);, [<class 'openscad_py.combinations.Union'>, <class 'openscad_py.transformations.Translate.X'>])]
        """
        result = []
        queue = [(child, [self]) for child in self.children]
        
        while len(queue) > 0:
            (node, path) = queue.pop()
            
            if len(signature(filter).parameters) == 1:
                if filter(node):
                    result.append((node, path))
            elif len(signature(filter).parameters) == 2:
                if filter(node, path):
                    result.append((node, path))

            for child in node.children:
                queue.append((child, path + [node]))

        return EntitySelector(result)

    def __setitem__(self, filter: Callable[[Self], bool], value: Union[Self, Callable[[Self, List[Self]], Self]]):
        """
        Examples
        --------
        >>> from openscad_py.objects_2d import Circle, Square
        >>> from openscad_py.transformations import Color, Translate
        >>> example = (Square(40)
        ...     | Circle(5)
        ...     | Translate.X(40) << Circle(7)
        ...     | Translate.Y(40) << Circle(9)
        ...     | Translate([40, 40, 0]) << Circle(11))
        >>> example[lambda x: isinstance(x, Circle)] = Circle(12.5)
        >>> example
        union() {
            square(size=[40, 40]);
            circle(r=12.5);
            translate(v=[40, 0, 0])
            circle(r=12.5);
            translate(v=[0, 40, 0])
            circle(r=12.5);
            translate(v=[40, 40, 0])
            circle(r=12.5);
        }
        >>> example = (Square(40)
        ...     | Circle(5)
        ...     | Translate.X(40) << Circle(7)
        ...     | Translate.Y(40) << Circle(9)
        ...     | Translate([40, 40, 0]) << Circle(11))
        >>> example[lambda x: isinstance(x, Circle) and x.r < 8] = lambda x: Square(x.r * 2, center=True)
        >>> example
        union() {
            square(size=[40, 40]);
            square(size=[10, 10], center=true);
            translate(v=[40, 0, 0])
            square(size=[14, 14], center=true);
            translate(v=[0, 40, 0])
            circle(r=9);
            translate(v=[40, 40, 0])
            circle(r=11);
        }
        """
        if isinstance(value, EntitySelector):
            # if the value is an EntitySelector, do nothing since processing has been already done
            return
        
        for x, path in self[filter]:
            v = value
            if callable(value):
                if len(signature(value).parameters) == 1:
                    v = value(x)
                elif len(signature(value).parameters) == 2:
                    v = value(x, path)
                
            for i, child in enumerate(path[-1].children):
                if child is x:
                    path[-1].children[i] = v
                    break
    
    def __delitem__(self, filter: Callable[[Self], bool]):
        """
        Examples
        --------
        >>> from openscad_py.objects_2d import Circle, Square
        >>> from openscad_py.transformations import Color, Translate
        >>> example = (Square(40)
        ...     | Circle(5)
        ...     | Translate.X(40) << Circle(7)
        ...     | Translate.Y(40) << Circle(9)
        ...     | Translate([40, 40, 0]) << Circle(11))
        >>> del example[lambda x: isinstance(x, Circle) and x.r > 8]
        >>> example
        union() {
            square(size=[40, 40]);
            circle(r=5);
            translate(v=[40, 0, 0])
            circle(r=7);
            translate(v=[0, 40, 0]);
            translate(v=[40, 40, 0]);
        }
        """
        for x, path in self[filter]:
            for i, child in enumerate(path[-1].children):
                if child is x:
                    del path[-1].children[i]
                    break    

    def __str__(self):
        return self.__repr__()

    def __repr__(self) -> str:
        return self.render()

    @abstractmethod
    def render(self, indent: int = 0) -> str:
        pass