"""
Module to provide RotatedGroup class
"""

from typing import TypedDict
import osvg.elements.elementbase
import osvg

import osvg.elements


class RectangleLikeParameters(TypedDict):
    """
    Parameter class for element classes based classes without upstream style parameter
    """

    width: float | osvg.float.Float
    height: float | osvg.float.Float


class RectangleBasedShape:
    # pylint: disable=no-member
    """
    Meta class for shapes which base on a rectangle.
    """

    border_width_precentage = 1.5

    @property
    def border_width(self) -> float:
        """
        Get calculated border with
        """
        return (self.width + self.height) / 100 * self.border_width_precentage

    @property
    def inner_stroke_width(self) -> float:
        """
        Get calculated stroke with for inner drawings
        """
        return (
            osvg.Min(self.width, self.height) / 100 * self.border_width_precentage * 2
        )

    def get_border_rectangle(self, parent: osvg.elements.elementbase.SVGElement):
        """
        Get background rectangle to represent the border line
        """
        return osvg.Rectangle(
            parent=parent,
            position=self.position,
            width=self.width,
            height=self.height,
            style=osvg.Style(fill_color=self.border_color, stroke_width=0),
        )

    @property
    def fill_width(self) -> float:
        """
        Get calculated width of inner rectangle (fill)
        """
        return self.width - self.border_width * 2

    @property
    def fill_heigth(self) -> float:
        """
        Get calculated height of inner rectangle (fill)
        """
        return self.height - self.border_width * 2

    def get_fill_rectangle(self, parent: osvg.elements.elementbase.SVGElement):
        """
        Get foreground rectangle to represent the filling
        """
        return osvg.Rectangle(
            parent=parent,
            position=self.position,
            width=self.fill_width,
            height=self.fill_heigth,
            style=osvg.Style(stroke_width=0),
        )


class SCRectangleBasedShape(RectangleBasedShape):
    # pylint: disable=no-member
    """
    Meta class for shapes which base on a smooth cornered rectangle.
    """

    def get_border_rectangle(self, parent: osvg.elements.elementbase.SVGElement):
        """
        Get background rectangle to represent the border line
        """
        return osvg.SCRectangle(
            parent=parent,
            position=self.position,
            width=self.width,
            height=self.height,
            percentage=self.border_width,
            style=osvg.Style(fill_color=self.border_color, stroke_width=0),
        )

    def get_fill_rectangle(self, parent: osvg.elements.elementbase.SVGElement):
        """
        Get foreground rectangle to represent the filling
        """
        width = self.fill_width
        height = self.fill_heigth
        percentage = (width + height) / 100 * self.border_width_precentage
        return osvg.SCRectangle(
            parent=parent,
            position=self.position,
            width=width,
            height=height,
            percentage=percentage,
            style=osvg.Style(stroke_width=0),
        )
