import jpype
import asposeslides

jpype.startJVM()

from asposeslides.api import Presentation, ShapeType, SaveFormat

pres = Presentation()
slide = pres.getSlides().get_Item(0)
slide.getShapes().addAutoShape(ShapeType.Line, 50, 150, 300, 0)
pres.save("NewPresentation.pptx", SaveFormat.Pptx)

jpype.shutdownJVM()