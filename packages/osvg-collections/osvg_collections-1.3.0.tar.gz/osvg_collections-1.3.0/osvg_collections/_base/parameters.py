"""
Module to provide a Base parameter classes
"""

from typing import TypedDict
import osvg


class ExtraStyledElementParameters(TypedDict):
    """
    Parameter class for element classes based classes without upstream style parameter
    """

    parent: osvg.SVG | osvg.Group
    position: osvg.Position = None
    name: str = None
    layer: int = 0
    rotation: float | osvg.float.Float = 0
    hyperlink: str = None
    border_color: str
    fill_color: str
    joints_color: str
