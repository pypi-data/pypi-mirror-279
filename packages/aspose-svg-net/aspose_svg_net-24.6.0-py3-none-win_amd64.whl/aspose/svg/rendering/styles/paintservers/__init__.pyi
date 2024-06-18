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

class ISvgPaintServer:
    '''Represents a paint server used in SVG rendering.'''
    
    @property
    def paint_server_type(self) -> aspose.svg.rendering.styles.paintservers.SvgPaintServerType:
        ...
    
    ...

class SvgPaintServerType:
    '''Specifies the type of SVG paint server.'''
    
    @classmethod
    @property
    def HATCH(cls) -> SvgPaintServerType:
        '''Represents a hatch paint server type.'''
        ...
    
    @classmethod
    @property
    def MESH_GRADIENT(cls) -> SvgPaintServerType:
        '''Represents a mesh gradient paint server type.'''
        ...
    
    @classmethod
    @property
    def PATTERN(cls) -> SvgPaintServerType:
        '''Represents a pattern paint server type.'''
        ...
    
    @classmethod
    @property
    def RADIAL_GRADIENT(cls) -> SvgPaintServerType:
        '''Represents a radial gradient paint server type.'''
        ...
    
    @classmethod
    @property
    def SOLIDCOLOR(cls) -> SvgPaintServerType:
        '''Represents a solid color paint server type.'''
        ...
    
    @classmethod
    @property
    def LINEAR_GRADIENT(cls) -> SvgPaintServerType:
        '''Represents a linear gradient paint server type.'''
        ...
    
    ...

