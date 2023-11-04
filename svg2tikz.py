import argparse
import xml.etree.ElementTree as ET
from utils import path_to_tikz, rect_to_tikz


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=ET.parse, help="input svg file")
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
        code += indent * 2 + rect_to_tikz(rect, draw_options="")

    for path in root.findall(".//{http://www.w3.org/2000/svg}path"):
        code += indent * 2 + path_to_tikz(path, draw_options="")

    code += indent + "\\end{scope}\n"
    code += "\\end{tikzpicture}\n"

    print(code)


if __name__ == "__main__":
    main()
