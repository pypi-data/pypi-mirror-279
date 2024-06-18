from typing import Collection, Tuple, Union

import shapely
from shapely import affinity

__all__ = ["compute_center_principal_axes", "buffer_principal_axis"]


def compute_center_principal_axes(
    poly: shapely.geometry.base.BaseGeometry,
) -> Tuple[shapely.LineString, shapely.LineString]:
    if not isinstance(poly, shapely.geometry.base.BaseGeometry):
        assert isinstance(
            poly, Collection
        ), f"{poly} was an collection of shapely objects"
        poly = shapely.unary_union(poly)

    poly: shapely.Polygon = poly.minimum_rotated_rectangle

    x, y = poly.exterior.coords.xy

    first_axis = shapely.LineString(
        [shapely.Point(x[0], y[0]), shapely.Point(x[1], y[1])]
    )
    other_axis = shapely.LineString(
        [shapely.Point(x[1], y[1]), shapely.Point(x[2], y[2])]
    )

    principal_axis = first_axis
    secondary_axis = other_axis

    if first_axis.length < other_axis.length:
        principal_axis, secondary_axis = secondary_axis, principal_axis

    x_off = poly.centroid.x - principal_axis.centroid.x
    y_off = poly.centroid.y - principal_axis.centroid.y

    return (
        affinity.translate(principal_axis, xoff=x_off, yoff=y_off),
        affinity.translate(secondary_axis, xoff=x_off, yoff=y_off),
    )


def buffer_principal_axis(
    poly: shapely.geometry.base.BaseGeometry, distance: float = 1.4
) -> Union[shapely.Polygon, shapely.MultiPolygon]:
    pax, sax = compute_center_principal_axes(poly)
    return shapely.buffer(
        pax,
        sax.length / distance,
        # single_sided=True,
        cap_style=shapely.BufferCapStyle.flat,
    )
