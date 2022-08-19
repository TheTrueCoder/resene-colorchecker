import xml.etree.ElementTree as ET
import colour
import os
import random
import numpy as np

# Constants
COLOUR_LIBRARY_PATH = 'colour-library'
COLOURS_LIST = 'colors.txt'


def get_colour_val(colour_name: str, colour_obj: ET.Element) -> int:
    return float(colour_obj.find(colour_name).text)/255


def RGB_to_Lab(rgb_colour: list):
    illuminant_RGB = np.array([0.31270, 0.32900])
    illuminant_XYZ = np.array([0.34570, 0.35850])
    chromatic_adaptation_transform = 'Bradford'
    matrix_RGB_to_XYZ = np.array(
        [[0.41240000, 0.35760000, 0.18050000],
        [0.21260000, 0.71520000, 0.07220000],
        [0.01930000, 0.11920000, 0.95050000]])
    xyz_colour=colour.RGB_to_XYZ(
        rgb_colour, illuminant_RGB, illuminant_XYZ, matrix_RGB_to_XYZ, chromatic_adaptation_transform)
    return colour.XYZ_to_Lab(xyz_colour)


def parse_acb_colours(acb_file: str) -> list[dict]:
    root=ET.parse(acb_file).getroot()

    colours=[]
    # print(root.findall('colorPage'))

    for page in root.findall('colorPage'):
        for current_col in page.findall('colorEntry'):
            name: str=current_col.find('colorName').text
            col_obj=current_col.find('RGB8')

            colour_val=(get_colour_val('red', col_obj), get_colour_val(
                'green', col_obj), get_colour_val('blue', col_obj))

            colours.append({
                'name': name,
                'colour': colour_val
            })

    return colours


def load_colour_library(folder: str):
    colour_lib=[]
    for filename in os.listdir(folder):
        colour_lib += parse_acb_colours(os.path.join(folder, filename))
    return colour_lib

# print(parse_acb_colours("colour-library\Resene_The_Range_2000.acb"))
colour_library=load_colour_library('colour-library')

selected_colour=random.choice(colour_library)
print(RGB_to_Lab(selected_colour['colour']))
