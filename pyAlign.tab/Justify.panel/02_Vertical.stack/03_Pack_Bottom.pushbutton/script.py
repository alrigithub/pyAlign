# -*- coding: utf-8 -*-
__title__ = "Pack Bottom"
__doc__ = """Pack selected elements together vertically against the bottom edge."""
__author__ = "Alex Ritivoi"
__context__ = "selection"
__min_revit_ver__ = 2025
__max_revit_ver__ = 2026

from align_utils.commands import run_justify

doc = __revit__.ActiveUIDocument.Document

if __name__ == '__main__':
    run_justify(doc, __title__, "y", "end")
