# Presentation Manipulation Python API

![banner](https://products.aspose.com/slides/images/aspose_slides-for-python-via-java-banner.png)

[Product Page](https://products.aspose.com/slides/python-java/) | [Docs](https://docs.aspose.com/slides/python-java/) | [Demos](https://products.aspose.app/slides/family) | [API Reference](https://reference.aspose.com/slides/python-java/) | [Blog](https://blog.aspose.com/category/slides/) | [Search](https://search.aspose.com/) | [Free Support](https://forum.aspose.com/c/slides) | [Release Notes](https://releases.aspose.com/slides/python-java/release-notes/) | [Temporary License](https://purchase.aspose.com/temporary-license)

[Aspose.Slides for Python via Java](https://products.aspose.com/slides/python-java/) is a powerful on-premise class library used for processing and working with presentations. With this API, developers and applications get to generate, modify, convert, render, print, and manipulate presentations without relying on Microsoft PowerPoint or other third-party applications and services. 

Without having to install a PowerPoint program or any 3rd party component, you can use Aspose.Slides to build different types applications. For example, Aspose, using its own APIs, developed a [free web application](https://products.aspose.app/slides/import/pdf-to-powerpoint) that allows people to convert their PDF documents to PowerPoint Presentation online.

>Aspose.Slides for Python requires you to use python programming language. For .NET, Java, C++, PHP and JavaScript languages, we recommend you get [Aspose.Slides for .NET](https://products.aspose.com/slides/net/), [Aspose.Slides for Java](https://products.aspose.com/slides/java/), [Aspose.Slides for C++](https://products.aspose.com/slides/cpp/), [Aspose.Slides for PHP via Java](https://products.aspose.com/slides/php-java/) and [Aspose.Slides for Node.js via Java](https://products.aspose.com/slides/nodejs-java/), respectively.

## Slides API Features

Aspose.Slides for Python via Java provides these popular features:
- Loading, opening, and viewing presentations 
- Editing presentations
- Converting presentations to PDF, Word, JPG, HTML, GIF, SVG, and many other formats
- Rendering and printing presentations
- Encrypting and decrypting presentations; password-protecting presentations and removing passwords
- Manipulating presentation entities, such as master slides, shapes, charts, picture frames, audio frames, video frames, OLE, VBA macros, animations, etc.

## Platform Independence

Aspose.Slides for Python via Java is platform-independent API and can be used on any platform (Windows, Linux and MacOS) where **Python**, **Java** and **jpype1 bridge** are installed.

## Get Started

Ready to try Aspose.Slides for Python via Java?

Please read detailed installation instructions - [Installing Aspose.Slides for Python for Java](https://docs.aspose.com/slides/python-java/installation/)

Fetch the package and install **aspose-slides-java**. Run this command: `pip install aspose-slides-java`

If you already have **aspose-slides-java** package installed and want to get the latest version,   
you have to run `pip install --upgrade aspose-slides-java` instead. 

## Create a Presentation (PPTX) from scratch in Python

```py
import jpype
import asposeslides

jpype.startJVM()

from asposeslides.api import Presentation, ShapeType, SaveFormat

# Instantiate a Presentation object
presentation = Presentation()

# Select first slide
slide = presentation.getSlides().get_Item(0)

# Add new Line shape to slide
slide.getShapes().addAutoShape(ShapeType.Line, 50, 150, 300, 0)

# Save the presentation as PPTX
presentation.save("newPresentation.pptx", SaveFormat.Pptx)

jpype.shutdownJVM()
```

## Convert a Presentation to PDF

```py
import jpype
import asposeslides

jpype.startJVM()

from asposeslides.api import Presentation, SaveFormat

# Instantiate a Presentation object that represents a PPTX file
presentation = Presentation("presentation.pptx")

# Save the presentation as PDF
presentation.save("outputPDF.pdf", SaveFormat.Pdf)

jpype.shutdownJVM()
```

## Import PDF and Save it as a Presentation

```py
import jpype
import asposeslides

jpype.startJVM()

from asposeslides.api import Presentation, SaveFormat

# Instantiate a Presentation object that represents a PPTX file
presentation = Presentation()

# Remove the first slide from a presentation
presentation.getSlides().removeAt(0)

# Import the contents of a PDF file into a presentation.
presentation.getSlides().addFromPdf("welcome-to-powerpoint.pdf")

# Save the presentation as PPTX
presentation.save("outputPresentation.pptx", SaveFormat.Pptx)

jpype.shutdownJVM()
```


[Product Page](https://products.aspose.com/slides/python-java/) | [Docs](https://docs.aspose.com/slides/python-java/) | [Demos](https://products.aspose.app/slides/family) | [API Reference](https://reference.aspose.com/slides/python-java/) | [Blog](https://blog.aspose.com/category/slides/) | [Search](https://search.aspose.com/) | [Free Support](https://forum.aspose.com/c/slides) | [Release Notes](https://releases.aspose.com/slides/python-java/release-notes/) | [Temporary License](https://purchase.aspose.com/temporary-license)