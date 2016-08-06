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


from GlyphsApp.plugins import *

class ShowFilledPreview(ReporterPlugin):

	def settings(self):
		self.menuName = Glyphs.localize({
			'en': u'Filled Preview while Editing', 
			'de': u'Gefüllte Vorschau beim Bearbeiten'
		})

	def drawLayerOpenOrClosed( self, Layer ):
		try:
			if len( Layer.paths ) > 0:
				try:
					Layer.bezierPath.fill()
				except:
					pass # Layer.bezierPath() is None
				
				try:
					Layer.openBezierPath.fill()
					# sometimes leaves traces (ghost paths) after deletion
					# the if statement above should fix this
					# please report if ghost paths still occur
				except:
					pass # Layer.openBezierPath is None
		except Exception as e:
			self.logToConsole( "drawLayerOpenOrClosed: %s" % str(e) )
		
	def background(self, layer):
		NSColor.darkGrayColor().set()
		self.drawLayerOpenOrClosed( layer )

	def preview(self, layer):
		if NSUserDefaults.standardUserDefaults().boolForKey_("GSPreview_Black"):
			# set the drawing color to white if preview background is black:
			NSColor.whiteColor().set()
		else:
			# set the drawing color to black if preview background is white:
			NSColor.blackColor().set()
		
		if layer.paths:
			layer.bezierPath.fill()
			layer.openBezierPath.fill()
		if layer.components:
			for component in layer.components:
				component.bezierPath.fill()

	def inactiveLayers(self, layer):
		NSColor.blackColor().set()
		layer.openBezierPath.fill()
	
	def needsExtraMainOutlineDrawingForInactiveLayer_(self, layer):
		return True
	