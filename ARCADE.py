#!/usr/bin/python
# A wrapper for the command-line ARCADE client
# (Originally from the ARCADE in English, ARCADEie, project)

import subprocess

class ArcadeClient:
	"""
	A class which may (one day) become a full arcade wrapper allowing all kinds of
	data to be pulled nicely from arcade.
	"""
	def _getOutputFromCommand(self, command):
		print "Starting arcade..."
		arcade = subprocess.popen(["arcade"], stdin=subprocess.PIPE,
		                                      stdout=subprocess.PIPE)
		print "Running arcade command '%s'..."%(command)
		output, _ = arcade.communicate(command)
		print "Done!"
		return output
	
	@property
	def timetable(self):
		rawArcadeOutput = self._getOutputFromCommand("c7qqrx")
		
		# The actual data is contained between bars of =
		usefulSection = rawArcadeOutput.split("="*79)[1]
		
		# Convert line-endings to unix-style
		usefulSection = usefulSection.replace("\n\r","\n")
		return usefulSection
