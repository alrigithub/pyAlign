# -*- coding: utf-8 -*-
"""Selection validation and pinned-element reference utilities."""

from Autodesk.Revit.DB import View3D


def _alert(message, exitscript=False):
    from pyrevit import forms
    forms.alert(message, exitscript=exitscript)


def check_view(view):
    """Exit script if the active view is a 3D view."""
    if isinstance(view, View3D):
        _alert("Alignment is not supported in 3D views.", exitscript=True)


def get_pinned_reference(pairs):
    """Return the pinned element's bbox to use as alignment reference.

    Args:
        pairs: list of (element, bbox) tuples.

    Returns:
        BoundingBoxXYZ of the single pinned element, or None if no
        pinned elements exist.  Prompts the user to choose when
        multiple pinned elements are found.
    """
    pinned = [(el, bb) for el, bb in pairs if getattr(el, "Pinned", False)]
    if len(pinned) == 0:
        return None
    if len(pinned) == 1:
        return pinned[0][1]
    # Multiple pinned elements — ask the user to pick one
    from pyrevit import forms
    options = {
        "Element {} (id {})".format(
            getattr(el, "Name", el.Category.Name if el.Category else "?"),
            el.Id.Value,
        ): bb
        for el, bb in pinned
    }
    chosen = forms.SelectFromList.show(
        sorted(options.keys()),
        title="Multiple Pinned Elements",
        message="Select which pinned element to align to:",
        button_name="Use as Reference",
    )
    if not chosen:
        _alert("No reference selected.", exitscript=True)
    return options[chosen]
