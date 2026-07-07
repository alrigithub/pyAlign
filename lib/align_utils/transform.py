# -*- coding: utf-8 -*-
"""Element movement utilities."""

from Autodesk.Revit.DB import ElementTransformUtils


def move_element(doc, element, delta):
    """Move an element by an XYZ delta, handling annotation types.

    TextNote/TextElement move via .Coord and IndependentTag via
    .TagHeadPosition; everything else (including Dimensions) falls
    back to ElementTransformUtils.

    Args:
        doc: Revit Document.
        element: Revit Element to move.
        delta: XYZ translation vector in feet.
    """
    if abs(delta.X) < 1e-9 and abs(delta.Y) < 1e-9 and abs(delta.Z) < 1e-9:
        return

    type_name = type(element).__name__

    if type_name in ("TextNote", "TextElement"):
        element.Coord = element.Coord.Add(delta)
    elif type_name == "IndependentTag":
        element.TagHeadPosition = element.TagHeadPosition.Add(delta)
    else:
        ElementTransformUtils.MoveElement(doc, element.Id, delta)
