import os
import shutil
from zipfile import ZipFile
from xml.etree import ElementTree
from xml.etree.ElementTree import Element as XElement  # shortened "XML Element"

from ..geo.construction import Construction
from ..geo.lib_commands import Command
from ..geo.lib_vars import *
from ..geo.lib_elements import *

temp_path = os.path.join(os.getcwd(), "temp")

#--------------------------------------------------------------------------

def rgb_to_hex(r, g, b):
    return '#{:02x}{:02x}{:02x}'.format(r, g, b)

def get_xelems(ggb_path: str): # -> XElement:
    try:    
        os.mkdir(temp_path)
    except FileExistsError:
        pass
    shutil.copyfile(ggb_path, os.path.join(temp_path, "temp.ggb"))
    
    ggb = ZipFile(os.path.join(temp_path, "temp.ggb"))
    ggb.extractall(temp_path)
    ggb.close()
    os.remove(os.path.join(temp_path, "temp.ggb"))
    
    tree = ElementTree.parse(os.path.join(temp_path, "geogebra.xml"))
    root = tree.getroot()
    
    shutil.rmtree(temp_path)
    
    return root.find("construction"), root.find("euclidianView")

def parse_constr(constr: Construction, constr_xelem: XElement, debug = False):
    xelems_left_to_pass = 0
    fixed_element = False

    style = {}
    
    for xelem in constr_xelem:            
        if xelem.tag == "element":
            name = xelem.attrib['label']
            type = xelem.attrib["type"]
            #print(f'ELEMENT {name}')
            if type != "numeric":
                style[name] = {}

                elem = xelem.find("decoration")
                if elem is not None: 
                    style[name]['lines'] = int(elem.attrib['type'])
                    if xelem.attrib['type'] == 'angle':
                        style[name]['lines'] += 1
                       
                elem = xelem.find("show")
                if elem is not None: 
                    style[name]['show_element'] = (elem.attrib['object'] == 'true')
                    style[name]['show_label'] = (elem.attrib['label'] == 'true')
                
                elem = xelem.find("labelMode")
                if elem is not None:
                    caption = xelem.find("caption")
                    if (elem.attrib['val'] == '3') & (caption is not None):
                        style[name]['label'] = caption.attrib['val']
    
                elem = xelem.find("labelOffset")
                if elem is not None: 
                    if type == "angle":
                        style[name]['offset'] = [float(elem.attrib['x']) / 50, -float(elem.attrib['y']) / 50]
                    else:
                        style[name]['offset'] = [0.2 + float(elem.attrib['x']) / 50, 0.3 - float(elem.attrib['y']) / 50]
                else:
                    if type == "angle":
                        style[name]['offset'] = [0, 0]
                    else:
                        style[name]['offset'] = [0.2, 0.3]
 
                elem = xelem.find("arcSize")
                if elem is not None: 
                    if xelem.attrib['type'] == 'angle':
                        style[name]['r_offset'] = (float(elem.attrib['val']) - 30) / 30
                    
                elem = xelem.find("objColor")
                if elem is not None:
                    r, g, b, a = int(elem.attrib['r']), int(elem.attrib['g']), int(elem.attrib['b']), float(elem.attrib['alpha'])
                    if xelem.attrib['type'] in ['angle', 'polygon', 'arc', 'conic']:
                        style[name]['fill'] = rgb_to_hex(r, g, b)
                        style[name]['fill_opacity'] = a
                    lineStyle = xelem.find("lineStyle")
                    if lineStyle is not None:
                        thick, tt = lineStyle.attrib['thickness'], lineStyle.attrib['type']
                        op = float(lineStyle.attrib['opacity']) if 'opacity' in lineStyle.attrib else 255
                        if xelem.attrib['type'] in ['angle', 'segment', 'arc', 'conic', 'vector']:
                            style[name]['stroke'] = rgb_to_hex(r, g, b)
                            #style[name]['stroke_opacity'] = op / 255
                            style[name]['stroke_width'] = thick
                            if int(tt) > 0: style[name]['stroke_dash'] = 0.65
                        
        if xelems_left_to_pass:
            xelems_left_to_pass -= 1
            continue

        if xelem.tag == "expression":
            #unknown_objs[xelem.attrib["label"]] = True
            #xelems_left_to_pass = 1
            continue
        if xelem.tag == "command":
            comm_name = xelem.attrib["name"]
            input_xelem, output_xelem = xelem.find("input"), xelem.find("output")
            inputs, outputs = list(input_xelem.attrib.values()), list(output_xelem.attrib.values())
            
            if comm_name == "Point":
                if len(inputs) == 1:
                    if debug: print('Point FIXED')
                    fixed_element = True
                else:
                    xelems_left_to_pass = 1
                continue
            if comm_name == "PointIn":
                xelems_left_to_pass = 1
                continue

            constr.add(Command(comm_name, inputs, outputs))
            xelems_left_to_pass = len(output_xelem.attrib)
            continue
        
        # Here xelem has to be a commandless point or numeric (Var)
        
        if xelem.tag == "element":
            if xelem.attrib["type"] == "point":
                coords = list(xelem.find("coords").attrib.values())
                coords.pop(-1) #  removing z coordinate
                constr.add(Element(xelem.attrib["label"], Point([float(x) for x in coords]), fixed = fixed_element))
                fixed_element = False
                continue
            if xelem.attrib["type"] == "numeric":
                value_xelem = xelem.find("value")
                constr.add(Var(xelem.attrib["label"], float(value_xelem.attrib["val"])))
                continue
            if xelem.attrib["type"] == "angle":
                value_xelem = xelem.find("value")
                constr.add(Var(xelem.attrib["label"], AngleSize(float(value_xelem.attrib["val"]))))
                continue
        
        #raise ElementTree.ParseError(f"Unexpected XElement met:\n\t<{xelem.tag}>, {xelem.attrib}")
        print(f"Unexpected XElement met:\n\t<{xelem.tag}>, {xelem.attrib}")

    constr.rebuild(debug = debug)

    #styling elements
    for name in style:
        for key in style[name]:
            if debug: print(f'STYLE >> {name} >> {key} = {style[name][key]}')
            if key == 'show_element':
                constr.element(name).visible = style[name][key]
                continue
            constr.element(name).style[key] = style[name][key]

def FloatOrNone(txt):
    return float(txt) if txt is not None else None

def parse_view(constr: Construction, view_xelem: XElement, debug = False):
    constr.style['view'] = {}
    
    for xelem in view_xelem:            
        if xelem.tag == "size":
            constr.style['view']['width'], constr.style['view']['height'] = FloatOrNone(xelem.attrib['width']), FloatOrNone(xelem.attrib['height'])

        if xelem.tag == "coordSystem":
            constr.style['view']['xZero'], constr.style['view']['yZero'] = FloatOrNone(xelem.attrib['xZero']), FloatOrNone(xelem.attrib['yZero'])
            constr.style['view']['scale'] = FloatOrNone(xelem.attrib['scale'])       

def load(ggb_path: str, debug = False): # -> Construction:
    constr_xelem, view_xelem = get_xelems(ggb_path)
    if debug: print(constr_xelem, view_xelem)
    constr = Construction()
    parse_constr(constr, constr_xelem, debug = debug)
    parse_view(constr, view_xelem, debug = debug)
    
    return constr
