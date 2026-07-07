# -*- coding: utf-8 -*-
"""Keep first and last selected elements fixed, then equalize horizontal gaps between them."""

from align_utils.commands import run_space

doc = __revit__.ActiveUIDocument.Document

if __name__ == '__main__':
    run_space(doc, "Between H", "x", "between")
