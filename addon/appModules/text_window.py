import wx
import gui

_active_window = None

class TextWindow(wx.Frame):
	def __init__(self, text, title, insertionPoint=0):
		global _active_window
		if _active_window:
			try:
				_active_window.Close()
			except Exception:
				pass
			_active_window = None
		super().__init__(gui.mainFrame, title=title)
		_active_window = self
		self.Bind(wx.EVT_CLOSE, self.onClose)
		sizer = wx.BoxSizer(wx.VERTICAL)
		style = wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_RICH
		self.outputCtrl = wx.TextCtrl(self, style=style)
		self.outputCtrl.Bind(wx.EVT_KEY_DOWN, self.onOutputKeyDown)
		sizer.Add(self.outputCtrl, proportion=1, flag=wx.EXPAND)
		self.SetSizer(sizer)
		sizer.Fit(self)
		self.outputCtrl.SetValue(text)
		self.outputCtrl.SetFocus()
		self.outputCtrl.SetInsertionPoint(insertionPoint)
		self.Raise()
		self.Maximize()
		self.Show()

	def onOutputKeyDown(self, event):
		if event.GetKeyCode() == wx.WXK_ESCAPE:
			self.Close()
		event.Skip()

	def onClose(self, event):
		global _active_window
		if _active_window is self:
			_active_window = None
		event.Skip()

