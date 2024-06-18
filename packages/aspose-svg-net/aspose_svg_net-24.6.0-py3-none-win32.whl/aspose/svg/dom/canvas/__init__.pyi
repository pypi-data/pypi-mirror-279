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

class ICanvasGradient:
    '''Represents an opaque object describing a gradient.'''
    
    def add_color_stop(self, offset : float, color : str):
        '''Adds a new stop, defined by an offset and a color, to the gradient.
        
        :param offset: A number between 0 and 1.
        :param color: A CSS color'''
        ...
    
    ...

class ICanvasLinearGradientFactory:
    '''Represents a factory for creating linear gradients to be used with the HTML canvas rendering context.'''
    
    ...

class ICanvasPattern:
    '''Represents an opaque object describing a pattern, based on an image, a canvas or a video.'''
    
    def set_transform(self, transform : aspose.svg.datatypes.SVGMatrix):
        '''Applies an SVGMatrix representing a linear transform to the pattern.
        
        :param transform: An SVGMatrix to use as the pattern's transformation matrix.'''
        ...
    
    ...

class ICanvasPatternFactory:
    '''Represents a factory for creating patterns to be used with the HTML canvas rendering context.'''
    
    def create(self, canvas : aspose.svg.rendering.ICanvas, data : bytes, repetition : str) -> aspose.svg.dom.canvas.ICanvasPattern:
        '''Creates a pattern using the specified image data and repetition mode.
        
        :param canvas: The canvas associated with the pattern.
        :param data: The image data used for the pattern.
        :param repetition: A string indicating how to repeat the image.
        :returns: An opaque object describing the created pattern.'''
        ...
    
    ...

class ICanvasRadialGradientFactory:
    '''Represents a factory for creating radial gradients to be used with the HTML canvas rendering context.'''
    
    ...

class ICanvasSolid(aspose.svg.drawing.IBrush):
    '''Represents an opaque object describing a solid color to be used with the HTML canvas rendering context.'''
    
    def get_color(self) -> str:
        '''Gets the string representation of the solid color.
        
        :returns: The string representation of the solid color.'''
        ...
    
    def to_native(self) -> any:
        '''Converts the brush to a native representation.
        
        :returns: The native representation of the brush.'''
        ...
    
    @property
    def type(self) -> aspose.svg.drawing.BrushType:
        '''Get type of brush; See :py:class:`aspose.svg.drawing.BrushType`.'''
        ...
    
    @property
    def supports_shader(self) -> bool:
        ...
    
    ...

class ICanvasSolidFactory:
    '''Represents a factory for creating solid colors to be used with the HTML canvas rendering context.'''
    
    def create(self, string_color : str, color : aspose.pydrawing.Color) -> aspose.svg.dom.canvas.ICanvasSolid:
        '''Creates a solid color using the specified string representation and Color object.
        
        :param string_color: The string representation of the color.
        :param color: The Color object representing the color.
        :returns: An opaque object describing the created solid color.'''
        ...
    
    ...

