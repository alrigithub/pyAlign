# -*- coding: utf-8 -*-
__title__ = "Right"
__doc__ = """Align selected elements to the rightmost edge, or to a pinned reference element."""
__author__ = "Alex Ritivoi"
__context__ = "selection"
__min_revit_ver__ = 2025
__max_revit_ver__ = 2026

from align_utils.commands import run_align

doc = __revit__.ActiveUIDocument.Document

if __name__ == '__main__':
    run_align(doc, __title__, "x", "max")
