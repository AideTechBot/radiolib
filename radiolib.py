"""
radiolib

a library for sending and receiving data with a raspberry pi (basically just a wrapper for pifmdma and rtl_fm)

written by Aidetechbot
"""
import commands
from subprocess import *

class Radio:
	#initialization
	def __init__(self):

		PiFmDma_installed = True
		RTLFM_installed = True

		status, result = commands.getstatusoutput("./minimodem")
		if status > 0:
			raise OSError("Minimodem not found")

		status, result = commands.getstatusoutput("rtl_fm")
		if status > 0:
			print "[WARNING] RLT_FM not found."
			RTLFM_installed = False

		status, result = commands.getstatusoutput("aplay")
		if status > 0:
			raise OSError("Aplay not found")

		status, result = commands.getstatusoutput("./PiFmDma")
		if status > 0:
			print "[WARNING] PiFmDma not found"
			PiFmDma_installed = False


	#sending something over a freqency
	def send(self, message, freq, baud):
		if not PiFmDma_installed:
			raise OSError("PiFmDma is not installed: Cannot transmit")

		#encoding it into sound
		p1 = Popen(["echo", "-e", data], stdout=PIPE)
		p2 = Popen(["sudo", "./minimodem", "--tx", "-8", "-R", "18000", "-f", "send.wav", baud])

		#sending it with pifmdma
		call(["./PiFmDma",freq])
		

	#listening on a frequency
	def listen(self, freq):
		if not RTLFM_installed:
			raise OSError("RTL_FM is not installed: Cannot listen")
	#reading one char only
	def read_char(self,pos):

	#reading a line 
	def read_line(self):
