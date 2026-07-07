# -*- coding: utf-8 -*-
"""Equalize horizontal space around each selected element, with half-gaps at the outer edges."""

from align_utils.commands import run_space

doc = __revit__.ActiveUIDocument.Document

if __name__ == '__main__':
    run_space(doc, "Around H", "x", "around")
