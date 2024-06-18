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

class CssOptions:
    '''Represents css rendering options.'''
    
    @property
    def media_type(self) -> aspose.svg.rendering.MediaType:
        ...
    
    @media_type.setter
    def media_type(self, value : aspose.svg.rendering.MediaType):
        ...
    
    ...

class Device:
    '''Represents a base class for implementing rendering devices that are used to draw graphics in various formats and environments.'''
    
    ...

class DeviceAdapter(Device):
    '''Represents a device adapter that adapts the interface of the wrapped device.'''
    
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

class GlyphInfo:
    '''Contains glyph related information.'''
    
    @property
    def width(self) -> float:
        '''Gets the width of the glyph, in points.'''
        ...
    
    @property
    def offset(self) -> float:
        '''Gets the offset to the next glyph in points.'''
        ...
    
    @property
    def index(self) -> int:
        '''Gets the index of this glyph in the font.'''
        ...
    
    @property
    def string_representation(self) -> str:
        ...
    
    ...

class GraphicContext:
    '''Holds current graphics control parameters.
    These parameters define the global framework within which the graphics operators execute.'''
    
    def transform(self, matrix : aspose.svg.drawing.IMatrix):
        '''Modify the current transformation matrix by multiplying the specified matrix.
        
        :param matrix: Transformation matrix.'''
        ...
    
    def clone(self) -> aspose.svg.rendering.GraphicContext:
        '''Creates a new instance of a GraphicContext class with the same property values as an existing instance.
        
        :returns: Instance of a GraphicContext'''
        ...
    
    @property
    def line_cap(self) -> aspose.svg.drawing.StrokeLineCap:
        ...
    
    @line_cap.setter
    def line_cap(self, value : aspose.svg.drawing.StrokeLineCap):
        ...
    
    @property
    def line_dash_offset(self) -> float:
        ...
    
    @line_dash_offset.setter
    def line_dash_offset(self, value : float):
        ...
    
    @property
    def line_dash_pattern(self) -> List[float]:
        ...
    
    @line_dash_pattern.setter
    def line_dash_pattern(self, value : List[float]):
        ...
    
    @property
    def line_join(self) -> aspose.svg.drawing.StrokeLineJoin:
        ...
    
    @line_join.setter
    def line_join(self, value : aspose.svg.drawing.StrokeLineJoin):
        ...
    
    @property
    def line_width(self) -> float:
        ...
    
    @line_width.setter
    def line_width(self, value : float):
        ...
    
    @property
    def miter_limit(self) -> float:
        ...
    
    @miter_limit.setter
    def miter_limit(self, value : float):
        ...
    
    @property
    def fill_brush(self) -> aspose.svg.drawing.IBrush:
        ...
    
    @fill_brush.setter
    def fill_brush(self, value : aspose.svg.drawing.IBrush):
        ...
    
    @property
    def stroke_brush(self) -> aspose.svg.drawing.IBrush:
        ...
    
    @stroke_brush.setter
    def stroke_brush(self, value : aspose.svg.drawing.IBrush):
        ...
    
    @property
    def font(self) -> aspose.svg.drawing.ITrueTypeFont:
        '''Sets or gets the true type font object that is used for rendering text.'''
        ...
    
    @font.setter
    def font(self, value : aspose.svg.drawing.ITrueTypeFont):
        '''Sets or gets the true type font object that is used for rendering text.'''
        ...
    
    @property
    def font_size(self) -> float:
        ...
    
    @font_size.setter
    def font_size(self, value : float):
        ...
    
    @property
    def font_style(self) -> aspose.pydrawing.FontStyle:
        ...
    
    @font_style.setter
    def font_style(self, value : aspose.pydrawing.FontStyle):
        ...
    
    @property
    def character_spacing(self) -> float:
        ...
    
    @character_spacing.setter
    def character_spacing(self, value : float):
        ...
    
    @property
    def transformation_matrix(self) -> aspose.svg.drawing.IMatrix:
        ...
    
    @transformation_matrix.setter
    def transformation_matrix(self, value : aspose.svg.drawing.IMatrix):
        ...
    
    @property
    def text_info(self) -> aspose.svg.rendering.TextInfo:
        ...
    
    ...

class ICanvas:
    '''Represents a canvas for drawing 2D graphics.'''
    
    @overload
    def arc(self, x : float, y : float, radius : float, start_angle : float, end_angle : float):
        '''Adds an arc to the current path.
        
        :param x: The x-coordinate of the center of the arc.
        :param y: The y-coordinate of the center of the arc.
        :param radius: The radius of the arc.
        :param start_angle: The starting angle of the arc in radians.
        :param end_angle: The ending angle of the arc in radians.'''
        ...
    
    @overload
    def arc(self, x : float, y : float, radius : float, start_angle : float, end_angle : float, counterclockwise : bool):
        '''Adds an arc to the current path.
        
        :param x: The x-coordinate of the center of the arc.
        :param y: The y-coordinate of the center of the arc.
        :param radius: The radius of the arc.
        :param start_angle: The starting angle of the arc in radians.
        :param end_angle: The ending angle of the arc in radians.
        :param counterclockwise: Specifies whether the arc should be drawn counterclockwise.'''
        ...
    
    @overload
    def clip(self, mode : aspose.svg.drawing.FillRule):
        '''Sets the current clipping path using the specified fill rule.
        
        :param mode: The fill rule to use for clipping.'''
        ...
    
    @overload
    def clip(self, path : aspose.svg.rendering.IPath, mode : aspose.svg.drawing.FillRule):
        '''Sets the current clipping path using the specified path and fill rule.
        
        :param path: The path to use for clipping.
        :param mode: The fill rule to use for clipping.'''
        ...
    
    @overload
    def ellipse(self, x : float, y : float, radius_x : float, radius_y : float, rotation : float, start_angle : float, end_angle : float):
        '''Adds an ellipse to the current path.
        
        :param x: The x-coordinate of the center of the ellipse.
        :param y: The y-coordinate of the center of the ellipse.
        :param radius_x: The x-radius of the ellipse.
        :param radius_y: The y-radius of the ellipse.
        :param rotation: The rotation of the ellipse in radians.
        :param start_angle: The starting angle of the ellipse in radians.
        :param end_angle: The ending angle of the ellipse in radians.'''
        ...
    
    @overload
    def ellipse(self, x : float, y : float, radius_x : float, radius_y : float, rotation : float, start_angle : float, end_angle : float, anticlockwise : bool):
        '''Adds an ellipse to the current path.
        
        :param x: The x-coordinate of the center of the ellipse.
        :param y: The y-coordinate of the center of the ellipse.
        :param radius_x: The x-radius of the ellipse.
        :param radius_y: The y-radius of the ellipse.
        :param rotation: The rotation of the ellipse in radians.
        :param start_angle: The starting angle of the ellipse in radians.
        :param end_angle: The ending angle of the ellipse in radians.
        :param anticlockwise: Specifies whether the ellipse should be drawn in the anticlockwise direction.'''
        ...
    
    @overload
    def fill(self, mode : aspose.svg.drawing.FillRule):
        '''Fills the current path with the specified fill rule.
        
        :param mode: The fill rule to use for filling the path.'''
        ...
    
    @overload
    def fill(self, path : aspose.svg.rendering.IPath, mode : aspose.svg.drawing.FillRule):
        '''Fills the specified path with the specified fill rule.
        
        :param path: The path to fill.
        :param mode: The fill rule to use for filling the path. See :py:class:`aspose.svg.drawing.FillRule`.'''
        ...
    
    @overload
    def is_point_in_path(self, x : float, y : float, mode : aspose.svg.drawing.FillRule) -> bool:
        '''Determines whether the specified point is inside the current path using the specified fill rule.
        
        :param x: The x-coordinate of the point to test.
        :param y: The y-coordinate of the point to test.
        :param mode: The fill rule to use for testing. See :py:class:`aspose.svg.drawing.FillRule`.
        :returns: ``true`` if the point is inside the path; otherwise, ``false``.'''
        ...
    
    @overload
    def is_point_in_path(self, path : aspose.svg.rendering.IPath, x : float, y : float, mode : aspose.svg.drawing.FillRule) -> bool:
        '''Determines whether the specified point is inside the specified path using the specified fill rule.
        
        :param path: The path to test.See :py:class:`aspose.svg.rendering.IPath`.
        :param x: The x-coordinate of the point to test.
        :param y: The y-coordinate of the point to test.
        :param mode: The fill rule to use for testing. See :py:class:`aspose.svg.drawing.FillRule`.
        :returns: ``true`` if the point is inside the path; otherwise, ``false``.'''
        ...
    
    @overload
    def is_point_in_stroke(self, x : float, y : float) -> bool:
        '''Determines whether the specified point is inside the current stroked path.
        
        :param x: The x-coordinate of the point to test.
        :param y: The y-coordinate of the point to test.
        :returns: ``true`` if the point is inside the stroked path; otherwise, ``false``.'''
        ...
    
    @overload
    def is_point_in_stroke(self, path : aspose.svg.rendering.IPath, x : float, y : float) -> bool:
        '''Determines whether the specified point is inside the specified stroked path.
        
        :param path: The path to test. See :py:class:`aspose.svg.rendering.IPath`.
        :param x: The x-coordinate of the point to test.
        :param y: The y-coordinate of the point to test.
        :returns: ``true`` if the point is inside the stroked path; otherwise, ``false``.'''
        ...
    
    @overload
    def stroke(self):
        '''Strokes the current path.'''
        ...
    
    @overload
    def stroke(self, path : aspose.svg.rendering.IPath):
        '''Strokes the specified path.
        
        :param path: The path to stroke. See :py:class:`aspose.svg.rendering.IPath`.'''
        ...
    
    def arc_to(self, x1 : float, y1 : float, x2 : float, y2 : float, radius : float):
        '''Adds an arc to the current path, connecting the previous point to the start point of the arc with a straight line.
        
        :param x1: The x-coordinate of the first arc point.
        :param y1: The y-coordinate of the first arc point.
        :param x2: The x-coordinate of the second arc point.
        :param y2: The y-coordinate of the second arc point.
        :param radius: The radius of the arc.'''
        ...
    
    def begin_path(self):
        '''Begins a new subpath, discarding the current path if any.'''
        ...
    
    def bezier_curve_to(self, cp_1x : float, cp_1y : float, cp_2x : float, cp_2y : float, x : float, y : float):
        '''Adds a cubic Bézier curve to the current path.
        
        :param cp_1x: The x-coordinate of the first control point.
        :param cp_1y: The y-coordinate of the first control point.
        :param cp_2x: The x-coordinate of the second control point.
        :param cp_2y: The y-coordinate of the second control point.
        :param x: The x-coordinate of the ending point.
        :param y: The y-coordinate of the ending point.'''
        ...
    
    def clear_rect(self, x : float, y : float, w : float, h : float):
        '''Clears the specified rectangular area to transparent.
        
        :param x: The x-coordinate of the top-left corner of the area to clear.
        :param y: The y-coordinate of the top-left corner of the area to clear.
        :param w: The width of the area to clear.
        :param h: The height of the area to clear.'''
        ...
    
    def close_path(self):
        '''Closes the current subpath by drawing a straight line from the current point to the starting point of the subpath.'''
        ...
    
    def draw_image(self, data : bytes, type : aspose.svg.drawing.WebImageFormat, rect : aspose.pydrawing.RectangleF):
        '''Draws an image on the canvas.
        
        :param data: The byte array representing the image data.
        :param type: The format of the image data. See :py:class:`aspose.svg.drawing.WebImageFormat`.
        :param rect: The destination rectangle where the image will be drawn.'''
        ...
    
    def fill_rect(self, x : float, y : float, w : float, h : float):
        '''Fills the specified rectangular area with the current fill style.
        
        :param x: The x-coordinate of the top-left corner of the rectangle.
        :param y: The y-coordinate of the top-left corner of the rectangle.
        :param w: The width of the rectangle.
        :param h: The height of the rectangle.'''
        ...
    
    def fill_text(self, text : str, x : float, y : float):
        '''Fills the specified text at the specified position.
        
        :param text: The text to fill.
        :param x: The x-coordinate of the starting position of the text.
        :param y: The y-coordinate of the starting position of the text.'''
        ...
    
    def get_path_rect(self) -> aspose.pydrawing.RectangleF:
        '''Gets the bounding rectangle of the current path.
        
        :returns: The bounding rectangle of the current path.'''
        ...
    
    def line_to(self, x : float, y : float):
        '''Adds a line segment to the current path.
        
        :param x: The x-coordinate of the ending point of the line segment.
        :param y: The y-coordinate of the ending point of the line segment.'''
        ...
    
    def measure_text(self, text : str) -> float:
        '''Measures the width of the specified text using the current font properties.
        
        :param text: The text to measure.
        :returns: The width of the text.'''
        ...
    
    def move_to(self, x : float, y : float):
        '''Moves the starting point of a new subpath to the specified point.
        
        :param x: The x-coordinate of the starting point.
        :param y: The y-coordinate of the starting point.'''
        ...
    
    def quadratic_curve_to(self, control_point_x : float, control_point_y : float, x : float, y : float):
        '''Adds a quadratic Bézier curve to the current path.
        
        :param control_point_x: The x-coordinate of the control point.
        :param control_point_y: The y-coordinate of the control point.
        :param x: The x-coordinate of the ending point.
        :param y: The y-coordinate of the ending point.'''
        ...
    
    def rect(self, x : float, y : float, width : float, height : float):
        '''Adds a rectangle to the current path.
        
        :param x: The x-coordinate of the top-left corner of the rectangle.
        :param y: The y-coordinate of the top-left corner of the rectangle.
        :param width: The width of the rectangle.
        :param height: The height of the rectangle.'''
        ...
    
    def restore_context(self):
        '''Restores the most recently saved canvas state by popping the top entry from the drawing state stack.'''
        ...
    
    def save_context(self):
        '''Saves the entire state of the canvas by pushing the current state onto a stack.'''
        ...
    
    def stroke_rect(self, x : float, y : float, width : float, height : float):
        '''Strokes the specified rectangular area.
        
        :param x: The x-coordinate of the top-left corner of the rectangle.
        :param y: The y-coordinate of the top-left corner of the rectangle.
        :param width: The width of the rectangle.
        :param height: The height of the rectangle.'''
        ...
    
    def stroke_text(self, text : str, x : float, y : float):
        '''Strokes the specified text at the specified position.
        
        :param text: The text to stroke.
        :param x: The x-coordinate of the starting position of the text.
        :param y: The y-coordinate of the starting position of the text.'''
        ...
    
    @property
    def context(self) -> aspose.svg.rendering.ICanvasContext:
        '''Gets the canvas context associated with the canvas.'''
        ...
    
    ...

class ICanvasContext:
    '''Represents the context of an HTML canvas 2D drawing.'''
    
    def transform(self, matrix : aspose.svg.drawing.IMatrix):
        '''Applies a transformation matrix to the context. See :py:class:`aspose.svg.drawing.IMatrix`.
        
        :param matrix: The transformation matrix.'''
        ...
    
    @property
    def shadow_offset_x(self) -> float:
        ...
    
    @shadow_offset_x.setter
    def shadow_offset_x(self, value : float):
        ...
    
    @property
    def shadow_offset_y(self) -> float:
        ...
    
    @shadow_offset_y.setter
    def shadow_offset_y(self, value : float):
        ...
    
    @property
    def shadow_blur(self) -> float:
        ...
    
    @shadow_blur.setter
    def shadow_blur(self, value : float):
        ...
    
    @property
    def shadow_color(self) -> aspose.pydrawing.Color:
        ...
    
    @shadow_color.setter
    def shadow_color(self, value : aspose.pydrawing.Color):
        ...
    
    @property
    def shadow_color_string(self) -> str:
        ...
    
    @shadow_color_string.setter
    def shadow_color_string(self, value : str):
        ...
    
    @property
    def text_align(self) -> int:
        ...
    
    @text_align.setter
    def text_align(self, value : int):
        ...
    
    @property
    def text_baseline(self) -> int:
        ...
    
    @text_baseline.setter
    def text_baseline(self, value : int):
        ...
    
    @property
    def global_alpha(self) -> float:
        ...
    
    @global_alpha.setter
    def global_alpha(self, value : float):
        ...
    
    @property
    def image_smoothing_enabled(self) -> bool:
        ...
    
    @image_smoothing_enabled.setter
    def image_smoothing_enabled(self, value : bool):
        ...
    
    @property
    def global_composite_operation(self) -> int:
        ...
    
    @global_composite_operation.setter
    def global_composite_operation(self, value : int):
        ...
    
    @property
    def letter_spacing(self) -> float:
        ...
    
    @letter_spacing.setter
    def letter_spacing(self, value : float):
        ...
    
    @property
    def font_value(self) -> str:
        ...
    
    @font_value.setter
    def font_value(self, value : str):
        ...
    
    @property
    def character_spacing(self) -> float:
        ...
    
    @character_spacing.setter
    def character_spacing(self, value : float):
        ...
    
    @property
    def fill_brush(self) -> aspose.svg.drawing.IBrush:
        ...
    
    @fill_brush.setter
    def fill_brush(self, value : aspose.svg.drawing.IBrush):
        ...
    
    @property
    def font(self) -> aspose.svg.drawing.ITrueTypeFont:
        '''Gets the font. See :py:class:`aspose.svg.drawing.ITrueTypeFont`.'''
        ...
    
    @font.setter
    def font(self, value : aspose.svg.drawing.ITrueTypeFont):
        '''Sets the font. See :py:class:`aspose.svg.drawing.ITrueTypeFont`.'''
        ...
    
    @property
    def font_size(self) -> float:
        ...
    
    @font_size.setter
    def font_size(self, value : float):
        ...
    
    @property
    def font_style(self) -> aspose.pydrawing.FontStyle:
        ...
    
    @font_style.setter
    def font_style(self, value : aspose.pydrawing.FontStyle):
        ...
    
    @property
    def line_cap(self) -> aspose.svg.drawing.StrokeLineCap:
        ...
    
    @line_cap.setter
    def line_cap(self, value : aspose.svg.drawing.StrokeLineCap):
        ...
    
    @property
    def line_dash_offset(self) -> float:
        ...
    
    @line_dash_offset.setter
    def line_dash_offset(self, value : float):
        ...
    
    @property
    def line_dash_pattern(self) -> List[float]:
        ...
    
    @line_dash_pattern.setter
    def line_dash_pattern(self, value : List[float]):
        ...
    
    @property
    def line_join(self) -> aspose.svg.drawing.StrokeLineJoin:
        ...
    
    @line_join.setter
    def line_join(self, value : aspose.svg.drawing.StrokeLineJoin):
        ...
    
    @property
    def line_width(self) -> float:
        ...
    
    @line_width.setter
    def line_width(self, value : float):
        ...
    
    @property
    def miter_limit(self) -> float:
        ...
    
    @miter_limit.setter
    def miter_limit(self, value : float):
        ...
    
    @property
    def stroke_brush(self) -> aspose.svg.drawing.IBrush:
        ...
    
    @stroke_brush.setter
    def stroke_brush(self, value : aspose.svg.drawing.IBrush):
        ...
    
    @property
    def text_info(self) -> aspose.svg.rendering.TextInfo:
        ...
    
    @property
    def transformation_matrix(self) -> aspose.svg.drawing.IMatrix:
        ...
    
    @transformation_matrix.setter
    def transformation_matrix(self, value : aspose.svg.drawing.IMatrix):
        ...
    
    ...

class ICanvasFactory:
    '''Represents a factory for creating instances of the canvas.'''
    
    def create(self, width : int, height : int) -> aspose.svg.rendering.ICanvas:
        '''Creates a new canvas with the specified width and height.
        
        :param width: The width of the canvas.
        :param height: The height of the canvas.
        :returns: A new instance of the :py:class:`aspose.svg.rendering.ICanvas`.'''
        ...
    
    ...

class ICanvasPathFactory:
    '''Represents a factory for creating canvas paths.'''
    
    @overload
    def create(self) -> aspose.svg.rendering.IPath:
        '''Creates a new empty path.
        
        :returns: The created :py:class:`aspose.svg.rendering.IPath`.'''
        ...
    
    @overload
    def create(self, path : aspose.svg.rendering.IPath) -> aspose.svg.rendering.IPath:
        '''Creates a new path by copying an existing path.
        
        :param path: The path to copy.
        :returns: The created :py:class:`aspose.svg.rendering.IPath`.'''
        ...
    
    ...

class IDevice:
    '''Defines methods and properties that support custom rendering of the graphic elements like paths, text and images.'''
    
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
        '''Appends a cubic Bézier curve to the current path. The curve extends from the current point to the point pt3,
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
    
    def draw_image(self, data : bytes, type : aspose.svg.drawing.WebImageFormat, rect : aspose.pydrawing.RectangleF):
        '''Draws the specified image.
        
        :param data: An array of bytes representing the image.
        :param type: Image type.
        :param rect: A rectangel which determines position and size to draw.'''
        ...
    
    def flush(self):
        '''Flushes all data to output stream.'''
        ...
    
    @property
    def options(self) -> aspose.svg.rendering.RenderingOptions:
        '''Gets rendering options.'''
        ...
    
    @property
    def graphic_context(self) -> aspose.svg.rendering.GraphicContext:
        ...
    
    ...

class IPath:
    '''Represents a path for defining shapes or outlines.'''
    
    @overload
    def arc(self, x : float, y : float, radius : float, start_angle : float, end_angle : float):
        '''Adds a circular arc to the path.
        
        :param x: The x-coordinate of the center of the arc.
        :param y: The y-coordinate of the center of the arc.
        :param radius: The radius of the arc.
        :param start_angle: The starting angle of the arc in radians.
        :param end_angle: The ending angle of the arc in radians.'''
        ...
    
    @overload
    def arc(self, x : float, y : float, radius : float, start_angle : float, end_angle : float, counterclockwise : bool):
        '''Adds a circular arc to the path.
        
        :param x: The x-coordinate of the center of the arc.
        :param y: The y-coordinate of the center of the arc.
        :param radius: The radius of the arc.
        :param start_angle: The starting angle of the arc in radians.
        :param end_angle: The ending angle of the arc in radians.
        :param counterclockwise: Specifies whether the arc should be drawn counterclockwise.'''
        ...
    
    @overload
    def ellipse(self, x : float, y : float, radius_x : float, radius_y : float, rotation : float, start_angle : float, end_angle : float):
        '''Adds an elliptical arc to the path.
        
        :param x: The x-coordinate of the center of the ellipse.
        :param y: The y-coordinate of the center of the ellipse.
        :param radius_x: The radius of the ellipse along the x-axis.
        :param radius_y: The radius of the ellipse along the y-axis.
        :param rotation: The rotation angle of the ellipse in radians.
        :param start_angle: The starting angle of the arc in radians.
        :param end_angle: The ending angle of the arc in radians.'''
        ...
    
    @overload
    def ellipse(self, x : float, y : float, radius_x : float, radius_y : float, rotation : float, start_angle : float, end_angle : float, anticlockwise : bool):
        '''Adds an elliptical arc to the path.
        
        :param x: The x-coordinate of the center of the ellipse.
        :param y: The y-coordinate of the center of the ellipse.
        :param radius_x: The radius of the ellipse along the x-axis.
        :param radius_y: The radius of the ellipse along the y-axis.
        :param rotation: The rotation angle of the ellipse in radians.
        :param start_angle: The starting angle of the arc in radians.
        :param end_angle: The ending angle of the arc in radians.
        :param anticlockwise: Specifies whether the arc should be drawn in the anticlockwise direction.'''
        ...
    
    def add_path(self, path : aspose.svg.rendering.IPath, transformation : aspose.svg.drawing.IMatrix):
        '''Adds the specified path to the current path, applying the given transformation.
        
        :param path: The path to add.
        :param transformation: The transformation to apply. See :py:class:`aspose.svg.drawing.IMatrix`.'''
        ...
    
    def clear(self):
        '''Clears the contents of the path.'''
        ...
    
    def close(self):
        '''Closes the current subpath by connecting the current point to the starting point.'''
        ...
    
    def move_to(self, x : float, y : float):
        '''Moves the current point to the specified coordinates.
        
        :param x: The x-coordinate of the destination point.
        :param y: The y-coordinate of the destination point.'''
        ...
    
    def line_to(self, x : float, y : float):
        '''Adds a straight line segment from the current point to the specified coordinates.
        
        :param x: The x-coordinate of the destination point.
        :param y: The y-coordinate of the destination point.'''
        ...
    
    def transform(self, transformation : aspose.svg.drawing.IMatrix):
        '''Applies the specified transformation to the path.
        
        :param transformation: The transformation matrix to apply.'''
        ...
    
    def quadratic_curve_to(self, control_point_x : float, control_point_y : float, end_point_x : float, end_point_y : float):
        '''Adds a quadratic Bézier curve segment to the path.
        
        :param control_point_x: The x-coordinate of the control point.
        :param control_point_y: The y-coordinate of the control point.
        :param end_point_x: The x-coordinate of the destination point.
        :param end_point_y: The y-coordinate of the destination point.'''
        ...
    
    def bezier_curve_to(self, control_point_1x : float, control_point_1y : float, control_point_2x : float, control_point_2y : float, end_point_x : float, end_point_y : float):
        '''Adds a cubic Bézier curve segment to the path.
        
        :param control_point_1x: The x-coordinate of the first control point.
        :param control_point_1y: The y-coordinate of the first control point.
        :param control_point_2x: The x-coordinate of the second control point.
        :param control_point_2y: The y-coordinate of the second control point.
        :param end_point_x: The x-coordinate of the destination point.
        :param end_point_y: The y-coordinate of the destination point.'''
        ...
    
    def arc_to(self, x1 : float, y1 : float, x2 : float, y2 : float, radius : float):
        '''Adds an arc segment to the path.
        
        :param x1: The x-coordinate of the first arc point.
        :param y1: The y-coordinate of the first arc point.
        :param x2: The x-coordinate of the second arc point.
        :param y2: The y-coordinate of the second arc point.
        :param radius: The radius of the arc.'''
        ...
    
    def rect(self, x : float, y : float, width : float, height : float):
        '''Adds a rectangle to the path.
        
        :param x: The x-coordinate of the upper-left corner of the rectangle.
        :param y: The y-coordinate of the upper-left corner of the rectangle.
        :param width: The width of the rectangle.
        :param height: The height of the rectangle.'''
        ...
    
    @property
    def fill_mode(self) -> aspose.svg.drawing.FillRule:
        ...
    
    @fill_mode.setter
    def fill_mode(self, value : aspose.svg.drawing.FillRule):
        ...
    
    @property
    def is_empty(self) -> bool:
        ...
    
    @property
    def native_object(self) -> any:
        ...
    
    ...

class ISVGDeviceContext:
    '''Represents a device context for SVG rendering.'''
    
    @property
    def device(self) -> aspose.svg.rendering.IDevice:
        '''Gets the underlying device associated with the context. See :py:class:`aspose.svg.rendering.IDevice`.'''
        ...
    
    @property
    def clip_strategy(self) -> aspose.svg.rendering.ClipStrategy:
        ...
    
    @clip_strategy.setter
    def clip_strategy(self, value : aspose.svg.rendering.ClipStrategy):
        ...
    
    @property
    def is_glyphs_rendering_supported(self) -> bool:
        ...
    
    ...

class ISVGDeviceContextFactory:
    '''Represents a factory for creating SVG device contexts.'''
    
    def create(self, device : aspose.svg.rendering.IDevice, renderer_service : aspose.svg.rendering.ISVGElementRendererService) -> aspose.svg.rendering.ISVGDeviceContext:
        '''Creates an SVG device context with the specified device and renderer service.
        
        :param device: The device associated with the context. See :py:class:`aspose.svg.rendering.IDevice`
        :param renderer_service: The renderer service used for rendering SVG elements.
        :returns: The created :py:class:`aspose.svg.rendering.ISVGDeviceContext`.'''
        ...
    
    ...

class ISVGElementRendererService:
    '''Represents a service for rendering SVG elements.'''
    
    ...

class ISVGRenderContext:
    '''Represents a rendering context for SVG rendering.'''
    
    ...

class ISVGRenderContextFactory:
    '''Represents a factory for creating SVG render contexts.'''
    
    def create(self, device_context : aspose.svg.rendering.ISVGDeviceContext, resolving_context : aspose.svg.rendering.styles.ISVGPropertyResolvingContext) -> aspose.svg.rendering.ISVGRenderContext:
        '''Creates a new instance of the SVG render context.
        
        :param device_context: The SVG device context used for rendering. See :py:class:`aspose.svg.rendering.ISVGDeviceContext`.
        :param resolving_context: The SVG property resolving context. See :py:class:`aspose.svg.rendering.styles.ISVGPropertyResolvingContext`.
        :returns: The created SVG render context.'''
        ...
    
    ...

class PageSetup:
    '''Represents a page setup object is used for configuration output page-set.'''
    
    def set_left_right_page(self, left_page : aspose.svg.drawing.Page, right_page : aspose.svg.drawing.Page):
        '''Sets the Left/Right page configuration.
        
        :param left_page: The left page.
        :param right_page: The right page.'''
        ...
    
    @property
    def at_page_priority(self) -> aspose.svg.rendering.AtPagePriority:
        ...
    
    @at_page_priority.setter
    def at_page_priority(self, value : aspose.svg.rendering.AtPagePriority):
        ...
    
    @property
    def left_page(self) -> aspose.svg.drawing.Page:
        ...
    
    @property
    def right_page(self) -> aspose.svg.drawing.Page:
        ...
    
    @property
    def any_page(self) -> aspose.svg.drawing.Page:
        ...
    
    @any_page.setter
    def any_page(self, value : aspose.svg.drawing.Page):
        ...
    
    @property
    def first_page(self) -> aspose.svg.drawing.Page:
        ...
    
    @first_page.setter
    def first_page(self, value : aspose.svg.drawing.Page):
        ...
    
    @property
    def sizing(self) -> aspose.svg.rendering.SizingType:
        '''Gets the sizing type.'''
        ...
    
    @sizing.setter
    def sizing(self, value : aspose.svg.rendering.SizingType):
        '''Sets the sizing type.'''
        ...
    
    ...

class Renderer:
    '''Represents a base class for all renderers and implemnts IDisposable interface.'''
    
    ...

class RenderingOptions:
    '''Represents rendering options.'''
    
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
    
    ...

class SvgRenderer(Renderer):
    '''Represents SVG document renderer.'''
    
    @overload
    def render(self, device : aspose.svg.rendering.IDevice, timeout : TimeSpan, sources : List[aspose.svg.SVGDocument]):
        ...
    
    @overload
    def render(self, device : aspose.svg.rendering.IDevice, source : aspose.svg.SVGDocument):
        ...
    
    @overload
    def render(self, device : aspose.svg.rendering.IDevice, source : aspose.svg.SVGDocument, timeout : TimeSpan):
        ...
    
    @overload
    def render(self, device : aspose.svg.rendering.IDevice, source : aspose.svg.SVGDocument, timeout : int):
        ...
    
    @overload
    def render(self, device : aspose.svg.rendering.IDevice, sources : List[aspose.svg.SVGDocument]):
        ...
    
    @overload
    def render(self, device : aspose.svg.rendering.IDevice, timeout : int, sources : List[aspose.svg.SVGDocument]):
        ...
    
    ...

class TextInfo:
    '''Contains information about rendered text.'''
    
    @property
    def glyph_infos(self) -> List[aspose.svg.rendering.GlyphInfo]:
        ...
    
    ...

class AtPagePriority:
    '''Specifies possible orders of applying page size declarations.'''
    
    @classmethod
    @property
    def OPTIONS_PRIORITY(cls) -> AtPagePriority:
        '''Specifies that :py:class:`aspose.svg.rendering.PageSetup` values declared in :py:class:`aspose.svg.rendering.RenderingOptions` will override values defined in css by ``@page`` rules :link:`https://www.w3.org/TR/CSS2/page.html#page-selectors`.'''
        ...
    
    @classmethod
    @property
    def CSS_PRIORITY(cls) -> AtPagePriority:
        '''Specifies that ``@page`` rules :link:`https://www.w3.org/TR/CSS2/page.html#page-selectors` defined in css will override values defined in :py:class:`aspose.svg.rendering.PageSetup`.'''
        ...
    
    ...

class ClipStrategy:
    '''Specifies the strategy for clipping an SVG element.
    This enum is used to determine how to apply clipping paths or masks to SVG elements during rendering.'''
    
    @classmethod
    @property
    def NONE(cls) -> ClipStrategy:
        '''Indicates that no clipping will be applied to the SVG element.
        This strategy is used when there is no clip-path or mask associated with the SVG element.'''
        ...
    
    @classmethod
    @property
    def MASK(cls) -> ClipStrategy:
        '''This strategy applies a mask for clipping.
        This strategy is used when the SVG element has a mask element applied to it.
        Instead of clipping the canvas, a mask layer is used to determine the visibility of the SVG element.
        A mask is an image where the alpha value of each pixel is used
        to determine the visibility of the corresponding pixel in the SVG element.'''
        ...
    
    @classmethod
    @property
    def PATH(cls) -> ClipStrategy:
        '''This strategy uses a path for clipping.
        This strategy is used when the SVG element has a clipPath element applied to it.
        A clipPath is a region defined by a path; anything outside of this path is clipped out.'''
        ...
    
    ...

class MediaType:
    '''Specifies possible media types used during rendering.'''
    
    @classmethod
    @property
    def PRINT(cls) -> MediaType:
        '''The ``Print`` media is used during rendering.'''
        ...
    
    @classmethod
    @property
    def SCREEN(cls) -> MediaType:
        '''The ``Screen`` media is used during rendering.'''
        ...
    
    ...

class SizingType:
    '''Represents the enumeration of page sizing types.'''
    
    @classmethod
    @property
    def FIT_CONTENT(cls) -> SizingType:
        '''Changing given sizes of the page to fit the size of the content it contains.'''
        ...
    
    @classmethod
    @property
    def SCALE_CONTENT(cls) -> SizingType:
        '''Scaling a content size in accordance to the given size of the page.'''
        ...
    
    @classmethod
    @property
    def CONTAIN(cls) -> SizingType:
        '''Fitting the content size to the page size while maintaining the preferred aspect ratio insofar as possible.'''
        ...
    
    @classmethod
    @property
    def CROP(cls) -> SizingType:
        '''Placing the content on page and crop everything that out of given page size.'''
        ...
    
    ...

