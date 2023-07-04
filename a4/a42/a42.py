#!/usr/bin/env python
"""Assignment 4 Part 2"""
print(__doc__)

import random as rd
from enum import Enum
from typing import IO, List, NamedTuple

class ShapeKind(str, Enum):
    """Class of possible shapes to create"""
    CIRCLE = 0
    RECTANGLE = 1
    ELLIPSE = 3

    def __str__(self) -> str:
        """Returns a string of the values of ShapeKind"""
        return f'{self.value}'
    

class Irange(NamedTuple):
    """An integer range with max and minimum values"""
    imin: int
    imax: int

    def __str__(self) -> str:
        """Returns a string of the values of an instance of Irange"""
        return f'{self.imin},{self.imax}'
    

class Frange(NamedTuple):
    """A float range with minimum and maximum values"""
    fmin: float
    fmax: float

    def __str__(self) -> str:
        """Returns a string of the values of an instance of Frange"""
        return f'{self.fmin},{self.fmax}'
    

class Colour(NamedTuple):
    """RBG colors based on a given integer range"""
    red: Irange
    green: Irange
    blue: Irange
    opacity: Frange

    def __str__(self) -> str:
        """Returns a string of the values of an instance of Colour"""
        return f'({self.red},{self.green},{self.blue})'
    

class Extent(NamedTuple):
    """Extent based on width and height ranges"""
    width: Irange
    height: Irange

    def __str__(self) -> str:
        """Returns a string of the values of an instance of Extent"""
        return f'({self.width},{self.height})'
    
class PyArtConfig:
    """Input configuration for an instance of a random shape"""
    def __init__(self, can: Extent, sha: List[ShapeKind], rad: Irange,
                rwh: Extent, col: Colour) -> None:
        self.shape: List[ShapeKind] = sha
        self.can: Extent = can
        self.rad: Irange = rad
        self.rwh: Extent = rwh
        self.col: Colour = col

    def __str__(self) -> str:
        """Returns a string detailing the values of the PyArtConfig"""
        return f'\nUser-defined art configuration\n' \
               f'Shape types = ({", ".join(self.shape)})\n' \
               f'can(CXMIN,MXMAX,CYMIN,CYMAX) = {self.can})\n' \
               f'rad(RADMIN,RADMAX) = ({self.rad})\n' \
               f'rwh(WMIN,WMAX,HMIN,HMAX) = {self.rwh}\n' \
               f'col(REDMIN,REDMAX,GREMIN,GREMAX,BLUMIN,BLUEMAX) = {self.col}\n' \
               f'col(OPMIN,OPMAX) = ({self.col.opacity.fmin:.1f},{self.col.opacity.fmax:.1f})\n'

def gen_int(r: Irange) -> int:
    """Returns a randomly generated integer"""
    return rd.randint(r.imin, r.imax)

def gen_float(r: Frange) -> float:
    """Returns a randomly generated float"""
    return rd.uniform(r.fmin, r.fmax)

class RandomShape:
    """class creates an instance of a PyArtConfig based """
    def __init__(self, config: PyArtConfig, count: int) -> None:
        self.shape_type: int = rd.choice(config.shape)
        self.canX: int = gen_int(config.can.width)
        self.canY: int = gen_int(config.can.height)
        self.radius: int = gen_int(config.rad)
        self.rx: int = rd.randint(10,30)
        self.ry: int = rd.randint(10,30)
        self.width: int = gen_int(config.rwh.width)
        self.height: int = gen_int(config.rwh.height)
        self.red: int = gen_int(config.col.red)
        self.green: int = gen_int(config.col.green)
        self.blue: int = gen_int(config.col.blue)
        self.opacity: float = gen_float(config.col.opacity)
        self.config: PyArtConfig = config
        self.count: int = count

    def __str__(self) -> str:
        """Returns a string detailing the values of a RandomShape instance"""
        return f'\nCurrent instance of a RandomShape\n' \
               f'Current number value = {self.shape_type}\n' \
               f'X-coordinate = {self.canX}, Y-coordinate = {self.canY}\n' \
               f'Radius = {self.radius}, with width = {self.width} and height = {self.height}\n' \
               f'Colour(R,G,B) = ({self.red},{self.green},{self.blue})\n' \
               f'Opacity = {self.opacity:.1f}\n'
    
    def as_Part2_line(self) -> str:
        """Returns a string of columns containing the values of a RandomShape instance"""
        return f'{self.shape_type: >4}{self.canX: >4}{self.canY: >4}{self.radius: >4}{self.rx: >4}' \
               f'{self.count: >4}{self.ry: >4}{self.width: >4}{self.height: >4}{self.red: >4}{self.green: >4}{self.blue: >4}{self.opacity:>4.1f}'

    def as_svg(self) -> str:
        """Returns the appropriate svg string depending on the shape of the RandomShape"""
        if(self.shape_type == 0):
            return f'<circle cx="{self.canX}" cy="{self.canY}" r="{self.radius}" ' \
                   f'fill="rgb({self.red},{self.green},{self.blue})" ' \
                   f'fill-opacity="{self.opacity}"></circle>'
        elif(self.shape_type == 1):
            return f'<rect x="{self.canX}" y="{self.canY}" width="{self.width}" height="{self.height}" ' \
                   f'style="rgb({self.red},{self.green},{self.blue})" ' \
                   f'fill-opacity="{self.opacity}"></rect>'
        else:
            return f'<ellipse cx="{self.canX}" cy="{self.canY}" rx="{self.rx}" ry="{self.ry}" ' \
                   f'style="rgb({self.red},{self.green},{self.blue})" ' \
                   f'fill-opacity="{self.opacity}"></ellipse>'


def basic_archetype():
    """Creates a PyArtConfig of 10 completely random shapes and prints the appropriate svg string"""
    canvas_dimen: Extent = Extent(Irange(imin = 0, imax = 600), Irange(imin = 0, imax = 400))
    circ_radius: Irange = Irange(imin = 0, imax = 100)
    rect_rwh: Extent = Extent(Irange(imin = 10, imax = 100), Irange(imin = 10, imax = 100))
    colours: Colour = Colour(Irange(imin = 0, imax = 255), Irange(imin = 0, imax = 255), Irange(imin = 0, imax = 255), Frange(fmin = 0.0, fmax = 1.0))
    possible_shapes: List[ShapeKind] = [ShapeKind.CIRCLE, ShapeKind.RECTANGLE, ShapeKind.ELLIPSE]
    temp: PyArtConfig = PyArtConfig(canvas_dimen, possible_shapes, circ_radius, rect_rwh, colours)

    count: int = 0
    print(f"{'CNT': >4}{'SHA': >4}{'X': >4}{'Y': >4}{'RAD': >4}{'RX': >4}{'RY': >4}{'W': >4}{'H': >4}{'R': >4}{'R': >4}{'B': >4}{'OP':>4}")
    for i in range(10):
        temp1: RandomShape = RandomShape(temp, count)
        print(temp1.as_Part2_line())
        count += 1

def main() -> None:
    """Main method"""
    basic_archetype()

if __name__ == "__main__":
    main()