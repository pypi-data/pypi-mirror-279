import cairocffi as cairo

from bgfactory.components.cairo_helpers import image_from_surface
from bgfactory.components.constants import FILL
from bgfactory.components.layout.vertical_flow_layout import VerticalFlowLayout
from bgfactory.components.shape import Rectangle
from bgfactory.components.source import PNGSource

if __name__ == '__main__':
    
    
    path = 'output/test_vertflow.png'
    
    rect = Rectangle(0, 0, 100, 500, fill_src=PNGSource(path, 0, 0, FILL, FILL), stroke_width=0, layout=VerticalFlowLayout())
    
    rect2 = Rectangle(0, 0, 20, 20)
    
    rect.add(rect2)
    rect.add(rect2)
    rect.add(rect2)
    rect.add(rect2)
    
    rect.image().show()
    