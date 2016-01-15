#!/usr/bin/env python
# encoding: utf-8

import objc
from Foundation import *
from AppKit import *
import sys, os, re

MainBundle = NSBundle.mainBundle()
path = MainBundle.bundlePath() + "/Contents/Scripts"
if not path in sys.path:
	sys.path.append( path )

import GlyphsApp

GlyphsReporterProtocol = objc.protocolNamed( "GlyphsReporter" )

class ShowFilledPreview ( NSObject, GlyphsReporterProtocol ):
	
	def init( self ):
		"""
		Put any initializations you want to make here.
		"""
		try:
			return self
		except Exception as e:
			self.logToConsole( "init: %s" % str(e) )
		
	def title( self ):
		"""
		This is the name as it appears in the menu in combination with 'Show'.
		E.g. 'return "Nodes"' will make the menu item read "Show Nodes".
		"""
		return "Filled Preview while Editing"
		
	def interfaceVersion( self ):
		"""
		Must return 1.
		"""
		try:
			return 1
		except Exception as e:
			self.logToConsole( "interfaceVersion: %s" % str(e) )
		
	def keyEquivalent( self ):
		"""
		The key for the keyboard shortcut. Set modifier keys in modifierMask() further below.
		Pretty tricky to find a shortcut that is not taken yet, so be careful.
		If you are not sure, use 'return None'. Users can set their own shortcuts in System Prefs.
		"""
		try:
			return None
		except Exception as e:
			self.logToConsole( "keyEquivalent: %s" % str(e) )
		
	def modifierMask( self ):
		"""
		Use any combination of these to determine the modifier keys for your default shortcut:
			return NSShiftKeyMask | NSControlKeyMask | NSCommandKeyMask | NSAlternateKeyMask
		Or:
			return 0
		... if you do not want to set a shortcut.
		"""
		try:
			return 0
		except Exception as e:
			self.logToConsole( "modifierMask: %s" % str(e) )
		
	def drawForegroundForLayer_( self, Layer ):
		"""
		Whatever you draw here will be displayed IN FRONT OF the paths.
		"""
		try:
			pass
		except Exception as e:
			self.logToConsole( "drawForegroundForLayer_: %s" % str(e) )

	def bezierPathComp( self, thisPath ):
		"""Compatibility method for bezierPath before v2.3."""
		try:
			return thisPath.bezierPath() # until v2.2
		except Exception as e:
			return thisPath.bezierPath # v2.3+

	def drawLayerOpenOrClosed( self, Layer ):
		try:
			if len( Layer.paths ) > 0:
				try:
					self.bezierPathComp(Layer).fill()
				except:
					pass # Layer.bezierPath() is None
				
				try:
					Layer.openBezierPath().fill()
					# sometimes leaves traces (ghost paths) after deletion
					# the if statement above should fix this
					# please report if ghost paths still occur
				except:
					pass # Layer.openBezierPath() is None
		except Exception as e:
			self.logToConsole( "drawLayerOpenOrClosed: %s" % str(e) )
			
	
	def drawBackgroundForLayer_( self, Layer ):
		"""
		Whatever you draw here will be displayed BEHIND the paths.
		"""
		try:
			NSColor.darkGrayColor().set()
			self.drawLayerOpenOrClosed( Layer )
		except Exception as e:
			self.logToConsole( "drawBackgroundForLayer_: %s" % str(e) )
			
	def needsExtraMainOutlineDrawingForInactiveLayer_( self, Layer ):
		"""
		Whatever you draw here will be displayed in the Preview at the bottom.
		Remove the method or return True if you want to leave the Preview untouched.
		Return True to leave the Preview as it is and draw on top of it.
		Return False to disable the Preview and draw your own.
		In that case, don't forget to add Bezier methods like in drawForegroundForLayer_(),
		otherwise users will get an empty Preview.
		"""
		try:
			return False
		except Exception as e:
			return True
	
	def drawBackgroundForInactiveLayer_( self, Layer ):
		"""
		Whatever you draw here will be displayed behind the paths, but for inactive masters.
		"""
		try:
			# Color for INACTIVE GLYPH IN EDIT VIEW
			if self.controller:
				# set the drawing color to black:
				NSColor.blackColor().set()

			# Color for GLYPH IN PREVIEW:	
			else:
				# check for background color (can be black or white):
				if NSUserDefaults.standardUserDefaults().boolForKey_("GSPreview_Black"):
					# set the drawing color to white if preview background is black:
					NSColor.whiteColor().set()
				else:
					# set the drawing color to black if preview background is white:
					NSColor.blackColor().set()
			
			self.drawLayerOpenOrClosed( Layer )
		except Exception as e:
			self.logToConsole( "drawBackgroundForInactiveLayer_: %s" % str(e) )
			
	def setController_( self, Controller ):
		"""
		Use self.controller as object for the current view controller.
		"""
		try:
			self.controller = Controller
		except Exception as e:
			self.logToConsole( "setController_: %s" % str(e) )
		
	def logToConsole( self, message ):
		"""
		The variable 'message' will be passed to Console.app.
		Use self.logToConsole( "bla bla" ) for debugging.
		"""
		myLog = "Show %s plugin:\n%s" % ( self.title(), message )
		print myLog
		NSLog( myLog )
