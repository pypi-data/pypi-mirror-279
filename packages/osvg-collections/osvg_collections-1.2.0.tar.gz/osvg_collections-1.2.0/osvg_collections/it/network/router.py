"""
Module to provide network Router shapes.
"""

# pylint: disable=too-few-public-methods,too-many-ancestors

from typing_extensions import Unpack
import osvg
from . import rs_base


class Router(rs_base.RSBase):
    """
    Basic class for router shapes.
    """

    def _add_central_ornament(self, group, inner_side, stroke_width) -> None:

        # Add ornament Circle
        inner_circle = osvg.Circle(
            parent=group,
            position=self.position,
            radius=inner_side / 2,
            style=osvg.Style(fill_color="none"),
        )
        # Add inner crossed lines
        osvg.Line(
            parent=group,
            start=osvg.PolarShiftedPosition(
                origin=inner_circle.connectors["top-left"],
                angle=45,
                distance=stroke_width * 2,
            ),
            end=osvg.PolarShiftedPosition(
                origin=inner_circle.connectors["bottom-right"],
                angle=-135,
                distance=stroke_width * 2,
            ),
        )
        osvg.Line(
            parent=group,
            start=osvg.PolarShiftedPosition(
                origin=inner_circle.connectors["top-right"],
                angle=135,
                distance=stroke_width * 2,
            ),
            end=osvg.PolarShiftedPosition(
                origin=inner_circle.connectors["bottom-left"],
                angle=-45,
                distance=stroke_width * 2,
            ),
        )
        return inner_circle


class RouterGray(Router):
    """
    Red Router shape
    """

    def __init__(self, **kwargs: Unpack[rs_base.RSBaseParams]) -> None:
        kwargs["border_color"] = kwargs.get("border_color", "444444")
        kwargs["fill_color"] = kwargs.get("fill_color", "888888")
        kwargs["ornament_color"] = kwargs.get("ornament_color", "ffffff")
        super().__init__(**kwargs)


class RouterRed(Router):
    """
    Red Router shape
    """

    def __init__(self, **kwargs: Unpack[rs_base.RSBaseParams]) -> None:
        kwargs["border_color"] = kwargs.get("border_color", "ff0000")
        kwargs["fill_color"] = kwargs.get("fill_color", "ff9999")
        kwargs["ornament_color"] = kwargs.get("ornament_color", "ffffff")
        super().__init__(**kwargs)


class RouterGreen(Router):
    """
    Green Router shape
    """

    def __init__(self, **kwargs: Unpack[rs_base.RSBaseParams]) -> None:
        kwargs["border_color"] = kwargs.get("border_color", "00bb00")
        kwargs["fill_color"] = kwargs.get("fill_color", "99ff99")
        kwargs["ornament_color"] = kwargs.get("ornament_color", "ffffff")
        super().__init__(**kwargs)


class RouterBlue(Router):
    """
    Blue Router shape
    """

    def __init__(self, **kwargs: Unpack[rs_base.RSBaseParams]) -> None:
        kwargs["border_color"] = kwargs.get("border_color", "0000bb")
        kwargs["fill_color"] = kwargs.get("fill_color", "3399ff")
        kwargs["ornament_color"] = kwargs.get("ornament_color", "ffffff")
        super().__init__(**kwargs)


class RouterOrange(Router):
    """
    Orange Router shape
    """

    def __init__(self, **kwargs: Unpack[rs_base.RSBaseParams]) -> None:
        kwargs["border_color"] = kwargs.get("border_color", "ff8000")
        kwargs["fill_color"] = kwargs.get("fill_color", "ffcc99")
        kwargs["ornament_color"] = kwargs.get("ornament_color", "ffffff")
        super().__init__(**kwargs)
