from typing import List, Tuple
import xml.etree.ElementTree

# SVG path syntax:
# - https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/d


def next_number(string: str, start: int) -> Tuple[float, int]:
    end = start

    sign_found = False
    dot_found = False
    while True:
        # Out of bounds
        if end >= len(string):
            break

        # Sign
        if not sign_found and string[end] in "+-":
            sign_found = True
            end += 1
            continue

        # Dot
        if not dot_found and string[end] == ".":
            sign_found = True
            dot_found = True
            end += 1
            continue

        # Digit
        if string[end].isdigit():
            sign_found = True
            end += 1
            continue

        # Not a digit
        break

    try:
        number = float(string[start:end])
    except ValueError:
        raise ValueError(f"Invalid number: {string[start:end]}, start={start}, end={end}")

    return number, end


def next_multiple_numbers(string: str, start: int, n: int) -> Tuple[List[float], int]:
    numbers = []
    for i in range(n):
        number, start = next_number(string, start)
        numbers.append(number)

        if start >= len(string):
            break

        # if next character is a separator (not a digit or a letter or a sign), skip it
        c = string[start]
        if not c.isdigit() and not c.isalpha() and string[start] not in "+-.":
            start += 1  # skip the separator

    return numbers, start


def path_to_tikz(path: xml.etree.ElementTree.Element, draw_options: str = "") -> str:
    """Convert an SVG path to a TikZ path."""
    d = path.attrib["d"]
    class_name = path.attrib["class"]

    code = f"\\draw[{draw_options}] "

    i = 0  # index in d
    x = 0  # current x coordinate
    y = 0  # current y coordinate
    path_type = None
    is_first = True
    while i < len(d):
        c = d[i]

        if c.isalpha():
            path_type = c
            i += 1

        if path_type == "m":
            # svg: m dx dy
            # tikz: ++(dx, dy)
            (dx, dy), i = next_multiple_numbers(d, i, 2)
            x += dx
            y += dy
            code += f" -- ++({dx:.5g}, {dy:.5g})"
        elif path_type == "h":
            # svg: h dx
            # tikz: ++(dx, 0)
            (dx,), i = next_multiple_numbers(d, i, 1)
            x += dx
            code += f" -- ++({dx:.5g}, 0)"
        elif path_type == "H":
            # svg: H x
            # tikz: ++(x, 0)
            (x,), i = next_multiple_numbers(d, i, 1)
            code += f" -- ({x:.5g}, {y:.5g})"
        elif path_type == "v":
            # svg: v dy
            # tikz: ++(0, dy)
            (dy,), i = next_multiple_numbers(d, i, 1)
            y += dy
            code += f" -- ++(0, {dy:.5g})"
        elif path_type == "V":
            # svg: V y
            # tikz: ++(0, y)
            (y,), i = next_multiple_numbers(d, i, 1)
            code += f" -- ({x:.5g}, {y:.5g})"
        elif path_type == "l":
            # svg: l dx dy
            # tikz: ++(dx, dy)
            (dx, dy), i = next_multiple_numbers(d, i, 2)
            x += dx
            y += dy
            code += f" -- ++({dx:.5g}, {dy:.5g})"
        elif path_type == "c":
            # svg: c dx1 dy1, dx2 dy2, dx dy
            # tikz: .. controls (x + dx1, y + dy1) and (x + dx2, y + dy2) .. ++(dx, dy)
            (dx1, dy1, dx2, dy2, dx, dy), i = next_multiple_numbers(d, i, 6)
            x1 = x + dx1
            y1 = y + dy1
            x2 = x + dx2
            y2 = y + dy2
            x += dx
            y += dy
            code += f" .. controls ({x1:.5g}, {y1:.5g}) and ({x2:.5g}, {y2:.5g}) .. ++({dx:.5g}, {dy:.5g})"
        elif path_type == "s":
            # svg: s dx2 dy2, dx dy
            # tikz: .. controls (x - dx2, y - dy2) and (x + dx2, y + dy2) .. ++(dx, dy)
            (dx2, dy2, dx, dy), i = next_multiple_numbers(d, i, 4)
            x1 = x - dx2
            y1 = y - dy2
            x2 = x + dx2
            y2 = y + dy2
            x += dx
            y += dy
            code += f" .. controls ({x1:.5g}, {y1:.5g}) and ({x2:.5g}, {y2:.5g}) .. ++({dx:.5g}, {dy:.5g})"
        elif path_type == "z" or path_type == "Z":
            code += " -- cycle"
            break
        else:
            raise ValueError(f"Unsupported path type: {path_type}")

        if is_first:
            # Delete first " -- "
            code = code.replace(" -- ", "", 1)
            is_first = False

    code += f"; % {class_name}"
    code += "\n"

    return code


def rect_to_tikz(rect: xml.etree.ElementTree.Element, draw_options: str = "") -> str:
    """Convert an SVG rect to a TikZ path."""
    x0 = float(rect.attrib["x"])
    y0 = float(rect.attrib["y"])
    x1 = float(rect.attrib["width"])
    y1 = float(rect.attrib["height"])
    class_name = rect.attrib["class"]

    code = f"\\draw[{draw_options}] "
    code += f"({x0:.5g}, {y0:.5g}) rectangle ({x0 + x1:.5g}, {y0 + y1:.5g}); % {class_name}"
    code += "\n"

    return code
