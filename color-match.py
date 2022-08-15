import xml.etree.ElementTree as ET
import colour


def get_colour_val(colour_name: str, colour_obj: ET.Element) -> int:
    return int(colour_obj.find(colour_name).text)


def parse_acb_colours(acb_file: str):
    root = ET.parse(acb_file).getroot()

    colours = []
    # print(root.findall('colorPage'))

    for page in root.findall('colorPage'):
        for current_col in page.findall('colorEntry'):
            name: str = current_col.find('colorName')
            col_obj = current_col.find('RGB8')

            colour_val = colour.Color()
            colour_val.rgb = (get_colour_val('red', col_obj), get_colour_val('green', col_obj), get_colour_val('blue', col_obj))
            
            colours.append({
                'name': name,
                'colour': colour_val
            })

    return colours


# def load_colour_library(filename: str):
#     with open(filename) as f:
#         return f.read()

print(parse_acb_colours("color-library\Resene_The_Range_2000.acb"))
