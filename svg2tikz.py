import argparse
import xml.etree.ElementTree as ET
from utils import path_to_tikz, rect_to_tikz


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=ET.parse, help="input svg file")
    args = parser.parse_args()
    tree = args.input
    root = tree.getroot()

    # settings
    indent = " " * 4
    color_palette = ["red", "green", "blue", "cyan", "magenta", "yellow", "brown", "lime", "olive", "orange", "pink", "purple", "teal", "violet"]
    filename_image = "path to image"

    # get the svg dimensions
    viewbox = root.attrib["viewBox"]
    min_x, min_y, max_x, max_y = map(float, viewbox.split(" "))
    width = max_x - min_x
    height = max_y - min_y

    # the number of digits of the maximum dimension
    g = len(str(int(max(width, height)))) + 1

    code = ""
    code += f"\\begin{{tikzpicture}}[x=\\linewidth/{max(width, height):.1f}, y=-\\linewidth/{max(width, height):.1f}, transform shape, scale=1.0]\n"
    code += indent + f"\\node[inner sep=0] (image) at (0,0) {{\\includegraphics[width=\\hsize]{{{filename_image}}}}};\n"
    code += indent + "\\begin{scope}[shift={(image.north west)}]\n"

    for path in root.findall(".//{http://www.w3.org/2000/svg}path"):
        color = color_palette.pop(0) if color_palette else ""
        code += indent * 2 + path_to_tikz(path, draw_options=f"{color}", g=g)

    for rect in root.findall(".//{http://www.w3.org/2000/svg}rect"):
        color = color_palette.pop(0) if color_palette else ""
        code += indent * 2 + rect_to_tikz(rect, draw_options=f"{color}", g=g)

    code += indent + "\\end{scope}\n"
    code += "\\end{tikzpicture}\n"

    print(code)


if __name__ == "__main__":
    main()
