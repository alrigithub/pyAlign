# -*- coding: utf-8 -*-
"""Shared command runners for toolbar alignment operations."""

from Autodesk.Revit.DB import Transaction
from pyrevit import revit

from align_utils.geometry import (
    get_element_bbox,
    project_bbox,
    project_pairs,
    view_delta_to_model,
)
from align_utils.selection import check_view, get_pinned_reference
from align_utils.transform import move_element


EL = 0
BBOX = 1
MIN = 2
MAX = 3
CENTER = 4
SIZE = 5

POINT_INDEX = {
    "min": MIN,
    "max": MAX,
    "center": CENTER,
}


def _alert(message, exitscript=False):
    from pyrevit import forms
    forms.alert(message, exitscript=exitscript)


def _get_records(doc, min_count, axis, selection_message, geometry_message):
    view = doc.ActiveView
    check_view(view)

    selection = revit.get_selection()
    elements = [element for element in selection.elements if element is not None]
    if len(elements) < min_count:
        _alert(selection_message, exitscript=True)

    pairs = []
    for element in elements:
        bbox = get_element_bbox(element, view)
        if bbox:
            pairs.append((element, bbox))

    if len(pairs) < min_count:
        _alert(geometry_message, exitscript=True)

    return view, pairs, project_pairs(pairs, view, axis)


def _delta_to_model(axis, amount, view):
    if axis == "x":
        return view_delta_to_model(amount, 0, view)
    return view_delta_to_model(0, amount, view)


def _commit_moves(doc, title, view, axis, moves):
    moves = [
        (element, amount)
        for element, amount in moves
        if not getattr(element, "Pinned", False) and abs(amount) > 1e-9
    ]
    if not moves:
        return

    transaction = Transaction(doc, title)
    transaction.Start()
    try:
        for element, amount in moves:
            move_element(doc, element, delta=_delta_to_model(axis, amount, view))
        transaction.Commit()
    except Exception as err:
        transaction.RollBack()
        _alert("Error: {}".format(str(err)))


def run_align(doc, title, axis, anchor):
    view, pairs, records = _get_records(
        doc,
        2,
        axis,
        "Select at least 2 elements.",
        "Need at least 2 elements with valid geometry.",
    )

    ref_bbox = get_pinned_reference(pairs)
    if ref_bbox:
        ref_min, ref_max, ref_center, _ = project_bbox(ref_bbox, view, axis)
        target = {"min": ref_min, "max": ref_max, "center": ref_center}[anchor]
    elif anchor == "min":
        target = min(record[MIN] for record in records)
    elif anchor == "max":
        target = max(record[MAX] for record in records)
    else:
        target = (
            min(record[MIN] for record in records)
            + max(record[MAX] for record in records)
        ) / 2.0

    index = POINT_INDEX[anchor]
    moves = [(record[EL], target - record[index]) for record in records]
    _commit_moves(doc, title, view, axis, moves)


def run_distribute(doc, title, axis, point):
    view, _, records = _get_records(
        doc,
        3,
        axis,
        "Select at least 3 elements to distribute.",
        "Need at least 3 elements with valid geometry.",
    )

    index = POINT_INDEX[point]
    records.sort(key=lambda record: record[index])

    count = len(records)
    first = records[0][index]
    last = records[-1][index]
    step = (last - first) / float(count - 1)

    moves = []
    for i, record in enumerate(records):
        target = first + i * step
        moves.append((record[EL], target - record[index]))

    _commit_moves(doc, title, view, axis, moves)


def run_justify(doc, title, axis, mode):
    view, _, records = _get_records(
        doc,
        2,
        axis,
        "Select at least 2 elements.",
        "Need at least 2 elements with valid geometry.",
    )

    # "start" means left/top in UI terms, but the projected scalar grows
    # upward on the vertical axis, so start/end swap sides for y.
    if axis == "y" and mode != "center":
        mode = "end" if mode == "start" else "start"

    records.sort(key=lambda record: record[CENTER])
    total_size = sum(record[SIZE] for record in records)

    if mode == "start":
        current = min(record[MIN] for record in records)
    elif mode == "end":
        current = max(record[MAX] for record in records) - total_size
    else:
        overall_center = (
            min(record[MIN] for record in records)
            + max(record[MAX] for record in records)
        ) / 2.0
        current = overall_center - total_size / 2.0

    moves = []
    for record in records:
        moves.append((record[EL], current - record[MIN]))
        current += record[SIZE]

    _commit_moves(doc, title, view, axis, moves)


def run_space(doc, title, axis, mode):
    view, _, records = _get_records(
        doc,
        3,
        axis,
        "Select at least 3 elements to distribute.",
        "Need at least 3 elements with valid geometry.",
    )

    records.sort(key=lambda record: record[CENTER])
    count = len(records)

    if mode == "between":
        container_min = records[0][MIN]
        container_max = records[-1][MAX]
        divisor = float(count - 1)
        edge_offset = 0.0
    else:
        container_min = min(record[MIN] for record in records)
        container_max = max(record[MAX] for record in records)
        divisor = float(count)
        edge_offset = 0.5

    total_size = sum(record[SIZE] for record in records)
    gap = ((container_max - container_min) - total_size) / divisor
    current = container_min + gap * edge_offset

    moves = []
    for record in records:
        moves.append((record[EL], current - record[MIN]))
        current += record[SIZE] + gap

    _commit_moves(doc, title, view, axis, moves)
