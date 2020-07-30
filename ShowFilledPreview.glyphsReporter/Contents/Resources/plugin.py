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
		try:
			self.opacity = float( Glyphs.defaults["com.mekkablue.ShowFilledPreview.opacity"] )
			if self.opacity < 0.0:
				self.opacity = 0.0
			elif self.opacity > 1.0:
				self.opacity = 1.0
		except:
			self.opacity = 1.0

	@objc.python_method
	def drawLayerOpenOrClosed( self, layer ):
		try:
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
		NSColor.disabledControlTextColor().colorWithAlphaComponent_(self.opacity).set()
		self.drawLayerOpenOrClosed( layer )

	@objc.python_method
	def inactiveLayerForeground(self, layer):
		NSColor.controlTextColor().colorWithAlphaComponent_(self.opacity).set()
		self.drawLayerOpenOrClosed( layer )

	@objc.python_method
	def preview(self, layer):
		if Glyphs.defaults["GSPreview_Black"]:
			NSColor.whiteColor().colorWithAlphaComponent_(self.opacity).set()
		else:
			NSColor.blackColor().colorWithAlphaComponent_(self.opacity).set()
			
		self.drawLayerOpenOrClosed(layer)

	@objc.python_method
	def needsExtraMainOutlineDrawingForInactiveLayer_(self, layer=None):
		return True	