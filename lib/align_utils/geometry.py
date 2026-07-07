# -*- coding: utf-8 -*-
"""Bounding box and geometry utilities."""

from collections import namedtuple

from Autodesk.Revit.DB import XYZ


#: An element's bounding box projected onto one view axis.
Record = namedtuple("Record", "element min max center size")


def get_element_bbox(element, view=None):
    """Get bounding box in model coordinates.

    For view-specific elements (annotations), retrieves the bbox via
    the owning view then transforms to model coordinates if needed.
    For model elements, returns the standard model-space bbox.

    Args:
        element: Revit Element.
        view: Active view (used for view-specific elements).

    Returns:
        BoundingBoxXYZ or None.  Min/Max are in model coordinates.
    """
    if view and getattr(element, "ViewSpecific", False):
        bbox = element.get_BoundingBox(view)
        if bbox:
            # If the bbox has a non-identity transform, convert to model coords
            t = bbox.Transform
            if not t.IsIdentity:
                model_min = t.OfPoint(bbox.Min)
                model_max = t.OfPoint(bbox.Max)
                new_bbox = _make_bbox(model_min, model_max)
                return new_bbox
            return bbox
    bbox = element.get_BoundingBox(None)
    if bbox:
        t = bbox.Transform
        if not t.IsIdentity:
            model_min = t.OfPoint(bbox.Min)
            model_max = t.OfPoint(bbox.Max)
            return _make_bbox(model_min, model_max)
    return bbox


def _make_bbox(pt_a, pt_b):
    """Create an axis-aligned BoundingBoxXYZ from two arbitrary points."""
    from Autodesk.Revit.DB import BoundingBoxXYZ
    bb = BoundingBoxXYZ()
    bb.Min = XYZ(min(pt_a.X, pt_b.X), min(pt_a.Y, pt_b.Y), min(pt_a.Z, pt_b.Z))
    bb.Max = XYZ(max(pt_a.X, pt_b.X), max(pt_a.Y, pt_b.Y), max(pt_a.Z, pt_b.Z))
    return bb


def project_bbox(bbox, view, axis):
    """Project bbox min/max once onto a view axis."""
    direction = view.RightDirection if axis == "x" else view.UpDirection
    min_value = bbox.Min.DotProduct(direction)
    max_value = bbox.Max.DotProduct(direction)
    return (
        min_value,
        max_value,
        (min_value + max_value) / 2.0,
        max_value - min_value,
    )


def project_pairs(pairs, view, axis):
    """Project (element, bbox) pairs onto a view axis as Records."""
    return [
        Record(element, *project_bbox(bbox, view, axis))
        for element, bbox in pairs
    ]


def view_delta_to_model(dx_view, dy_view, view):
    """Convert a 2D view-space delta to a 3D model-space XYZ vector.

    Args:
        dx_view: movement along view horizontal (RightDirection).
        dy_view: movement along view vertical (UpDirection).
        view: Revit View.

    Returns:
        XYZ vector in model coordinates.
    """
    return view.RightDirection.Multiply(dx_view).Add(
        view.UpDirection.Multiply(dy_view)
    )
