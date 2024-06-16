"""
Module to provide RotatedGroup class
"""

from xml.etree import ElementTree as ET
from typing_extensions import Unpack
import osvg
from osvg.elements.elementbase import SVGElementParams


class RotatedGroup(osvg.Group):
    # pylint: disable=too-few-public-methods
    """
    Sub-class to OSVG Group but which "isolates" sub elements from rotation of the group.
    """

    def __init__(self, **kwargs: Unpack[SVGElementParams]) -> None:
        super().__init__(**kwargs)
        self.group_rotation = self.element_rotation + self.parent_rotation
        self.rotation = 0

    def add_element_rotation(self, element: ET.ElementTree) -> None:
        """
        Add transform tag with rotation if required
        """
        if float(self.group_rotation) != 0:
            element.set(
                "transform",
                f"rotate({str(self.group_rotation)} {str(self.position.x)} {str(self.position.y)})",
            )

    @property
    def _plain_etree_element(self) -> ET.Element:
        element = super()._plain_etree_element
        self.add_element_rotation(element=element)
        return element


class RotatedGroupShape:
    # pylint: disable=no-member,too-few-public-methods
    """
    Base class for all shape classes using a rotated group to draw the shape.
    """

    def get_group_element(self, style: osvg.Style):
        """
        Get Group Element as "carrier" for shape's SVG elements
        """
        # Create Group
        return RotatedGroup(
            name=self.name,
            position=self.position,
            style=style,
            rotation=self.rotation,
            hyperlink=self.hyperlink,
        )
