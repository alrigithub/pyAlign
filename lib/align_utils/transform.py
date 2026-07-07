# -*- coding: utf-8 -*-
"""Element movement utilities."""

from Autodesk.Revit.DB import XYZ, ElementTransformUtils


def move_element(doc, element, dx=0.0, dy=0.0, dz=0.0, delta=None):
    """Move an element by the given delta, handling annotation types.

    Detects TextNote/TextElement (uses .Coord), IndependentTag (uses
    .TagHeadPosition), and falls back to ElementTransformUtils for
    everything else including Dimensions.

    Args:
        doc: Revit Document.
        element: Revit Element to move.
        dx: Translation along X in feet (ignored if delta provided).
        dy: Translation along Y in feet (ignored if delta provided).
        dz: Translation along Z in feet (ignored if delta provided).
        delta: XYZ vector. If provided, overrides dx/dy/dz.
    """
    if delta is None:
        delta = XYZ(dx, dy, dz)

    if abs(delta.X) < 1e-9 and abs(delta.Y) < 1e-9 and abs(delta.Z) < 1e-9:
        return

    type_name = type(element).__name__

    if type_name in ("TextNote", "TextElement"):
        element.Coord = element.Coord.Add(delta)
    elif type_name == "IndependentTag":
        element.TagHeadPosition = element.TagHeadPosition.Add(delta)
    else:
        ElementTransformUtils.MoveElement(doc, element.Id, delta)
