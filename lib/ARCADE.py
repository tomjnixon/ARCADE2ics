#!/usr/bin/python
# A wrapper for the command-line ARCADE client
# (Originally from the ARCADE in English, ARCADEie, project)

import subprocess, os

class ArcadeClient:
	"""
	A class which may (one day) become a full arcade wrapper allowing all kinds of
	data to be pulled nicely from arcade.
	"""
	def _getOutputFromCommand(self, command):
		# Remove the display environment variable to force arcade into cli mode
		del os.environ["DISPLAY"]
		
		# A file to write arcade errors into
		arcadeErrors = open("ARCADE_errors.log","w")
		
		arcade = subprocess.Popen(["arcade"], env=os.environ,
		                                      stdin=subprocess.PIPE,
		                                      stderr=arcadeErrors,
		                                      stdout=subprocess.PIPE)
		output, _ = arcade.communicate(command)
		return output
	
	def getTimetable(self):
		rawArcadeOutput = self._getOutputFromCommand("c7qqrx")
		
		# Convert line-endings to unix-style
		arcadeOutput = rawArcadeOutput.replace("\n\r","\n")
		return arcadeOutput
