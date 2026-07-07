# pyAlign Toolbar Layout

The ribbon is grouped by operation first, then by axis:

```text
pyAlign
|
+-- Align
|   +-- Horizontal: Left | Center V | Right
|   +-- Vertical:   Top  | Center H | Bottom
|
+-- Distribute
|   +-- Horizontal: Left Edges | Centers V | Right Edges
|   +-- Vertical:   Top Edges  | Centers H | Bottom Edges
|
+-- Justify
|   +-- Horizontal: Pack Left | Pack Center V | Pack Right
|   +-- Vertical:   Pack Top  | Pack Center H | Pack Bottom
|
+-- Space
    +-- Horizontal: Between H | Around H
    +-- Vertical:   Between V | Around V
```

Behavior summary:

```text
Align      = move all selected elements to one shared edge/centerline.
Distribute = spread selected element edges/centerlines evenly.
Justify    = pack selected elements together with no gap, anchored or centered.
Space      = equalize the gaps between/around selected elements.
```

Pinned elements:

```text
Align      = pinned element can act as the reference.
Other tools = pinned elements are not moved.
```
