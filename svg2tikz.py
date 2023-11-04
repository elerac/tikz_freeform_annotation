import argparse
import xml.etree.ElementTree as ET
from utils import path_to_tikz, rect_to_tikz


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=ET.parse)
    args = parser.parse_args()
    tree = args.input
    root = tree.getroot()

    indent = " " * 4

    filename_image = "path to image"

    # get the svg dimensions
    viewbox = root.attrib["viewBox"]
    min_x, min_y, max_x, max_y = map(float, viewbox.split(" "))
    width = max_x - min_x
    height = max_y - min_y

    code = ""
    code += f"\\begin{{tikzpicture}}[x=\\linewidth/{max(width, height):.3f}, y=-\\linewidth/{max(width, height):.3f}, transform shape]\n"

    # image
    code += indent + f"\\node[above right, inner sep=0] (image) at (0,0) {{\\includegraphics[width=\\hsize]{{{filename_image}}}}};\n"

    code += indent + "\\begin{scope}[shift={(image.north west)}]\n"

    for rect in root.findall(".//{http://www.w3.org/2000/svg}rect"):
        code += indent * 2 + rect_to_tikz(rect)

    for path in root.findall(".//{http://www.w3.org/2000/svg}path"):
        code += indent * 2 + path_to_tikz(path)

    # text with arrow (arrow starts from the north west corner of the text box and ends at the specified coordinate (arrow_x, arrow_y))
    box_x = 2.0
    box_y = 3.0
    arrow_x = 100.0
    arrow_y = 120.0
    text = "Text"
    arrow_color = "red, thick"
    # print(f"        \\node[draw, align=center, anchor=north west] at ({box_x:.3f}, {box_y:.3f}) {{{text}}} edge[-latex, {arrow_color}] ({arrow_x:.3f}, {arrow_y:.3f});")

    code += indent + "\\end{scope}\n"
    code += "\\end{tikzpicture}\n"

    # \node[draw, green, align=center, anchor=north west] at (10.000, 10.000) {Metal plate} edge[-latex, green, thick] (150.000, 120.000);
    #         \node[draw, red, align=center, anchor=north west] at (450.000, 400.000) {Bunny} edge[-latex, red, thick] (400.000, 380.000);
    print(code)


if __name__ == "__main__":
    main()
