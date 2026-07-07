# -*- coding: utf-8 -*-
"""Pack selected elements together vertically and center the packed group."""

from align_utils.commands import run_justify

doc = __revit__.ActiveUIDocument.Document

if __name__ == '__main__':
    run_justify(doc, "Pack Center H", "y", "center")
