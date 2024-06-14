from typing import Annotated

from numpy.typing import ArrayLike


class Config:
    """Triangulation configuration."""

    def __init__(self) -> None: ...

    def __repr__(self) -> str: ...

    @property
    def min_angle(self) -> float:
        """Minimum angle constraint in degrees."""

    @min_angle.setter
    def min_angle(self, arg: float, /) -> None: ...

    @property
    def max_area(self) -> float:
        """Maximum area constraint. Negative value means not set."""

    @max_area.setter
    def max_area(self, arg: float, /) -> None: ...

    @property
    def max_num_steiner(self) -> int:
        """Maximum number of Steiner points. Negative value means unlimited."""

    @max_num_steiner.setter
    def max_num_steiner(self, arg: int, /) -> None: ...

    @property
    def verbose_level(self) -> int:
        """Verbose level (0-4, 0 == quiet)."""

    @verbose_level.setter
    def verbose_level(self, arg: int, /) -> None: ...

    @property
    def algorithm(self) -> str:
        """Algorithm: "divide_and_conquer", "sweepline", "incremental""""

    @algorithm.setter
    def algorithm(self, arg: str, /) -> str: ...

    @property
    def convex_hull(self) -> bool:
        """Whether to keep convex hul"""

    @convex_hull.setter
    def convex_hull(self, arg: bool, /) -> None: ...

    @property
    def conforming(self) -> bool:
        """Whether to require conforming triangulation."""

    @conforming.setter
    def conforming(self, arg: bool, /) -> None: ...

    @property
    def exact(self) -> bool:
        """Whether to use exact arithmetic (strongly recommended)."""

    @exact.setter
    def exact(self, arg: bool, /) -> None: ...

    @property
    def split_boundary(self) -> bool:
        """Whether to allow splitting the boundary."""

    @split_boundary.setter
    def split_boundary(self, arg: bool, /) -> None: ...

    @property
    def auto_hole_detection(self) -> bool:
        """Whether to detect holes automatically based on winding number."""

    @auto_hole_detection.setter
    def auto_hole_detection(self, arg: bool, /) -> None: ...

class Engine:
    """Triangulation engine."""

    def __init__(self) -> None: ...

    @property
    def in_points(self) -> Annotated[ArrayLike, dict(dtype='float64', shape=(None, 2), order='C')]:
        """Input 2D point cloud to be triangulated or Voronoi diagrammed."""

    @in_points.setter
    def in_points(self, arg: Annotated[ArrayLike, dict(dtype='float64', shape=(None, 2), order='C')], /) -> None: ...

    @property
    def in_segments(self) -> Annotated[ArrayLike, dict(dtype='int32', shape=(None, 2), order='C')]:
        """Input segment constraints."""

    @in_segments.setter
    def in_segments(self, arg: Annotated[ArrayLike, dict(dtype='int32', shape=(None, 2), order='C')], /) -> None: ...

    @property
    def in_triangles(self) -> Annotated[ArrayLike, dict(dtype='int32', shape=(None, 3), order='C')]:
        """
        Input existing triangulation of the point cloud. Used for refining an existing triangulation.
        """

    @in_triangles.setter
    def in_triangles(self, arg: Annotated[ArrayLike, dict(dtype='int32', shape=(None, 3), order='C')], /) -> None: ...

    @property
    def in_holes(self) -> Annotated[ArrayLike, dict(dtype='float64', shape=(None, 2), order='C')]:
        """
        Input hole points. Used by triangle to flood and remove faces representing holes.
        """

    @in_holes.setter
    def in_holes(self, arg: Annotated[ArrayLike, dict(dtype='float64', shape=(None, 2), order='C')], /) -> None: ...

    @property
    def in_areas(self) -> Annotated[ArrayLike, dict(dtype='float64', shape=(None), order='C')]:
        """Input triangle area constraints. One area per triangle."""

    @in_areas.setter
    def in_areas(self, arg: Annotated[ArrayLike, dict(dtype='float64', shape=(None), order='C')], /) -> None: ...

    @property
    def in_point_markers(self) -> Annotated[ArrayLike, dict(dtype='int32', shape=(None), order='C')]:
        """Input point markers. One positive integer marker per point."""

    @in_point_markers.setter
    def in_point_markers(self, arg: Annotated[ArrayLike, dict(dtype='int32', shape=(None), order='C')], /) -> None: ...

    @property
    def in_segment_markers(self) -> Annotated[ArrayLike, dict(dtype='int32', shape=(None), order='C')]:
        """Input segment markers. One positive integer marker per segment."""

    @in_segment_markers.setter
    def in_segment_markers(self, arg: Annotated[ArrayLike, dict(dtype='int32', shape=(None), order='C')], /) -> None: ...

    @property
    def out_points(self) -> Annotated[ArrayLike, dict(dtype='float64', shape=(None, 2), order='C')]:
        """Output 2D point cloud."""

    @property
    def out_segments(self) -> Annotated[ArrayLike, dict(dtype='int32', shape=(None, 2), order='C')]:
        """Output segment constraints."""

    @property
    def out_triangles(self) -> Annotated[ArrayLike, dict(dtype='int32', shape=(None, 3), order='C')]:
        """Output triangulation."""

    @property
    def out_edges(self) -> Annotated[ArrayLike, dict(dtype='int32', shape=(None, 2), order='C')]:
        """Output edges."""

    @property
    def out_triangle_neighbors(self) -> Annotated[ArrayLike, dict(dtype='int32', shape=(None, 3), order='C')]:
        """Output triangle neighbors."""

    @property
    def out_point_markers(self) -> Annotated[ArrayLike, dict(dtype='int32', shape=(None), order='C')]:
        """Output point markers."""

    @property
    def out_segment_markers(self) -> Annotated[ArrayLike, dict(dtype='int32', shape=(None), order='C')]:
        """Output segment markers."""

    @property
    def out_edge_markers(self) -> Annotated[ArrayLike, dict(dtype='int32', shape=(None), order='C')]:
        """Output edge markers."""

    def run(self, arg: Config, /) -> None:
        """Run triangulation."""
