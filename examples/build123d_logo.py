"""

name: build123d_logo.py
by:   Gumyr
date: August 5th 2022

desc:

    This example creates the build123d logo.

license:

    Copyright 2022 Gumyr

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""
from build123d import *
import cadquery as cq

with BuildSketch() as logo_text:
    Text("123d", fontsize=10, valign=Valign.BOTTOM)
    font_height = logo_text.vertices().sort_by(SortBy.Y)[-1].y

with BuildSketch() as build_text:
    Text("build", fontsize=5, halign=Halign.CENTER)
    build_bb = BoundingBox(build_text.sketch, mode=Mode.PRIVATE)
    build_vertices = build_bb.vertices().sort_by(SortBy.X)
    build_width = build_vertices[-1].x - build_vertices[0].x

with BuildLine() as one:
    l1 = Line((font_height * 0.3, 0), (font_height * 0.3, font_height))
    TangentArc(l1 @ 1, (0, font_height * 0.7), tangent=(l1 % 1) * -1)

with BuildSketch() as two:
    PushPoints((font_height * 0.35, 0))
    Text("2", fontsize=10, valign=Valign.BOTTOM)

with BuildPart() as three_d:
    PushPoints((font_height * 1.1, 0))
    with BuildSketch():
        Text("3d", fontsize=10, valign=Valign.BOTTOM)
    Extrude(font_height * 0.3)
    logo_width = three_d.vertices().sort_by(SortBy.X)[-1].x

with BuildLine() as arrow_left:
    t1 = TangentArc((0, 0), (1, 0.75), tangent=(1, 0))
    Mirror(t1, axis=Axis.X)

ext_line_length = font_height * 0.5
dim_line_length = (logo_width - build_width - 2 * font_height * 0.05) / 2
with BuildLine() as extension_lines:
    l1 = Line((0, -font_height * 0.1), (0, -ext_line_length - font_height * 0.1))
    l2 = Line(
        (logo_width, -font_height * 0.1),
        (logo_width, -ext_line_length - font_height * 0.1),
    )
    PushPoints(l1 @ 0.5)
    Add(*arrow_left.line)
    PushPoints(l2 @ 0.5)
    Add(*arrow_left.line, rotation=180.0)
    Line(l1 @ 0.5, l1 @ 0.5 + cq.Vector(dim_line_length, 0))
    Line(l2 @ 0.5, l2 @ 0.5 - cq.Vector(dim_line_length, 0))

# Precisely center the build Faces
with BuildSketch() as build:
    PushPoints(
        (l1 @ 0.5 + l2 @ 0.5) / 2
        - cq.Vector((build_vertices[-1].x + build_vertices[0].x) / 2, 0)
    )
    Add(build_text.sketch)

logo = cq.Assembly(None, name="logo")
logo.add(one.line_as_wire, name="one")
logo.add(two.sketch, name="two")
logo.add(three_d.part, name="three_d")
for line in extension_lines.line:
    logo.add(line)
logo.add(build.sketch, name="build")
logo.save("logo.step")
cq.exporters.export(
    logo.toCompound(),
    "logo.svg",
    opt={
        # "width": 300,
        # "height": 300,
        # "marginLeft": 10,
        # "marginTop": 10,
        "showAxes": False,
        # "projectionDir": (0.5, 0.5, 0.5),
        "strokeWidth": 0.1,
        # "strokeColor": (255, 0, 0),
        # "hiddenColor": (0, 0, 255),
        "showHidden": False,
    },
)

if "show_object" in locals():
    show_object(one.line, name="one")
    show_object(two.sketch, name="two")
    show_object(three_d.part, name="three_d")
    show_object(extension_lines.line, name="extension_lines")
    show_object(build.sketch, name="build")