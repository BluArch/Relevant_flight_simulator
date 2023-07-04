#!/usr/bin/env python
"""Assignment 4 Part 1"""
print(__doc__)

from typing import IO, NamedTuple

class Colour(NamedTuple):
    """RBG colors based on a given integer range"""
    red: int
    green: int
    blue: int
    opacity: int


class CircleInfo(NamedTuple):
    """Class that holds the dimensions of a circle"""
    cx: int
    cy: int
    rad: int


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


class CircleShape:
    """Circle class"""
    def __init__(self, cir: CircleInfo, col: Colour) -> None:
        self.__cx: int = cir.cx
        self.__cy: int = cir.cy
        self.__rad: int = cir.rad
        self.__red: int = col.red
        self.__green: int = col.green
        self.__blue: int = col.blue
        self.__op: float = col.opacity

    def as_svg(self) -> str:
        """Returns the svg string for the instance of a circle"""
        svg_line = f'<circle cx="{self.__cx}" cy="{self.__cy}" r="{self.__rad}" ' \
                f'fill="rgb({self.__red},{self.__green},{self.__blue})" ' \
                f'fill-opacity="{self.__op}"></circle>'
        return svg_line


def drawing(writeTo: HtmlDocument, circ_info: CircleInfo, circ_colour: Colour) -> None:
    """Will draw 5 circles with a given color, at a given xy coordinate location to the html document"""
    circle = CircleShape(circ_info, circ_colour)
    writeTo.gen_art(circle.as_svg())


def circleCreate_Part1(writeTo: HtmlDocument):
    """Creates red and blue circles along y=50 and y=250 in a html document"""
    x_axis: int = 50
    for i in range(5):
        drawing(writeTo, CircleInfo(cx=x_axis, cy=50, rad=50), Colour(red=255, green=0, blue=0, opacity=1.0))
        x_axis += 100
    x_axis = 50
    for i in range(5):
        drawing(writeTo, CircleInfo(cx=x_axis, cy=250, rad=50), Colour(red=0, green=0, blue=255, opacity=1.0))
        x_axis += 100


def writeHTMLfile() -> None:
    """Creates and writes circles to a html document"""
    fnam: str = "a41.html"
    winTitle = "Assignment 4 - SENG265 - My Art"
    writeTo: HtmlDocument = HtmlDocument(fnam, winTitle, (500, 300))
    circleCreate_Part1(writeTo)
    writeTo.closeSVGcanvas()


def main() -> None:
    """Main method"""
    writeHTMLfile()


if __name__ == "__main__":
    main()