# -*- coding: utf-8 -*-
__title__ = "Between H"
__doc__ = """Keep first and last selected elements fixed, then equalize horizontal gaps between them."""
__author__ = "Alex Ritivoi"
__context__ = "selection"
__min_revit_ver__ = 2025
__max_revit_ver__ = 2026

from align_utils.commands import run_space

doc = __revit__.ActiveUIDocument.Document

if __name__ == '__main__':
    run_space(doc, __title__, "x", "between")
