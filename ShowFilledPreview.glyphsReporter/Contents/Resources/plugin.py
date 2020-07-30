# encoding: utf-8
from __future__ import division, print_function, unicode_literals

###########################################################################################################
#
#	Reporter Plugin
#
#	Read the docs:
#	https://github.com/schriftgestalt/GlyphsSDK/tree/master/Python%20Templates/Reporter
#
###########################################################################################################

from GlyphsApp.plugins import *

class ShowFilledPreview(ReporterPlugin):
	@objc.python_method
	def settings(self):
		self.menuName = Glyphs.localize({
			'en': u'Filled Preview while Editing', 
			'de': u'Gefüllte Vorschau beim Bearbeiten',
			'es': u'contornos rellenos durante la edición',
			'fr': u'aperçu des formes pendant la édition',
		})
		Glyphs.registerDefault( "com.mekkablue.ShowFilledPreview.opacity", 1.0 )

	@objc.python_method
	def drawLayerOpenOrClosed( self, layer, color ):
		try:
			self.opacity = float( Glyphs.defaults["com.mekkablue.ShowFilledPreview.opacity"] )
			if self.opacity < 0.0 or self.opacity > 1.0:
				raise ValueError
		except:
			Glyphs.defaults["com.mekkablue.ShowFilledPreview.opacity"] = self.opacity = 1.0
		
		try:
			color.colorWithAlphaComponent_(self.opacity).set()
			if layer.paths:
				try:
					layer.bezierPath.fill()
				except:
					pass
				try:
					layer.openBezierPath.fill()
				except:
					pass
					
			for component in layer.components:
				# component.bezierPath.fill() # already included in layer.bezierPath 
				component.openBezierPath().fill()
		except Exception as e:
			import traceback
			print(traceback.format_exc())
			self.logToConsole( "drawLayerOpenOrClosed: %s" % str(e) )
		
	@objc.python_method
	def background(self, layer):
		self.drawLayerOpenOrClosed( layer, NSColor.disabledControlTextColor() )

	@objc.python_method
	def inactiveLayerForeground(self, layer):
		self.drawLayerOpenOrClosed( layer, NSColor.controlTextColor() )

	@objc.python_method
	def preview(self, layer):
		if Glyphs.defaults["GSPreview_Black"]:
			self.drawLayerOpenOrClosed(layer, NSColor.whiteColor() )
		else:
			self.drawLayerOpenOrClosed(layer, NSColor.blackColor() )

	@objc.python_method
	def needsExtraMainOutlineDrawingForInactiveLayer_(self, layer=None):
		return True	