"""
Module to provide network switch shapes.
"""

# pylint: disable=too-few-public-methods,too-many-ancestors

from typing_extensions import Unpack
import osvg
from . import rs_base


class Switch(rs_base.RSBase):
    """
    Basic class for switch shapes.
    """

    def _add_central_ornament(self, group, inner_side, stroke_width) -> None:

        # Add ornament rectangle
        inner_rect = osvg.Rectangle(
            parent=group,
            position=self.position,
            width=inner_side,
            height=inner_side,
            style=osvg.Style(fill_color="none"),
        )
        # Add inner crossed lines
        osvg.Line(
            parent=group,
            start=osvg.PolarShiftedPosition(
                origin=inner_rect.connectors["top-left"],
                angle=45,
                distance=stroke_width * 5,
            ),
            end=osvg.PolarShiftedPosition(
                origin=inner_rect.connectors["bottom-right"],
                angle=-135,
                distance=stroke_width * 5,
            ),
        )
        osvg.Line(
            parent=group,
            start=osvg.PolarShiftedPosition(
                origin=inner_rect.connectors["top-right"],
                angle=135,
                distance=stroke_width * 5,
            ),
            end=osvg.PolarShiftedPosition(
                origin=inner_rect.connectors["bottom-left"],
                angle=-45,
                distance=stroke_width * 5,
            ),
        )
        return inner_rect


class SwitchGray(Switch):
    """
    Red Switch shape
    """

    def __init__(self, **kwargs: Unpack[rs_base.RSBaseParams]) -> None:
        kwargs["border_color"] = kwargs.get("border_color", "444444")
        kwargs["fill_color"] = kwargs.get("fill_color", "888888")
        kwargs["ornament_color"] = kwargs.get("ornament_color", "ffffff")
        super().__init__(**kwargs)


class SwitchRed(Switch):
    """
    Red Switch shape
    """

    def __init__(self, **kwargs: Unpack[rs_base.RSBaseParams]) -> None:
        kwargs["border_color"] = kwargs.get("border_color", "ff0000")
        kwargs["fill_color"] = kwargs.get("fill_color", "ff9999")
        kwargs["ornament_color"] = kwargs.get("ornament_color", "ffffff")
        super().__init__(**kwargs)


class SwitchGreen(Switch):
    """
    Green Switch shape
    """

    def __init__(self, **kwargs: Unpack[rs_base.RSBaseParams]) -> None:
        kwargs["border_color"] = kwargs.get("border_color", "00bb00")
        kwargs["fill_color"] = kwargs.get("fill_color", "99ff99")
        kwargs["ornament_color"] = kwargs.get("ornament_color", "ffffff")
        super().__init__(**kwargs)


class SwitchBlue(Switch):
    """
    Blue Switch shape
    """

    def __init__(self, **kwargs: Unpack[rs_base.RSBaseParams]) -> None:
        kwargs["border_color"] = kwargs.get("border_color", "0000bb")
        kwargs["fill_color"] = kwargs.get("fill_color", "3399ff")
        kwargs["ornament_color"] = kwargs.get("ornament_color", "ffffff")
        super().__init__(**kwargs)


class SwitchOrange(Switch):
    """
    Orange Switch shape
    """

    def __init__(self, **kwargs: Unpack[rs_base.RSBaseParams]) -> None:
        kwargs["border_color"] = kwargs.get("border_color", "ff8000")
        kwargs["fill_color"] = kwargs.get("fill_color", "ffcc99")
        kwargs["ornament_color"] = kwargs.get("ornament_color", "ffffff")
        super().__init__(**kwargs)
