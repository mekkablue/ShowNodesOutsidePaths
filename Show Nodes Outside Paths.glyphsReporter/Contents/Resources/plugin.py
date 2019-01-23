# encoding: utf-8

###########################################################################################################
#
#
#	Reporter Plugin
#
#	Read the docs:
#	https://github.com/schriftgestalt/GlyphsSDK/tree/master/Python%20Templates/Reporter
#
#
###########################################################################################################

import objc
from GlyphsApp import *
from GlyphsApp.plugins import *

class ShowNodesOutsidePaths(ReporterPlugin):

	def settings(self):
		self.menuName = Glyphs.localize({
			'en': u'Nodes Outside Paths',
			'de': u'Punkte außerhalb von Pfaden',
		})
	
	def roundDotForPoint( self, thisPoint, markerWidth ):
		"""
		Returns a circle with thisRadius around thisPoint.
		"""
		myRect = NSRect( ( thisPoint.x - markerWidth * 0.5, thisPoint.y - markerWidth * 0.5 ), ( markerWidth, markerWidth ) )
		return NSBezierPath.bezierPathWithOvalInRect_(myRect)
	
	def drawHandleForNode(self, node, sizeFactor=1.0):
		# calculate handle size:
		handleSizeIndex = Glyphs.handleSize # user choice in Glyphs > Preferences > User Preferences > Handle Size
		handleSize = (5, 8, 12)[handleSizeIndex]*sizeFactor*self.getScale()**-0.9 # scaled diameter
	
		# # offcurves are a little smaller:
		# if node.type == OFFCURVE:
		# 	handleSize *= 0.8
	
		# selected handles are a little bigger:
		if node.selected:
			handleSize *= 1.45
	
		# draw disc inside a rectangle around point position:
		position = node.position
		rect = NSRect()
		rect.origin = NSPoint(position.x-handleSize/2, position.y-handleSize/2)
		rect.size = NSSize(handleSize, handleSize)
		return NSBezierPath.bezierPathWithOvalInRect_(rect)
	
		
	def background(self, layer):
		if self.getScale() > 0.099:
			bezierPaths = [p.bezierPath for p in layer.paths]
			for path in layer.paths:
				for node in path.nodes:
					if node.type != OFFCURVE:
						position = node.position
						pathCount = 0
						for bezierPath in bezierPaths:
							if bezierPath.containsPoint_(position):
								pathCount += 1
						if pathCount == 1:
							# fill:
							NSColor.whiteColor().set()
							handle = self.drawHandleForNode(node, sizeFactor=2)
							handle.fill()
							# contour:
							NSColor.blueColor().set()
							handle.setLineWidth_( 5.0 * self.getScale() ** -0.9 )
							handle.stroke()

	def __file__(self):
		"""Please leave this method unchanged"""
		return __file__
