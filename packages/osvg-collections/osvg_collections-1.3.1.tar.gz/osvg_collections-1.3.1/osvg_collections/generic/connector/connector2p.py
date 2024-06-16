"""
Module to provide generic two point connector.
"""

from xml.etree import ElementTree as ET
from osvg.elements.line_marker import Marker
from typing_extensions import Unpack
import osvg
from osvg.elements.line import LineParams

# pylint: disable=too-few-public-methods,duplicate-code


class _Connector2PParams(LineParams):
    """
    Parameter definition for _Connector2P class.
    """

    percentage: osvg.float.Float | float | int = 50


class _Connector2P(osvg.Line):
    """
    Metaclass for right-angled connector between two positions.
    """

    # pylint: disable=missing-function-docstring

    percentage = osvg.float.FloatProperty()
    default_percentage = 50

    def __init__(self, **kwargs: Unpack[_Connector2PParams]) -> None:
        self.percentage = kwargs.pop("percentage", self.default_percentage)
        super().__init__(**kwargs)
        self.start_marker_class = None
        self.start_marker_options = None
        self.end_marker_class = None
        self.end_marker_options = None

    def add_start_marker(self, marker_class: Marker, **kwargs) -> None:
        self.start_marker_class = marker_class
        self.start_marker_options = kwargs

    def add_end_marker(self, marker_class: Marker, **kwargs) -> None:
        self.end_marker_class = marker_class
        self.end_marker_options = kwargs


class ConnectorHParams(_Connector2PParams):
    """
    Parameter definition for ConnectorH class.
    """

    absolute_y: osvg.float.Float | float | int = None


class ConnectorH(_Connector2P):
    """
    Class for right-angled connector between two positions
    with a horizontal cross-connect.

    `percentage` is the relative y value for the cross-connection
    in the distance between the two positions. (Default=50)

    `absolute_y` is an absolute y value for the cross-connection.
    (Ignores percentage parameter)
    """

    absolute_y = osvg.float.FloatProperty()

    def __init__(self, **kwargs: Unpack[ConnectorHParams]) -> None:
        self.absolute_y = kwargs.pop("absolute_y", None)
        super().__init__(**kwargs)

    @property
    def _plain_etree_element(self) -> ET.Element:
        """
        Create ET for this connector
        """
        g = osvg.Group(name=self.name, style=self.style, layer=self.layer)
        # Calculate y value for cross-connect
        if self.absolute_y:
            y = self.absolute_y
        else:
            start_y = self.start.y
            end_y = self.end.y
            y = osvg.Min(start_y, end_y) + osvg.float_math.Abs(start_y - end_y) * (
                self.percentage / 100
            )
        start_c = osvg.Position(x=self.start.x, y=y)
        end_c = osvg.Position(x=self.end.x, y=y)
        # Add line from start to cross-connect
        l1 = osvg.Line(parent=g, start=self.start, end=start_c)
        if self.start_marker_class:
            l1.add_start_marker(
                marker_class=self.start_marker_class, **self.start_marker_options
            )
        # Add cross-connect
        osvg.Line(
            parent=g,
            start=start_c,
            end=end_c,
        )
        # Add line from cross-connect to end
        l3 = osvg.Line(parent=g, start=end_c, end=self.end)
        if self.end_marker_class:
            l3.add_end_marker(
                marker_class=self.end_marker_class, **self.end_marker_options
            )
        return g.etree_element


class ConnectorVParams(_Connector2PParams):
    """
    Parameter definition for ConnectorV class.
    """

    absolute_x: osvg.float.Float | float | int = None


class ConnectorV(_Connector2P):
    """
    Class for right-angled connector between two positions
    with a vertical cross-connect.

    `percentage` is the relative x value for the cross-connection
    in the distance between the two positions. (Default=50)

    `absolute_x` is an absolute x value for the cross-connection.
    (Ignores percentage parameter)
    """

    absolute_x = osvg.float.FloatProperty()

    def __init__(self, **kwargs: Unpack[ConnectorVParams]) -> None:
        self.absolute_x = kwargs.pop("absolute_x", None)
        super().__init__(**kwargs)

    @property
    def _plain_etree_element(self) -> ET.Element:
        """
        Create ET for this connector
        """
        g = osvg.Group(name=self.name, style=self.style, layer=self.layer)
        # Calculate x value for cross-connect
        if self.absolute_x:
            x = self.absolute_x
        else:
            start_x = self.start.x
            end_x = self.end.x
            x = osvg.Min(start_x, end_x) + osvg.float_math.Abs(start_x - end_x) * (
                self.percentage / 100
            )
        start_c = osvg.Position(x=x, y=self.start.y)
        end_c = osvg.Position(x=x, y=self.end.y)
        # Add line from start to cross-connect
        l1 = osvg.Line(parent=g, start=self.start, end=start_c)
        if self.start_marker_class:
            l1.add_start_marker(
                marker_class=self.start_marker_class, **self.start_marker_options
            )
        # Add cross-connect
        osvg.Line(
            parent=g,
            start=start_c,
            end=end_c,
        )
        # Add line from cross-connect to end
        l3 = osvg.Line(parent=g, start=end_c, end=self.end)
        if self.end_marker_class:
            l3.add_end_marker(
                marker_class=self.end_marker_class, **self.end_marker_options
            )
        return g.etree_element
