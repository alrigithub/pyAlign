# -*- coding: utf-8 -*-
"""Distribute selected elements by equal vertical spacing between horizontal centerlines."""

from align_utils.commands import run_distribute

doc = __revit__.ActiveUIDocument.Document

if __name__ == '__main__':
    run_distribute(doc, "Centers H", "y", "center")
