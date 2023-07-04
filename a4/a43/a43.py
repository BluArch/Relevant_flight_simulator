#!/usr/bin/env python
"""Assignment 4 Part 3"""
print(__doc__)

import random as rd
from enum import Enum
from typing import IO, List, NamedTuple


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
        return f'({self.width},{self.height})'
    
class PyArtConfig:
    """Input configuration for an instance of a random shape"""
    def __init__(self, can: Extent, sha: Irange, rad: Irange,
                rwh: Extent, col: Colour) -> None:
        self.shape: Irange = sha
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

    
class RandomShape:
    """class creates an instance of a PyArtConfig based """
    def __init__(self, config: PyArtConfig) -> None:
        self.shape_type: int = gen_int(config.shape)
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

    def __str__(self) -> str:
        """Returns a string detailing the values of a RandomShape instance"""
        return f'\nCurrent instance of a RandomShape\n' \
               f'Current number value = {self.shape_type}\n' \
               f'X-coordinate = {self.canX}, Y-coordinate = {self.canY}\n' \
               f'Radius = {self.radius}, with width = {self.width} and height = {self.height}\n' \
               f'Colour(R,G,B) = ({self.red},{self.green},{self.blue})\n' \
               f'Opacity = {self.opacity:.1f}\n'

    def as_svg(self) -> str:
        """Returns the appropriate svg string depending on the shape of the RandomShape"""
        if(self.shape_type == 0):
            temp:CircleShape = CircleShape(self)
            return temp.circ_svg()
        else:
            temp:RectShape = RectShape(self)
            return temp.rect_svg()
        

class CircleShape:
    """Circle class"""
    def __init__(self, object: RandomShape) -> None:
        self.cx: int = object.canX
        self.cy: int = object.canY
        self.rad: int = object.radius
        self.red: int = object.red
        self.green: int = object.green
        self.blue: int = object.blue
        self.op: float = object.opacity

    def circ_svg(self) -> str:
        """Returns the svg string for the instance of a circle"""
        svg_line = f'<circle cx="{self.cx}" cy="{self.cy}" r="{self.rad}" ' \
                f'fill="rgb({self.red},{self.green},{self.blue})" ' \
                f'fill-opacity="{self.op}"></circle>'
        return svg_line
    

class RectShape:
    """Circle class"""
    def __init__(self, object: RandomShape) -> None:
        self.cx: int = object.canX
        self.cy: int = object.canY
        self.width: int = object.width
        self.height: int = object.height
        self.red: int = object.red
        self.green: int = object.green
        self.blue: int = object.blue
        self.op: float = object.opacity

    def rect_svg(self) -> str:
        """Returns the svg string for the instance of a circle"""
        svg_line = f'<rect x="{self.cx}" y="{self.cy}" width="{self.width}" height="{self.height}" ' \
                   f'fill="rgb({self.red},{self.green},{self.blue})" ' \
                   f'fill-opacity="{self.op}"></rect>'
        return svg_line
    

def gen_int(r: Irange) -> int:
    """Returns a randomly generated integer"""
    return rd.randint(r.imin, r.imax)

def gen_float(r: Frange) -> float:
    """Returns a randomly generated float"""
    return rd.uniform(r.fmin, r.fmax)


class HtmlDocument:
    """Html Document Class"""
    TAB: str = "   "

    def __init__(self, filename: str, title_name: str, dimensions: tuple) -> None:
        self.title: str = title_name
        self.tabs: int = 0
        self.writeTo: IO[str] = open(filename, "w")
        self.width: int = dimensions[0]
        self.height: int = dimensions[1]
        self.__write_head()
        self.__svg_head()

    def __write_head(self) -> None:
        """Appends the header for a html document"""
        self.append("<html>")
        self.append("<head>")
        self.increase_indent()
        self.append(f'<title>{self.title}</title>')
        self.decrease_indent()
        self.append("</head>")
        self.append("<body>")

    def append(self, line: str) -> None:
        """Appends the given HTML command to this document"""
        tab: str = HtmlDocument.TAB * self.tabs
        self.writeTo.write(f'{tab}{line}\n')
        
    def increase_indent(self) -> None:
        """Increases the num of tab characters for indentation"""
        self.tabs += 1

    def decrease_indent(self) -> None:
        """Decreases the num of tab characters for indentation"""
        self.tabs -= 1

    def __write_comment(self, line:str) -> None:
        """Append an HTML comment to it's document"""
        ts: str = "   " * self.tabs
        self.append(f'<!---{line}--->')

    def __svg_head(self) -> None:
        """Appends the header for the SVG canvas of the document"""
        self.increase_indent()
        self.__write_comment("Define SVG drawing box")
        self.append(f'<svg width=\"{self.width}\" height=\"{self.height}\">')
    
    def closeSVGcanvas(self) -> None:
        """Closes the SVG canvas of the document"""
        ts: str = "   " * self.tabs
        self.append("</svg>")
        self.decrease_indent()
        self.append("</body>")
        self.append("</html>") 

    def gen_art(self, line: str) -> None:
        """Appends a given svg string, drawing a shape to the html document"""
        self.increase_indent()
        self.append(line)
        self.decrease_indent()


def drawing(writeTo: HtmlDocument, art_style: PyArtConfig, num_shapes: int) -> None:
    """Will draw 5 circles with a given color, at a given xy coordinate location to the html document"""
    writeTo.increase_indent()
    for i in range(num_shapes):
        temp: RandomShape = RandomShape(art_style)
        writeTo.gen_art(temp.as_svg())
    writeTo.decrease_indent()

    
def basic_archetype(dimensions: tuple) -> PyArtConfig:
    """Returns a PyArtConfig of completely random shapes"""
    canvas_dimen: Extent = Extent(Irange(imin = 0, imax = dimensions[0]), Irange(imin = 0, imax = dimensions[1]))
    circ_radius: Irange = Irange(imin = 0, imax = 100)
    rect_rwh: Extent = Extent(Irange(imin = 10, imax = 100), Irange(imin = 10, imax = 100))
    colours: Colour = Colour(Irange(imin = 0, imax = 255), Irange(imin = 0, imax = 255), Irange(imin = 0, imax = 255), Frange(fmin = 0.0, fmax = 1.0))
    shapes: Irange = Irange(imin = 0, imax = 1)
    temp: PyArtConfig = PyArtConfig(canvas_dimen, shapes, circ_radius, rect_rwh, colours)
    return temp

def midnight_archetype(dimensions: tuple) -> PyArtConfig:
    """Returns a PyArtConfig to form a portrait of a midnight sky"""
    canvas_dimen: Extent = Extent(Irange(imin = 0, imax = dimensions[0]), Irange(imin = 0, imax = dimensions[1]))
    circ_radius: Irange = Irange(imin = 0, imax = 100)
    rect_rwh: Extent = Extent(Irange(imin = 10, imax = 100), Irange(imin = 10, imax = 100))
    colours: Colour = Colour(Irange(imin = 0, imax =100), Irange(imin = 0, imax = 100), Irange(imin = 0, imax = 255), Frange(fmin = 0.0, fmax = 1.0))
    shapes: Irange = Irange(imin = 0, imax = 1)
    temp: PyArtConfig = PyArtConfig(canvas_dimen, shapes, circ_radius, rect_rwh, colours)
    return temp

def fall_archetype(dimensions: tuple) -> PyArtConfig:
    """Returns a PyArtConfig to form a portrait of fall colours"""
    canvas_dimen: Extent = Extent(Irange(imin = 0, imax = dimensions[0]), Irange(imin = 0, imax = dimensions[1]))
    circ_radius: Irange = Irange(imin = 0, imax = 100)
    rect_rwh: Extent = Extent(Irange(imin = 10, imax = 100), Irange(imin = 10, imax = 100))
    colours: Colour = Colour(Irange(imin = 100, imax = 255), Irange(imin = 0, imax = 175), Irange(imin = 0, imax = 50), Frange(fmin = 0.0, fmax = 1.0))
    shapes: Irange = Irange(imin = 0, imax = 1)
    temp: PyArtConfig = PyArtConfig(canvas_dimen, shapes, circ_radius, rect_rwh, colours)
    return temp


def writeHTMLfile() -> None:
    """Creates and writes shapes (of a chosen archetype) to a html document"""
    fnam: str = "a433.html"
    winTitle = "Fall Colours"
    dimensions: tuple = (500, 300)
    writeTo: HtmlDocument = HtmlDocument(fnam, winTitle, dimensions)
    art_style: PyArtConfig = fall_archetype((500, 300))
    drawing(writeTo, art_style, 10000)
    writeTo.closeSVGcanvas()

def main() -> None:
    """Main method"""
    writeHTMLfile()

if __name__ == "__main__":
    main()