"""
Module to provide gerneric multi-point connector.
"""

from collections.abc import Iterable
from types import GeneratorType
from xml.etree import ElementTree as ET
from typing_extensions import Unpack
import osvg
from osvg.elements.line_marker import Marker
from osvg.elements.polyline import PolylineParams

# pylint: disable=too-few-public-methods,duplicate-code


def _parse_iterable_float_args(
    *args: osvg.float.Float | float | int,
) -> list[float]:
    """
    Returns a list of float values from given arguments.
    Generator or Iterable arguments are deflated.
    """
    if not args:
        raise ValueError("Missing arguments")
    if not args:
        raise ValueError("Missing arguments")
    values = []
    for arg in args:
        if isinstance(arg, (GeneratorType, Iterable)):
            values += list(arg)
        else:
            values.append(arg)
    return values


def _two_middle_values(
    *args: osvg.float.Float | float | int,
) -> tuple[float, float]:
    """
    Return the two middle values from the list of values. This is sorted before.
    If list element count is not even. The middle and the most nearest value (+1/-1 in the list)
    ist returned.
    """
    values = _parse_iterable_float_args(*args)
    # remove duplicate values and sort the values
    values = sorted(set(float(x) for x in values))
    element_count = len(values)
    if element_count == 1:
        return values[0], values[0]
    if element_count == 2:
        return tuple(values)
    if len(values) % 2:
        # Uneven list element count
        middle_index = int(len(values) / 2)
        value1 = values[middle_index]
        value2_candidate1 = values[middle_index - 1]
        value2_candidate2 = values[middle_index + 1]
        if value1 - value2_candidate1 < value2_candidate2 - value1:
            value2 = value2_candidate1
        else:
            value2 = value2_candidate2
        return tuple(sorted([value1, value2]))
    middle_left = int(len(values) / 2 - 1)
    return values[middle_left], values[middle_left + 1]


def _average(
    *args: osvg.float.Float | float | int,
) -> float:
    """
    Return the average of all values within the arguments.
    """
    values = _parse_iterable_float_args(*args)
    values = [float(x) for x in values]
    return sum(values) / len(values)


class _MPConnectorParams(PolylineParams):
    """
    Parameter definition for _Connector2P class.
    """

    percentage: osvg.float.Float | float | int = 50
    average: bool = False


class _MPConnector(osvg.Polyline):
    """
    Metaclass for right-angled connector among multiple positions.
    """

    # pylint: disable=missing-function-docstring

    percentage = osvg.float.FloatProperty()
    default_percentage = 50
    cross_connect_overhang_factor = 2

    def __init__(self, **kwargs: Unpack[_MPConnectorParams]) -> None:
        self.percentage = kwargs.pop("percentage", self.default_percentage)
        self.average = kwargs.pop("average", False)
        super().__init__(**kwargs)
        self.marker_class = None
        self.marker_options = None

    def add_marker(self, marker_class: Marker, **kwargs) -> None:
        self.marker_class = marker_class
        self.marker_options = kwargs

    def add_position(
        self, p: osvg.Position | Iterable[float | int, float | int]
    ) -> None:
        """
        Add another position to the multi-point connector
        """
        if not isinstance(p, osvg.Position):
            p = osvg.Position(*p)
        self.positions.append(p)


class MPConnectorHParams(_MPConnectorParams):
    """
    Parameter definition for MPConnectorH class.
    """

    absolute_y: osvg.float.Float | float | int = None


class MPConnectorH(_MPConnector):
    """
    Class for right-angled connector among multiple positions
    with a horizontal cross-connect.

    `percentage` is the relative y value for the cross-connection
    in the distance between the two middle positions. (Default=50)

    `average`- If true use the average of all y values of the given
    positions. (Ignores percentage parameter)

    `absolute_y` is an absolute y value for the cross-connection.
    (Ignores percentage and average parameters)
    """

    absolute_y = osvg.float.FloatProperty()

    def __init__(self, **kwargs: Unpack[MPConnectorHParams]) -> None:
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
        elif self.average:
            y = _average(p.y for p in self.positions)
        else:
            y1, y2 = _two_middle_values(p.y for p in self.positions)
            y = osvg.Min(y1, y2) + abs(float(y1 - y2)) * (self.percentage / 100)
        # Add cross-connector
        x_values = [p.x for p in self.positions]
        x1 = (
            osvg.Min(*x_values) - self.cross_connect_overhang_factor * self.stroke_width
        )
        x2 = (
            osvg.Max(*x_values) + self.cross_connect_overhang_factor * self.stroke_width
        )
        osvg.Line(parent=g, start=(x1, y), end=(x2, y))
        # Add line from each position to the cross-connector
        for p in self.positions:
            l = osvg.Line(parent=g, start=p, end=(p.x, y))
            if self.marker_class:
                l.add_start_marker(
                    marker_class=self.marker_class, **self.marker_options
                )
        return g.etree_element


class MPConnectorVParams(_MPConnectorParams):
    """
    Parameter definition for MPConnectorV class.
    """

    absolute_x: osvg.float.Float | float | int = None


class MPConnectorV(_MPConnector):
    """
    Class for right-angled connector among multiple positions
    with a vertical cross-connect.

    `percentage` is the relative x value for the cross-connection
    in the distance between the two middle positions. (Default=50)

    `average`- If true use the average of all y values of the given
    positions. (Ignores percentage parameter)

    `absolute_x` is an absolute x value for the cross-connection.
    (Ignores percentage and average parameters)
    """

    absolute_x = osvg.float.FloatProperty()

    def __init__(self, **kwargs: Unpack[MPConnectorVParams]) -> None:
        self.absolute_x = kwargs.pop("absolute_x", None)
        super().__init__(**kwargs)

    @property
    def _plain_etree_element(self) -> ET.Element:
        """
        Create ET for this connector
        """
        g = osvg.Group(name=self.name, style=self.style, layer=self.layer)
        # Calculate y value for cross-connect
        if self.absolute_x:
            x = self.absolute_x
        elif self.average:
            x = _average(p.x for p in self.positions)
        else:
            x1, x2 = _two_middle_values(p.x for p in self.positions)
            x = osvg.Min(x1, x2) + abs(float(x1 - x2)) * (self.percentage / 100)
        # Add cross-connector
        y_values = [p.y for p in self.positions]
        y1 = osvg.Min(*y_values) - self.cross_connect_overhang_factor * float(
            self.stroke_width
        )
        y2 = osvg.Max(*y_values) + self.cross_connect_overhang_factor * float(
            self.stroke_width
        )
        osvg.Line(parent=g, start=(x, y1), end=(x, y2))
        # Add line from each position to the cross-connector
        for p in self.positions:
            l = osvg.Line(parent=g, start=p, end=(x, p.y))
            if self.marker_class:
                l.add_start_marker(
                    marker_class=self.marker_class, **self.marker_options
                )
        return g.etree_element
