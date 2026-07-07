# -*- coding: utf-8 -*-
"""Align selected elements to the vertical centerline, or to a pinned reference element."""

from align_utils.commands import run_align

doc = __revit__.ActiveUIDocument.Document

if __name__ == '__main__':
    run_align(doc, "Center V", "x", "center")
