# -*- coding: utf-8 -*-
__title__ = "Centers V"
__doc__ = """Distribute selected elements by equal horizontal spacing between vertical centerlines."""
__author__ = "Alex Ritivoi"
__context__ = "selection"
__min_revit_ver__ = 2025
__max_revit_ver__ = 2026

from align_utils.commands import run_distribute

doc = __revit__.ActiveUIDocument.Document

if __name__ == '__main__':
    run_distribute(doc, __title__, "x", "center")
