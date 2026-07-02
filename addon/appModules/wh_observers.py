import ui
import queueHandler
from threading import Timer
import config
from nvwave import playWaveFile
import os
import controlTypes
import api
import addonHandler

addonHandler.initTranslation()

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "media"))

class ProgressObserver:
	active = False
	interval = 1.0
	progress_obj = None
	last_val = None

	@classmethod
	def start(cls):
		obj = api.getFocusObject()
		cls.progress_obj = None
		if obj and getattr(obj, "childCount", 0) > 0:
			try:
				for child in getattr(obj, "children", []):
					if child and child.role == controlTypes.Role.PROGRESSBAR:
						cls.progress_obj = child
						break
			except:
				pass
		if cls.progress_obj:
			cls.active = True
			cls.tick()

	@classmethod
	def tick(cls):
		if not cls.active or not cls.progress_obj: return
		try:
			val = cls.progress_obj.value or cls.progress_obj.name
			if not cls.last_val or cls.last_val != val:
				ui.message(_("Progress: {val}").format(val=val))
				cls.last_val = val
			import wx
			wx.CallLater(int(cls.interval * 1000), cls.tick)
		except:
			cls.active = False
