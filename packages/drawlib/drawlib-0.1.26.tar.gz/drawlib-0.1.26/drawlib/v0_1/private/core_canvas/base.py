# Copyright (c) 2024 Yuichi Ito (yuichi@yuichi.com)
#
# This software is licensed under the Apache License, Version 2.0.
# For more information, please visit: https://github.com/yuichi110/drawlib
#
# This software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.

"""Base canvas features.

This modules define CanvasBase which is base class of Canvas features.
Each canvas features are aggregated on Canvas.

"""

# pylint: disable=redefined-outer-name
# pylint: disable=too-many-arguments
# pylint: disable=too-many-instance-attributes
# pylint: disable=too-many-public-methods

# !!! Temporary Lint Escape !!!
# pylint: disable=unnecessary-ellipsis
# pylint: disable=unused-argument


import math
from typing import Final, Union, Optional, List, Tuple
import matplotlib.font_manager
import matplotlib.artist
import matplotlib.lines
import matplotlib.text
from matplotlib.path import Path
from matplotlib.patches import PathPatch
from matplotlib import pyplot
from matplotlib.patches import FancyBboxPatch
import matplotlib as mpl

import PIL.Image

from drawlib.v0_1.private.core.theme import dtheme
from drawlib.v0_1.private.util import (
    error_handler,
    get_center_and_size,
    minus_2points,
)
from drawlib.v0_1.private.core.model import (
    LineStyle,
    ShapeStyle,
    ShapeTextStyle,
)
from drawlib.v0_1.private.core.colors import Colors
from drawlib.v0_1.private.core.dimage import Dimage
from drawlib.v0_1.private.core.util import ShapeUtil
from drawlib.v0_1.private.validators.args import validate_args


class CanvasBase:
    """Base class of Canvas and its features.

    This class is designed for diamond inheritance.

    """

    DEFAULT_WIDTH: Final[int] = 100
    DEFAULT_HEIGHT: Final[int] = 100
    DEFAULT_DPI: Final[int] = 100
    DEFAULT_GRID: Final[bool] = False
    DEFAULT_GRID_ONLY: Final[bool] = False
    DEFAULT_GRID_STYLE: Final[LineStyle] = LineStyle(width=1, color=Colors.Gray, style="dashed")
    DEFAULT_GRID_CENTERSTYLE: Final[LineStyle] = LineStyle(width=2, color=Colors.Gray, style="dashed")

    @error_handler
    def __init__(self) -> None:
        """Initialize Canvas instance with default params.

        Not only first initialization, it is called from ``clear()``.
        Variables are updated on ``config()``.

        Returns:
            None

        """

        self._width = self.DEFAULT_WIDTH
        self._height = self.DEFAULT_HEIGHT
        self._dpi = self.DEFAULT_DPI
        self._background_color: Union[
            Tuple[int, int, int],
            Tuple[int, int, int, float],
            None,
        ] = None  # apply theme default later if no update
        self._background_alpha: Optional[float] = None  # apply theme default later if no update
        self._grid = self.DEFAULT_GRID
        self._grid_only = self.DEFAULT_GRID_ONLY
        self._grid_style = self.DEFAULT_GRID_STYLE
        self._grid_centerstyle = self.DEFAULT_GRID_CENTERSTYLE
        self._grid_xpitch: Optional[int] = None
        self._grid_ypitch: Optional[int] = None
        self._artists: List[matplotlib.artist.Artist] = []

        # it is decleared only for typing system
        self._fig = pyplot.figure()
        self._ax = self._fig.add_subplot(1, 1, 1)

        # initialize fig and ax
        self.config()

    ##############
    ### basics ###
    ##############

    @error_handler
    def clear(self) -> None:
        """Initialize drawlib Canvas config

        Initialize drawlib Canvas completely.
        It will wipe params which are set by config().
        And also, all drawing states.

        Returns:
            None

        Note:
            ``clear()`` doesn't make theme default.
            If you want to change theme to default, please call ``config(theme="default")`` after ``clear()``.

        """

        pyplot.close()
        # pylint: disable=unnecessary-dunder-call
        CanvasBase.__init__(self)  # type: ignore[misc]
        # pylint: enable=unnecessary-dunder-call

    @error_handler
    def config(
        self,
        width: Optional[int] = None,
        height: Optional[int] = None,
        dpi: Optional[int] = None,
        background_color: Union[
            Tuple[int, int, int],
            Tuple[int, int, int, float],
            None,
        ] = None,
        background_alpha: Optional[float] = None,
        grid: Optional[bool] = None,
        grid_only: Optional[bool] = None,
        grid_style: Optional[LineStyle] = None,
        grid_centerstyle: Optional[LineStyle] = None,
        grid_xpitch: Optional[int] = None,
        grid_ypitch: Optional[int] = None,
    ) -> None:
        """Configure drawlib Canvas

        Configure drawlib canvas parameters.
        Parameters will be wiped when ``clear()`` method is called except ``theme``.
        You can call this function many times.

        Args:
            width(optional): Width of canvas. default is 100
            height(optional): Height of canvas. default is 100
            dpi(optional): Output image resolution. default is 100
            theme(optional): Choose draw theme. ``clear()`` doesn't initialize this.
            background_color(optional): Background color. default is "white"
            background_alpha(optional): Background alpha. between 0~1. default is 1.0
            grid(optional): show grid for checking coordinate on True
            grid_style(optional): Style of grid line. default is dashed gray. Setting this will set `grid=True` automatically.
            grid_centerstyle(optional): Style of grid line. default is thick dashed gray. Setting this will set `grid=True` automatically.

        Returns:
            None

        Note:
            Calling config after drawing raise RuntimeError.
            It is because few drawing action uses Canvas size and dpi etc.
            Changing them after drawing will mess the drawing status.
            You can call config() again after calling clear().

        """

        # This method config() can be called repeatedly.
        # Please don't set default value in args
        # but set it at __init__() at first and clear().

        validate_args(locals(), argnames_accept_none=list(locals().keys()))
        if len(self._artists) != 0:
            raise RuntimeError(
                "config() must be called before drawing. "
                "Please call clear() first if you want to "
                "initialize drawing configs and states."
            )

        def config_size_dpi():
            size_dpi_changed = False
            if width is not None:
                self._width = width
            if height is not None:
                self._height = height
            if dpi is not None:
                self._dpi = dpi

            # set fig size. width is always 10
            fig_width = 10
            fig_hight = self._height * 10 / self._width
            self._fig = pyplot.figure(
                figsize=(fig_width, fig_hight),
                dpi=self._dpi,
            )

            # set ax size
            self._ax = self._fig.add_subplot(1, 1, 1)
            self._ax.set_xlim(0, self._width)
            self._ax.set_ylim(0, self._height)
            self._ax.set_aspect("equal")
            self._ax.axis("off")
            self._ax.margins(0, 0)

        def config_background():
            if background_color is not None:
                self._background_color = background_color
            if background_alpha is not None:
                self._background_alpha = background_alpha

        def config_grid():
            if grid_style is not None:
                self._grid = True
                self._grid_style = grid_style
                if grid_centerstyle is None:
                    self._grid_centerstyle = grid_style

            if grid_centerstyle is not None:
                self._grid = True
                self._grid_centerstyle = grid_centerstyle

            if grid_only is not None:
                self._grid_only = grid_only
                if grid_only:
                    self._grid = True

            if grid_xpitch is not None:
                self._grid_xpitch = grid_xpitch

            if grid_ypitch is not None:
                self._grid_ypitch = grid_ypitch

            if grid is not None:
                self._grid = grid

            # grid is drawn at method _render()

        pyplot.close()
        config_size_dpi()
        config_background()
        config_grid()

    #######################
    ### low level shape ###
    #######################

    def shape(
        self,
        xy: Tuple[float, float],
        path_points: List[
            Union[
                Tuple[float, float],
                Tuple[Tuple[float, float], Tuple[float, float]],
                Tuple[Tuple[float, float], Tuple[float, float], Tuple[float, float]],
            ]
        ],
        angle: float = 0.0,
        style: Union[ShapeStyle, str, None] = None,
        text: str = "",
        textsize: Optional[float] = None,
        textstyle: Optional[ShapeTextStyle] = None,
        is_default_center: bool = False,
    ) -> None:
        """Draw basic shape.

        This function is useful for drawing user original shapes.
        Please check document and example for details.

        Args:
            xy: start point
            path_points: xy and bezier control points.
            angle(optional): shape angle.
            style(optional): shape style.
            text(optional): text of shape.
            textstyle(optional): text style.
            is_default_center: make (x, y) center of shape.

        Returns:
            None

        """

        validate_args(locals())
        style, textstyle = ShapeUtil.format_styles(
            style,
            textstyle,
            dtheme.shapestyles.get,
            dtheme.shapetextstyles.has,
            dtheme.shapetextstyles.get,
        )
        if textsize is not None:
            textstyle.size = textsize

        # helper

        def get_rotate_point(
            xy: Tuple[float, float], angle: float, move_x: float, move_y: float
        ) -> Tuple[float, float]:
            x = xy[0]
            y = xy[1]
            angle_rad = math.radians(angle)
            x_rotated = x * math.cos(angle_rad) - y * math.sin(angle_rad)
            y_rotated = x * math.sin(angle_rad) + y * math.cos(angle_rad)
            return x_rotated + move_x, y_rotated + move_y

        # shift to center (0, 0)
        points_without_cp = []
        for pp in path_points:
            if not isinstance(pp[0], tuple):
                points_without_cp.append(pp)
            else:
                points_without_cp.append(pp[0])
        center, (width, height) = get_center_and_size(points_without_cp)

        path_points2 = []
        for pp in path_points:

            # (x, y)
            if not isinstance(pp[0], tuple):
                xy1 = minus_2points(pp, center)
                path_points2.append(xy1)
                continue

            # ((x1, y1), (x2, y2))
            xy1 = minus_2points(pp[0], center)
            xy2 = minus_2points(pp[1], center)
            if len(pp) == 2:
                path_points2.append((xy1, xy2))
                continue

            # ((x1, y1), (x2, y2), (x3, y3))
            xy3 = minus_2points(pp[2], center)
            path_points2.append((xy1, xy2, xy3))

        # alignment
        if is_default_center:
            # move to center
            x, y = xy
            x -= width / 2
            y -= height / 2
            xy = (x, y)
        ((x, y), style) = ShapeUtil.apply_alignment(
            xy,
            width,
            height,
            angle,
            style,
            is_default_center=is_default_center,
        )

        # rotate and move
        cx = x + width / 2
        cy = y + height / 2
        path_points3 = []
        for pp in path_points2:
            # (x, y)
            if not isinstance(pp[0], tuple):
                xy1 = get_rotate_point(pp, angle=angle, move_x=cx, move_y=cy)
                path_points3.append(xy1)
                continue

            # ((x1, y1), (x2, y2))
            xy1 = get_rotate_point(pp[0], angle=angle, move_x=cx, move_y=cy)
            xy2 = get_rotate_point(pp[1], angle=angle, move_x=cx, move_y=cy)
            if len(pp) == 2:
                path_points3.append((xy1, xy2))
                continue

            # ((x1, y1), (x2, y2), (x3, y3))
            xy3 = get_rotate_point(pp[2], angle=angle, move_x=cx, move_y=cy)
            path_points3.append((xy1, xy2, xy3))

        # create Path
        vertices = [path_points3[0]]
        codes = [Path.MOVETO]
        for p in path_points3[1:]:
            length = len(p)
            if length not in [2, 3]:
                raise ValueError()

            if not isinstance(p[0], tuple):
                vertices.append(p)
                codes.append(Path.LINETO)
                continue
            elif length == 2:
                vertices.extend([p[0], p[1]])
                codes.extend([Path.CURVE3] * 2)
            else:
                vertices.extend([p[0], p[1], p[2]])
                codes.extend([Path.CURVE4] * 3)
        vertices.append(path_points3[0])
        codes.append(Path.CLOSEPOLY)
        path = Path(vertices=vertices, codes=codes)

        # create PathPatch

        options = ShapeUtil.get_shape_options(style)
        self._artists.append(PathPatch(path=path, **options))

        # create Text

        if text is not None:
            self._artists.append(
                ShapeUtil.get_shape_text(
                    xy=(cx, cy),
                    text=text,
                    angle=angle,
                    style=textstyle,
                )
            )

    @error_handler
    def rectangle(
        self,
        xy: Tuple[float, float],
        width: float,
        height: float,
        r: float = 0.0,
        angle: Union[int, float] = 0.0,
        style: Union[ShapeStyle, str, None] = None,
        text: str = "",
        textsize: Optional[float] = None,
        textstyle: Union[ShapeTextStyle, str, None] = None,
    ) -> None:
        """Draw rectangle

        Args:
            xy: left bottom of rectangle.
            width: width of rounded rectangle.
            height: height of rounded rectangle.
            r(optional): size of R. default is 0.0.
            angle(optional): rotate rectangle with specified angle. Requires Matplotlib's ax to achieve it.
            style(optional): style of rounded rectangle.
            text(optional): text which is shown at center of rounded rectangle.
            textstyle(optional): style of text.

        Returns:
            None

        """

        validate_args(locals())
        style, textstyle = ShapeUtil.format_styles(
            style,
            textstyle,
            dtheme.rectanglestyles.get,
            dtheme.rectangletextstyles.has,
            dtheme.rectangletextstyles.get,
        )

        if r == 0:
            p1 = (0, 0)
            p2 = (0, height)
            p3 = (width, height)
            p4 = (width, 0)
            self.shape(
                xy=xy,
                path_points=[p1, p2, p3, p4],
                angle=angle,
                style=style,
                text=text,
                textsize=textsize,
                textstyle=textstyle,
            )
            return

        # left center
        p1 = (0, height / 2)

        # left top corner
        p2 = (0, height - r)
        p3 = ((0, height), (r, height))

        # right top corner
        p4 = (width - r, height)
        p5 = ((width, height), (width, height - r))

        # right bottom corner
        p6 = (width, r)
        p7 = ((width, 0), (width - r, 0))

        # left bottom corner
        p8 = (r, 0)
        p9 = ((0, 0), (0, r))

        self.shape(
            xy=xy,
            path_points=[p1, p2, p3, p4, p5, p6, p7, p8, p9],
            angle=angle,
            style=style,
            text=text,
            textsize=textsize,
            textstyle=textstyle,
        )

    #############
    ### dutil ###
    #############

    @error_handler
    def get_image_zoom_original(
        self,
    ) -> float:
        """Get matplot image zoom which keeps original pixel size.

        Returns:
            float: zoom

        """

        #
        # calcuration
        # 0.72 * 100 / dpi
        #

        zoom = 72 / self._dpi
        return zoom

    @error_handler
    def get_image_zoom_from_width(
        self,
        image: Union[str, PIL.Image.Image, Dimage],
        width: float,
    ) -> float:
        """Get matplot image zoom which is fit to specified width.

        Returns:
            float: zoom

        """

        #
        # calcuration
        # 0.72 * 10 * 100 * target_width / canvas_width / image_width
        #

        if not isinstance(image, Dimage):
            image = Dimage(image)

        image_width, _ = image.get_image_size()
        zoom = 720 * width / self._width / image_width
        return zoom

    @error_handler
    def get_charwidth_from_fontsize(
        self,
        size: float,
    ) -> float:
        """Get character width from font size..

        Args:
            size: font size

        Returns:
            float: width

        """

        MAGIC_NUMBER = 460  # todo: requires better calcuration
        width = size * 0.72 * self._width / MAGIC_NUMBER
        return width

    @error_handler
    def get_fontsize_from_charwidth(
        self,
        width: float,
    ) -> float:
        """Get font size which fit to provided width.

        Args:
            width: character width

        Returns:
            int: size

        """

        MAGIC_NUMBER = 540  # todo: requires better calcuration
        size = MAGIC_NUMBER * width / 0.72 / self._width
        return int(size)
