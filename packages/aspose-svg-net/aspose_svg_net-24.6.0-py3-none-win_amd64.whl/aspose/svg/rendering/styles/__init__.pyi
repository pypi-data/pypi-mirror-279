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

class ISVGPropertyResolvingContext(aspose.svg.dom.css.IPercentResolvingContext):
    '''Represents a context for resolving SVG properties, extending the percent resolving context and property context.'''
    
    def get_absolute_bounding_box(self, ignore_element_tranformations : bool) -> aspose.pydrawing.RectangleF:
        '''Gets the absolute bounding box of the element, optionally ignoring element transformations.
        
        :param ignore_element_tranformations: Determines whether to ignore element transformations.
        :returns: The absolute bounding box as a :py:class:`aspose.pydrawing.RectangleF`.'''
        ...
    
    def get_bounding_box(self) -> aspose.pydrawing.RectangleF:
        '''Gets the bounding box of the element.
        
        :returns: The bounding box as a :py:class:`aspose.pydrawing.RectangleF`.'''
        ...
    
    def get_stroke_bounding_box(self) -> aspose.pydrawing.RectangleF:
        '''Gets the bounding box of the element's stroke.
        
        :returns: The stroke bounding box as a :py:class:`aspose.pydrawing.RectangleF`.'''
        ...
    
    @property
    def parent_context(self) -> aspose.svg.rendering.styles.ISVGPropertyResolvingContext:
        ...
    
    @property
    def document(self) -> aspose.svg.dom.Document:
        '''Gets the document associated with the context. See :py:attr:`aspose.svg.rendering.styles.ISVGPropertyResolvingContext.document`.'''
        ...
    
    @property
    def view_css(self) -> aspose.svg.dom.css.IViewCSS:
        ...
    
    @property
    def element(self) -> aspose.svg.dom.Element:
        '''Gets the SVG element associated with the context. See :py:attr:`aspose.svg.rendering.styles.ISVGPropertyResolvingContext.element`.'''
        ...
    
    @property
    def style_declaration(self) -> aspose.svg.dom.css.ICSSStyleDeclaration:
        ...
    
    @property
    def in_text_element(self) -> bool:
        ...
    
    @in_text_element.setter
    def in_text_element(self, value : bool):
        ...
    
    @property
    def style(self) -> aspose.svg.dom.css.IResolvedStyleDeclaration:
        '''Gets the resolved style declaration associated with the element. See :py:class:`aspose.svg.dom.css.IResolvedStyleDeclaration`.'''
        ...
    
    @property
    def horizontal_resolution(self) -> aspose.svg.drawing.Resolution:
        ...
    
    @property
    def vertical_resolution(self) -> aspose.svg.drawing.Resolution:
        ...
    
    @property
    def dr_factory(self) -> aspose.svg.drawing.IDrawingFactory:
        ...
    
    @property
    def is_filter_brush(self) -> bool:
        ...
    
    @is_filter_brush.setter
    def is_filter_brush(self, value : bool):
        ...
    
    @property
    def viewport(self) -> aspose.svg.drawing.Viewport:
        '''Gets the :py:attr:`aspose.svg.dom.css.IPercentResolvingContext.viewport` associated with the percentage resolving context.'''
        ...
    
    ...

