# -*- coding: utf-8 -*-
"""Pack selected elements together vertically from the top edge."""

from align_utils.commands import run_justify

doc = __revit__.ActiveUIDocument.Document

if __name__ == '__main__':
    run_justify(doc, "Pack Top", "y", "start")
