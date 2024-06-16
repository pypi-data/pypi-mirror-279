"""
Module to provide network firewall shapes.
"""

from xml.etree import ElementTree as ET
from typing_extensions import Unpack
import osvg
import osvg.elements
from osvg_collections._base.rotated_group import RotatedGroupShape
from osvg_collections._base.parameters import ExtraStyledElementParameters
from osvg_collections._base.rectangle_shape import (
    RectangleLikeParameters,
    SCRectangleBasedShape,
)


class FirewallParams(ExtraStyledElementParameters, RectangleLikeParameters):
    """
    Firewall class parameter definitions
    """

    fill_color: str
    joints_color: str


class Firewall(osvg.SCRectangle, RotatedGroupShape, SCRectangleBasedShape):
    """
    Class for firewall shapes.
    """

    # pylint: disable=too-few-public-methods

    def __init__(self, **kwargs: Unpack[FirewallParams]) -> None:
        self.border_color = kwargs.get("border_color", "ff8000")
        self.fill_color = kwargs.get("fill_color", "ffb366")
        self.joints_color = kwargs.get("joints_color", "ffffff")
        super().__init__(**kwargs)

    @property
    def inner_stroke_width(self) -> float:
        """
        Get calculated stroke with for inner drawings
        """
        return super().inner_stroke_width / 2

    @property
    def _plain_etree_element(self) -> ET.Element:
        """
        Create ET for this firewall shape
        """
        # pylint: disable=too-many-locals,too-many-statements
        g = self.get_group_element(
            style=osvg.Style(
                stroke_color=self.joints_color,
                stroke_width=self.inner_stroke_width,
                fill_color=self.fill_color,
            ),
        )
        self.get_border_rectangle(parent=g)
        inner_rect = self.get_fill_rectangle(parent=g)
        # Add joints
        rows = 6
        brick_height = (self.fill_width + self.fill_heigth) / 14
        brick_length = brick_height * 2
        rows = int((self.fill_heigth - self.border_width * 4) / brick_height)
        y_start_offset = (self.fill_heigth - rows * brick_height) / 2
        for i in range(rows + 1):
            if i % 2:
                x_shift_left = brick_length / 2 - self.border_width
                x_shift_rigth = -self.border_width * 2
            else:
                x_shift_left = self.border_width * 2
                x_shift_rigth = -brick_length / 2 + self.border_width
            # Draw horizontal joint
            osvg.Line(
                parent=g,
                start=inner_rect.connectors["top-left"]
                + (x_shift_left, brick_height * i + y_start_offset),
                end=inner_rect.connectors["top-right"]
                + (
                    x_shift_rigth,
                    brick_height * i + y_start_offset,
                ),
            )
            # Draw vertical joints between stones in this row
            top_left = inner_rect.connectors["top-left"]
            y_shift = brick_height * i + y_start_offset
            if i < rows:
                x_shift = x_shift_left + brick_length / 2
                while float(x_shift) <= float(self.fill_width - brick_length / 2):
                    osvg.Line(
                        parent=g,
                        start=top_left + (x_shift, y_shift),
                        end=top_left
                        + (
                            x_shift,
                            y_shift + brick_height,
                        ),
                    )
                    x_shift += brick_length
        return g.etree_element
