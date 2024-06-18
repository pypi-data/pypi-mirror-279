from bgfactory.components.constants import INFER, COLOR_WHITE, FILL
from bgfactory.components.shape import Rectangle
from bgfactory.components.text import TextUniform

if __name__ == '__main__':
    
    rect2 = Rectangle(0, 0, 500, 500, stroke_width=0)
    
    rect = Rectangle(100, 100, 50, 33, stroke_width=1, stroke_color=(0.7, 0, 0, 0.5), padding=(-1,-1,-1,-1))
    text = TextUniform(0, 0, FILL, FILL, 'This is a text')
    
    rect.add(text)
    rect2.add(rect)
    
    rect2.image().show()