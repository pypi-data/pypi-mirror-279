from typing import List, Optional, Dict, Iterable
import aspose.pycore
import aspose.pydrawing
import aspose.svg
import aspose.svg.builder
import aspose.svg.collections
import aspose.svg.converters
import aspose.svg.datatypes
import aspose.svg.diagnostics
import aspose.svg.dom
import aspose.svg.dom.attributes
import aspose.svg.dom.canvas
import aspose.svg.dom.css
import aspose.svg.dom.events
import aspose.svg.dom.mutations
import aspose.svg.dom.traversal
import aspose.svg.dom.traversal.filters
import aspose.svg.dom.views
import aspose.svg.dom.xpath
import aspose.svg.drawing
import aspose.svg.drawing.skiasharp
import aspose.svg.events
import aspose.svg.filters
import aspose.svg.imagevectorization
import aspose.svg.io
import aspose.svg.net
import aspose.svg.net.headers
import aspose.svg.net.messagefilters
import aspose.svg.net.messagehandlers
import aspose.svg.paths
import aspose.svg.rendering
import aspose.svg.rendering.devices
import aspose.svg.rendering.fonts
import aspose.svg.rendering.image
import aspose.svg.rendering.pdf
import aspose.svg.rendering.pdf.encryption
import aspose.svg.rendering.styles
import aspose.svg.rendering.styles.paintservers
import aspose.svg.rendering.xps
import aspose.svg.saving
import aspose.svg.saving.resourcehandlers
import aspose.svg.services
import aspose.svg.toolkit
import aspose.svg.toolkit.optimizers
import aspose.svg.window

class IPdfDeviceFactory:
    '''Represents a factory for creating PDF devices.'''
    
    @overload
    def create(self, options : aspose.svg.rendering.pdf.PdfRenderingOptions, stream_provider : aspose.svg.io.ICreateStreamProvider) -> aspose.svg.rendering.IDevice:
        '''Creates a PDF device with the specified rendering options and stream provider.
        
        :param options: The rendering options for the PDF device. See :py:class:`aspose.svg.rendering.pdf.PdfRenderingOptions`.
        :param stream_provider: The stream provider used to create the PDF output stream. See :py:class:`aspose.svg.io.ICreateStreamProvider`.
        :returns: The created PDF device.'''
        ...
    
    @overload
    def create(self, options : aspose.svg.rendering.pdf.PdfRenderingOptions, file : str) -> aspose.svg.rendering.IDevice:
        '''Creates a PDF device with the specified rendering options and file path.
        
        :param options: The rendering options for the PDF device. See :py:class:`aspose.svg.rendering.pdf.PdfRenderingOptions`.
        :param file: The file path for the PDF output.
        :returns: The created PDF device.'''
        ...
    
    @overload
    def create(self, options : aspose.svg.rendering.pdf.PdfRenderingOptions, stream : io.RawIOBase) -> aspose.svg.rendering.IDevice:
        '''Creates a PDF device with the specified rendering options and stream.
        
        :param options: The rendering options for the PDF device. See :py:class:`aspose.svg.rendering.pdf.PdfRenderingOptions`.
        :param stream: The stream for the PDF output.
        :returns: The created PDF device.'''
        ...
    
    ...

class PdfDevice(aspose.svg.rendering.DeviceAdapter):
    '''Represents rendering to a pdf document.'''
    
    def save_graphic_context(self):
        '''Pushes a copy of the entire graphics context onto the stack.'''
        ...
    
    def restore_graphic_context(self):
        '''Restores the entire graphics context to its former value by popping it from the stack.'''
        ...
    
    def begin_document(self, document : aspose.svg.dom.Document):
        '''Begins rendering of the document.
        
        :param document: The document.'''
        ...
    
    def end_document(self):
        '''Ends rendering of the document.'''
        ...
    
    def begin_page(self, size : aspose.pydrawing.SizeF):
        '''Begins rendering of the new page.
        
        :param size: Size of the page.'''
        ...
    
    def end_page(self):
        '''Ends rendering of the current page.'''
        ...
    
    def begin_element(self, element : aspose.svg.dom.Element, rect : aspose.pydrawing.RectangleF) -> bool:
        '''Begins rendering of the element.
        
        :param element: The :py:class:`aspose.svg.dom.Element`.
        :param rect: Bounding box of the node.
        :returns: Returns [true] if element should be processed.'''
        ...
    
    def end_element(self, element : aspose.svg.dom.Element):
        '''Ends rendering of the element.
        
        :param element: The :py:class:`aspose.svg.dom.Element`.'''
        ...
    
    def close_path(self):
        '''Closes the current subpath by appending a straight line segment from the current point to the starting point of the subpath.
        If the current subpath is already closed, "ClosePath" does nothing.
        This operator terminates the current subpath. Appending another segment to the current path begins a new subpath,
        even if the new segment begins at the endpoint reached by the "ClosePath" method.'''
        ...
    
    def move_to(self, pt : aspose.pydrawing.PointF):
        '''Begins a new subpath by moving the current point to coordinates of the parameter pt, omitting any connecting line segment.
        If the previous path construction method in the current path was also "MoveTo", the new "MoveTo" overrides it;
        no vestige of the previous "MoveTo" operation remains in the path.
        
        :param pt: Point of where to move the path to.'''
        ...
    
    def line_to(self, pt : aspose.pydrawing.PointF):
        '''Appends a straight line segment from the current point to the point (pt). The new current point is pt.
        
        :param pt: Point of where to create the line to.'''
        ...
    
    def add_rect(self, rect : aspose.pydrawing.RectangleF):
        '''Appends a rectangle to the current path as a complete subpath.
        
        :param rect: A rectangle to draw.'''
        ...
    
    def cubic_bezier_to(self, pt1 : aspose.pydrawing.PointF, pt2 : aspose.pydrawing.PointF, pt3 : aspose.pydrawing.PointF):
        '''Appends a cubic Bézier curve to the current path. The curve extends from the current point to the point pt2,
        using pt1 and pt2 as the Bézier control points. The new current point is pt3.
        
        :param pt1: Coordinates of first point
        :param pt2: Coordinates of second point
        :param pt3: Coordinates of third point'''
        ...
    
    def stroke(self):
        '''Strokes a line along the current path. The stroked line follows each straight or curved segment in the path,
        centered on the segment with sides parallel to it. Each of the path’s subpaths is treated separately.
        This method terminates current path.'''
        ...
    
    def fill(self, mode : aspose.svg.drawing.FillRule):
        '''Fills the entire region enclosed by the current path.
        If the path consists of several disconnected subpaths, it fills the insides of all subpaths,
        considered together.
        This method terminates current path.
        
        :param mode: Filling mode specifies how the interior of a closed path is filled'''
        ...
    
    def clip(self, mode : aspose.svg.drawing.FillRule):
        '''Modifies the current clipping path by intersecting it with the current path, using the FillMode rule to determine the region to fill.
        This method terminates current path.
        
        :param mode: Filling mode specifies how the interior of a closed path is clipped'''
        ...
    
    def stroke_and_fill(self, mode : aspose.svg.drawing.FillRule):
        '''Strokes and fill current path.
        This method terminates current path.
        
        :param mode: Filling mode specifies how the interior of a closed path is filled.'''
        ...
    
    def fill_text(self, text : str, pt : aspose.pydrawing.PointF):
        '''Fills the specified text string at the specified location.
        
        :param text: String to fill.
        :param pt: Point that specifies the coordinates of the text.'''
        ...
    
    def stroke_text(self, text : str, pt : aspose.pydrawing.PointF):
        '''Strokes the specified text string at the specified location.
        
        :param text: String to stroke.
        :param pt: Point that specifies the coordinates where to start the text.'''
        ...
    
    def draw_image(self, data : bytes, image_format : aspose.svg.drawing.WebImageFormat, rect : aspose.pydrawing.RectangleF):
        '''Draws the specified image.
        
        :param data: An array of bytes representing the image.
        :param image_format: Image format.
        :param rect: A rectangel which determines position and size to draw.'''
        ...
    
    def flush(self):
        '''Flushes all data to output stream.'''
        ...
    
    @property
    def adapted_device(self) -> aspose.svg.rendering.IDevice:
        ...
    
    @adapted_device.setter
    def adapted_device(self, value : aspose.svg.rendering.IDevice):
        ...
    
    @property
    def options(self) -> aspose.svg.rendering.RenderingOptions:
        '''Gets the rendering options.'''
        ...
    
    @property
    def graphic_context(self) -> aspose.svg.rendering.GraphicContext:
        ...
    
    ...

class PdfDocumentInfo:
    '''Represents the information about the PDF document.'''
    
    @property
    def title(self) -> str:
        '''The document's title.'''
        ...
    
    @title.setter
    def title(self, value : str):
        '''The document's title.'''
        ...
    
    @property
    def author(self) -> str:
        '''The name of the person who created the document.'''
        ...
    
    @author.setter
    def author(self, value : str):
        '''The name of the person who created the document.'''
        ...
    
    @property
    def subject(self) -> str:
        '''The subject of the document.'''
        ...
    
    @subject.setter
    def subject(self, value : str):
        '''The subject of the document.'''
        ...
    
    @property
    def keywords(self) -> str:
        '''Keywords associated with the document.'''
        ...
    
    @keywords.setter
    def keywords(self, value : str):
        '''Keywords associated with the document.'''
        ...
    
    @property
    def creator(self) -> str:
        '''The name of the product that created the original document.'''
        ...
    
    @creator.setter
    def creator(self, value : str):
        '''The name of the product that created the original document.'''
        ...
    
    @property
    def producer(self) -> str:
        '''The name of the product that converted the document.'''
        ...
    
    @producer.setter
    def producer(self, value : str):
        '''The name of the product that converted the document.'''
        ...
    
    @property
    def creation_date(self) -> DateTime:
        ...
    
    @creation_date.setter
    def creation_date(self, value : DateTime):
        ...
    
    @property
    def modification_date(self) -> DateTime:
        ...
    
    @modification_date.setter
    def modification_date(self, value : DateTime):
        ...
    
    ...

class PdfRenderingOptions(aspose.svg.rendering.RenderingOptions):
    '''Represents rendering options for :py:class:`aspose.svg.rendering.pdf.PdfDevice`.'''
    
    @property
    def css(self) -> aspose.svg.rendering.CssOptions:
        '''Gets a :py:class:`aspose.svg.rendering.CssOptions` object which is used for configuration of css properties processing.'''
        ...
    
    @property
    def page_setup(self) -> aspose.svg.rendering.PageSetup:
        ...
    
    @property
    def horizontal_resolution(self) -> aspose.svg.drawing.Resolution:
        ...
    
    @horizontal_resolution.setter
    def horizontal_resolution(self, value : aspose.svg.drawing.Resolution):
        ...
    
    @property
    def background_color(self) -> aspose.pydrawing.Color:
        ...
    
    @background_color.setter
    def background_color(self, value : aspose.pydrawing.Color):
        ...
    
    @property
    def vertical_resolution(self) -> aspose.svg.drawing.Resolution:
        ...
    
    @vertical_resolution.setter
    def vertical_resolution(self, value : aspose.svg.drawing.Resolution):
        ...
    
    @property
    def document_info(self) -> aspose.svg.rendering.pdf.PdfDocumentInfo:
        ...
    
    @property
    def form_field_behaviour(self) -> aspose.svg.rendering.pdf.FormFieldBehaviour:
        ...
    
    @form_field_behaviour.setter
    def form_field_behaviour(self, value : aspose.svg.rendering.pdf.FormFieldBehaviour):
        ...
    
    @property
    def jpeg_quality(self) -> int:
        ...
    
    @jpeg_quality.setter
    def jpeg_quality(self, value : int):
        ...
    
    @property
    def encryption(self) -> aspose.svg.rendering.pdf.encryption.PdfEncryptionInfo:
        '''Gets a encryption details. If not set, then no encryption will be performed.'''
        ...
    
    @encryption.setter
    def encryption(self, value : aspose.svg.rendering.pdf.encryption.PdfEncryptionInfo):
        '''Sets a encryption details. If not set, then no encryption will be performed.'''
        ...
    
    @property
    def is_tagged_pdf(self) -> bool:
        ...
    
    @is_tagged_pdf.setter
    def is_tagged_pdf(self, value : bool):
        ...
    
    ...

class FormFieldBehaviour:
    '''This enumeration is used to specify the behavior of form fields in the output PDF document.'''
    
    @classmethod
    @property
    def INTERACTIVE(cls) -> FormFieldBehaviour:
        '''The output PDF document will contain interactive form fields.'''
        ...
    
    @classmethod
    @property
    def FLATTENED(cls) -> FormFieldBehaviour:
        '''The output PDF document will contain flattened form fields.'''
        ...
    
    ...

