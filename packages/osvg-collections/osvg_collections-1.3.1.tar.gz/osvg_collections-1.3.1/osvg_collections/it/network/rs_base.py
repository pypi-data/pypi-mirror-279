"""
Module to provide network switch shapes.
"""

from xml.etree import ElementTree as ET
from typing_extensions import Unpack
import osvg.elements.elementbase
import osvg
import osvg.elements
from osvg_collections._base.rotated_group import RotatedGroupShape
from osvg_collections._base.parameters import ExtraStyledElementParameters
from osvg_collections._base.rectangle_shape import (
    RectangleLikeParameters,
    SCRectangleBasedShape,
)


class RSBaseParams(ExtraStyledElementParameters, RectangleLikeParameters):
    """
    Router or Switch class parameter definitions
    """

    border_color: str
    fill_color: str
    ornament_color: str


class RSBase(osvg.SCRectangle, RotatedGroupShape, SCRectangleBasedShape):
    """
    Basic class for router and switch shapes.
    """

    # pylint: disable=too-few-public-methods

    def __init__(self, **kwargs: Unpack[RSBaseParams]) -> None:
        self.border_color = kwargs.get("border_color")
        self.fill_color = kwargs.get("fill_color")
        self.ornament_color = kwargs.get("ornament_color")
        super().__init__(**kwargs)

    def _add_central_ornament(
        self, group, inner_side, stroke_width
    ) -> osvg.elements.elementbase.SVGElement:
        """
        Add inner central ornament
        """
        raise NotImplementedError()

    @property
    def _plain_etree_element(self) -> ET.Element:
        """
        Create ET for this switch shape
        """
        # pylint: disable=too-many-locals,too-many-statements
        g = self.get_group_element(
            style=osvg.Style(
                stroke_color=self.ornament_color,
                stroke_width=self.inner_stroke_width,
                fill_color=self.fill_color,
            )
        )
        self.get_border_rectangle(parent=g)
        self.get_fill_rectangle(parent=g)
        inner_side = osvg.Min(self.width, self.height) - self.border_width * 5
        self._add_central_ornament(g, inner_side, self.inner_stroke_width)
        ###
        ### Add arrows depending on orientation
        ###
        if float(self.width) > float(self.height):
            arrow_stroke_width = self.height / 12
            arrow_length = arrow_stroke_width * 3
            arrow_width = arrow_stroke_width * 2
            right_x_shift1 = inner_side / 2 + self.border_width * 2
            line_length = self.width / 2 - right_x_shift1 - self.border_width * 4
            left_x_shift1 = -right_x_shift1
            upper_y_shift = -self.height / 6
            lower_y_shift = self.height / 6
            # upper_left_arrow
            upper_left_start = self.position + (left_x_shift1, upper_y_shift)
            upper_left_arrow = osvg.Line(
                parent=g,
                start=upper_left_start,
                end=osvg.XShiftedPosition(
                    origin=upper_left_start,
                    x_shift=-line_length,
                ),
                style=osvg.Style(stroke_width=arrow_stroke_width),
            )
            upper_left_arrow.add_end_marker(
                osvg.ArrowMarker, length=arrow_length, width=arrow_width
            )
            # lower_left_arrow
            lower_left_start = self.position + (left_x_shift1, lower_y_shift)
            lower_left_arrow = osvg.Line(
                parent=g,
                start=lower_left_start,
                end=osvg.XShiftedPosition(
                    origin=lower_left_start,
                    x_shift=-line_length,
                ),
                style=osvg.Style(stroke_width=arrow_stroke_width),
            )
            lower_left_arrow.add_end_marker(
                osvg.ArrowMarker, length=arrow_length, width=arrow_width
            )
            # upper_right_arrow
            upper_right_start = self.position + (right_x_shift1, upper_y_shift)
            upper_right_arrow = osvg.Line(
                parent=g,
                start=upper_right_start,
                end=osvg.XShiftedPosition(
                    origin=upper_right_start,
                    x_shift=line_length,
                ),
                style=osvg.Style(stroke_width=arrow_stroke_width),
            )
            upper_right_arrow.add_end_marker(
                osvg.ArrowMarker, length=arrow_length, width=arrow_width
            )
            # lower_right_arrow
            lower_right_start = self.position + (right_x_shift1, lower_y_shift)
            lower_right_arrow = osvg.Line(
                parent=g,
                start=lower_right_start,
                end=osvg.XShiftedPosition(
                    origin=lower_right_start,
                    x_shift=line_length,
                ),
                style=osvg.Style(stroke_width=arrow_stroke_width),
            )
            lower_right_arrow.add_end_marker(
                osvg.ArrowMarker, length=arrow_length, width=arrow_width
            )
        elif float(self.width) < float(self.height):
            arrow_stroke_width = self.width / 12
            arrow_length = arrow_stroke_width * 3
            arrow_width = arrow_stroke_width * 2
            lower_y_shift1 = inner_side / 2 + self.border_width * 2
            line_length = self.height / 2 - lower_y_shift1 - self.border_width * 4
            upper_y_shift1 = -lower_y_shift1
            right_x_shift = self.width / 6
            left_x_shift = -right_x_shift
            # upper_left_arrow
            upper_left_start = self.position + (left_x_shift, upper_y_shift1)
            upper_left_arrow = osvg.Line(
                parent=g,
                start=upper_left_start,
                end=osvg.YShiftedPosition(
                    origin=upper_left_start,
                    y_shift=-line_length,
                ),
                style=osvg.Style(stroke_width=arrow_stroke_width),
            )
            upper_left_arrow.add_end_marker(
                osvg.ArrowMarker, length=arrow_length, width=arrow_width
            )
            # upper_rigth_arrow
            upper_rigth_start = self.position + (right_x_shift, upper_y_shift1)
            upper_right_arrow = osvg.Line(
                parent=g,
                start=upper_rigth_start,
                end=osvg.YShiftedPosition(
                    origin=upper_rigth_start,
                    y_shift=-line_length,
                ),
                style=osvg.Style(stroke_width=arrow_stroke_width),
            )
            upper_right_arrow.add_end_marker(
                osvg.ArrowMarker, length=arrow_length, width=arrow_width
            )
            # lower_left_arrow
            lower_left_start = self.position + (left_x_shift, lower_y_shift1)
            lower_left_arrow = osvg.Line(
                parent=g,
                start=lower_left_start,
                end=osvg.YShiftedPosition(
                    origin=lower_left_start,
                    y_shift=line_length,
                ),
                style=osvg.Style(stroke_width=arrow_stroke_width),
            )
            lower_left_arrow.add_end_marker(
                osvg.ArrowMarker, length=arrow_length, width=arrow_width
            )
            # lower_right_arrow
            lower_right_start = self.position + (right_x_shift, lower_y_shift1)
            lower_right_arrow = osvg.Line(
                parent=g,
                start=lower_right_start,
                end=osvg.YShiftedPosition(
                    origin=lower_right_start,
                    y_shift=line_length,
                ),
                style=osvg.Style(stroke_width=arrow_stroke_width),
            )
            lower_right_arrow.add_end_marker(
                osvg.ArrowMarker, length=arrow_length, width=arrow_width
            )
        return g.etree_element
