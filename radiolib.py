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

		self.PiFmDma_installed = True
		self.RTLFM_installed = True

		status, result = commands.getstatusoutput("which ./minimodem")
		if status > 0:
			raise OSError("Minimodem not found")

		status, result = commands.getstatusoutput("which rtl_fm")
		if status > 0:
			#print "[WARNING] RLT_FM not found."
			self.RTLFM_installed = False

		status, result = commands.getstatusoutput("which aplay")
		if status > 0:
			raise OSError("Aplay not found")

		status, result = commands.getstatusoutput("which ./PiFmDma")
		if status > 0:
			#print "[WARNING] PiFmDma not found"
			self.PiFmDma_installed = False


	#sending something over a freqency
	def send(self, data, freq, baud):
		if not self.PiFmDma_installed:
			raise OSError("PiFmDma is not installed: Cannot transmit")

		#encoding it into sound
		p1 = Popen(["echo", "-e", data], stdout=PIPE)
		p2 = Popen(["sudo", "./minimodem", "--tx", "-8", "-R", "18000", "-f", "send.wav", baud], stdin=p1.stdout, stdout=PIPE)

		#sending it with pifmdma
		call(["./PiFmDma", "send.wav", freq])

	#listening on a frequency
	def listen(self, freq, baud):
		if not self.RTLFM_installed:
			raise OSError("RTL_FM is not installed: Cannot listen")

		#rtl_fm -f 103.3e6 -W -s 200000 -r 48000 - | aplay -r 48k -f S16_LE
		self.rtlfm = Popen(["rtl_fm", "-f", str(freq) + "e6", "-W", "-s", "200000", "-r", "48000", "-"], stdout=PIPE)
		self.aplay = Popen(["aplay", "-r", "48k", "-f", "S16_LE"], stdin=self.rtlfm.stdout, stdout=PIPE)

		self.minimodem = Popen(["./minimodem", "--rx", "-8", "-q", baud], stdout=PIPE)