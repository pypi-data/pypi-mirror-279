"""
Module to provide network cloud shapes.
"""

from xml.etree import ElementTree as ET
from typing_extensions import Unpack
import osvg
import osvg.elements.rectanglebase
import osvg_collections._base.rotated_group


class Cloud(
    osvg.elements.rectanglebase.RectangleBase,
    osvg_collections._base.rotated_group.RotatedGroupShape,  # pylint: disable=protected-access
):
    """
    Class for firewall shapes.
    """

    # pylint: disable=too-few-public-methods

    def __init__(
        self, **kwargs: Unpack[osvg.elements.rectanglebase.RectangleBaseParams]
    ) -> None:
        self.stroke_color = kwargs.get("stroke_color", "000000")
        self.stroke_width_shape = kwargs.get("stroke_width", 1)
        self.fill_color = kwargs.get("fill_color", "none")
        super().__init__(**kwargs)

    @property
    def _plain_etree_element(self) -> ET.Element:
        """
        Create ET for this firewall shape
        """
        # pylint: disable=too-many-locals,too-many-statements
        # Create Group
        g = self.get_group_element(style=self.style_obj)
        #
        # Define positions which do not rotate
        #
        top_left = self.position + (
            -self.width / 2,
            -self.height / 2,
        )
        bottom_left = self.position + (
            -self.width / 2,
            self.height / 2,
        )
        top_center = osvg.YShiftedPosition(
            origin=self.position, y_shift=-self.height / 2
        )
        bottom_center = osvg.YShiftedPosition(
            origin=self.position, y_shift=self.height / 2
        )
        #
        # Define basic position shifts
        #
        y_shift_out_upper = self.height / 4
        y_shift_out_lower = self.height - y_shift_out_upper
        y_shift_inner_upper = self.height / 8
        y_shift_inner_lower = -y_shift_inner_upper
        x_shift_left_out = self.width / 6
        x_shift_right_out = self.width - x_shift_left_out
        #
        # Draw left bow
        #
        left_bow_start = top_left + (x_shift_left_out, y_shift_out_lower)
        path = osvg.Path(parent=g, position=left_bow_start)
        left_upper_bow_start = top_left + (x_shift_left_out, y_shift_out_upper)
        path.add_path_element(
            osvg.PathA(
                position=left_upper_bow_start,
                width=x_shift_left_out,
                height=self.height / 4,
                long_bow=False,
            )
        )
        #
        # Draw upper left bow
        #
        right_upper_bow_start = osvg.YShiftedPosition(
            origin=top_center, y_shift=y_shift_inner_upper
        )
        path.add_path_element(
            osvg.PathC(
                position1=osvg.XShiftedPosition(
                    origin=top_left, x_shift=x_shift_left_out
                ),
                position2=top_center,
                position3=right_upper_bow_start,
            )
        )
        #
        # Draw upper right bow
        #
        right_bow_start = top_left + (x_shift_right_out, y_shift_out_upper)
        path.add_path_element(
            osvg.PathC(
                position1=top_center,
                position2=osvg.XShiftedPosition(
                    origin=top_left, x_shift=x_shift_right_out
                ),
                position3=right_bow_start,
            )
        )
        #
        # Draw right bow
        #
        right_lower_bow_start = top_left + (x_shift_right_out, y_shift_out_lower)
        path.add_path_element(
            osvg.PathA(
                position=right_lower_bow_start,
                width=x_shift_left_out,
                height=self.height / 4,
                long_bow=False,
                right_bend=True,
            )
        )
        #
        # Draw lower right bow
        #
        left_lower_bow_start = osvg.YShiftedPosition(
            origin=bottom_center, y_shift=y_shift_inner_lower
        )
        path.add_path_element(
            osvg.PathC(
                position1=osvg.XShiftedPosition(
                    origin=bottom_left, x_shift=x_shift_right_out
                ),
                position2=bottom_center,
                position3=left_lower_bow_start,
            )
        )
        #
        # Draw lower left bow
        #
        path.add_path_element(
            osvg.PathC(
                position1=bottom_center,
                position2=osvg.XShiftedPosition(
                    origin=bottom_left, x_shift=x_shift_left_out
                ),
                position3=left_bow_start,
            )
        )
        #
        # Close Path
        #
        path.add_path_element(osvg.PathZ())
        return g.etree_element
