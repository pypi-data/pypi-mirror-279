# Object-oriented Scalable Vector Graphics

## Table of Content

- [Installation](#installation)
- [Major Goals](#major-goals)
- [Principals](#principals)
  - [Float Values and Math](#float-values-and-math)
  - [Position Objects](#position-objects)
  - [SVG Element Objects](#svg-element-objects)
  - [SVG Group Objects](#svg-group-objects)
  - [Layers](#layers)
  - [SVG Object](#svg-object)
- [Basic Usage](#basic-usage)

## Installation

```code
pip install osvg
```

## Major Goals

- Provide a Python API to generate SVG XML code
- Use objects to handle SVG elements
- Implement relational positions and values

## Principals

### Float Values and Math

Each float value of a SVG element object is an object of a special Float
class or one of it's sub classes. A Float object can be
assigned to/referenced by another Float object. I.e you can reference
the width of a rectangle as the relative length of line. If you
change the rectangle width attribute you also change the value of
the line length. In addition there are Float classes for math. I.e.
a Sum class which sums up all referenced Float object values you added to.
If one of the referenced object changes the value of the Sum changes.

### Position Objects

A Position object has two Float object attributes: x and y.
X and y can be referenced to other element's Float attributes or other
postion's x and y attributes.
In addition a position can be reference to another position or
special position object, which
implements some operation in the two-dimensal space. I.e PolarShiftedPosition
represents a position which is shifted in direction of a given angle and by
a given distance. Angle and distance are also Float object attributes and can
be referenced to other element's Float attributes
(or calculated by Float math objects).

### SVG Element Objects

Each SVG element has a coresponding Python class.
Each object has attributes representing SVG element attributes and
additional attributes to improve the handling of the objects/elements within
your Python code. SVG element attributes which are floating numbers
or strings with floating number within, are object attributes based on
Float objects. Thus the attributes can be a reference to other element's
attribute or can be calculated with Float math objects from other elements'
attributes.  
A given position for a SVG area element object
is always the center of the area. This differs to the top left
corner idea of a i.e. rectangle in the SVG code. The rectangle object automatically
handles the shift for the SVG XML code.

### SVG Group Objects

All SVG element object should be a 'child' to a SVG Group object or
another SVG element object. If not, the element won't be included in
the SVG XML code. A Group object can be a child to another Group object.
The attributes 'rotation' and 'style' are inherited to child elements.
Rotation of the child element is the sum of element's rotation and
the inherited rotation. Style can be overwritten/changed be the child.
Only the delta of the style to the inherited style will be within the
SVG XML code for this element.

### Layers

By default SVG elements will be added to the SVG XML code in the
order they are added as childs to a group. You can adjust this
with the layer integer attribute of the SVG element object. A higher
layer value will add the element earlier to SVG XML code - bringing
it to the background of a drawing. A lower
layer value will add the element later to SVG XML code - bringing
it to the foreground of a drawing. Layer default value is 0. Negative
values are allowed.

### SVG Object

The SVG object is Group object and the root for the drawing.
The SVG object is the only SVG element object which can have
a 'viewbox' to allow an easy usage of fixed float values for the
attributes of the elements within the drawing and a easy scaling
of the drawing.

## Basic Usage

The Python code:

```python
import osvg


svg = osvg.SVG(
    width=400,
    height=300,
    viewbox=osvg.ViewBox(width=800, height=600),
    style=osvg.Style(stroke_width=3, stroke_color="ff0044")
)
circle_center = osvg.Position(x=100, y=100)
rectangle_center = osvg.Position(x=400, y=200)
foreground = -100
osvg.Line(
    parent=svg,
    start=circle_center,
    end=rectangle_center,
    layer=foreground
)
circle = osvg.Circle(
    parent=svg,
    position=circle_center,
    radius=80,
    style=osvg.Style(fill_color="00ff00")
)
g1 = osvg.Group(parent=svg, style=osvg.Style(stroke_width=4))
rectangle = osvg.Rectangle(
    parent=g1,
    position=rectangle_center,
    width=400,
    height=circle.radius
)
print(svg.xml_string)
```

Will print this XML code:

```xml
<?xml version="1.0" ?>
<svg xmlns="http://www.w3.org/2000/svg" style="stroke:#ff0044;stroke-width:3" width="400" height="300" viewBox="0 0 800 600">
        <circle style="fill:#00ff00" cx="100" cy="100" r="80"/>
        <g style="stroke-width:4">
                <rect x="200" y="160" width="400" height="80"/>
        </g>
        <polyline points="100,100 400,200"/>
</svg>

```

Which is this drawing:

![Usage Example](usage_example.svg)

You can find more code and the corresponding output under
*test/system/*
