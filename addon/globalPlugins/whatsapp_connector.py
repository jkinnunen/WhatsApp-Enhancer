import globalPluginHandler
import appModuleHandler
import addonHandler
import config
import gui
import wx
from gui.settingsDialogs import SettingsPanel, NVDASettingsDialog

addonHandler.initTranslation()

SPEC = {
	'filter_phone_numbers_chat': 'boolean(default=False)',
	'filter_phone_numbers_messages': 'boolean(default=True)',
	'read_usage_hints': 'boolean(default=True)',
	'disable_browse_mode_lock': 'boolean(default=False)',
}

class WhatsAppEnhancerSettings(SettingsPanel):
	title = _("WhatsApp Enhancer")

	def makeSettings(self, settingsSizer):
		s = gui.guiHelper.BoxSizerHelper(self, sizer=settingsSizer)
		c = config.conf.get("WhatsAppEnhancer", {})
		self.filter_phone_numbers_chat = s.addItem(wx.CheckBox(self, label=_("Filter phone numbers in chat list")))
		self.filter_phone_numbers_chat.SetValue(bool(c.get("filter_phone_numbers_chat", False)))
		self.filter_phone_numbers_messages = s.addItem(wx.CheckBox(self, label=_("Filter phone numbers in message list")))
		self.filter_phone_numbers_messages.SetValue(bool(c.get("filter_phone_numbers_messages", True)))
		self.read_usage_hints = s.addItem(wx.CheckBox(self, label=_("Read usage hints while navigating chat list")))
		self.read_usage_hints.SetValue(bool(c.get("read_usage_hints", True)))
		self.disable_browse_mode_lock = s.addItem(wx.CheckBox(self, label=_("Disable browse mode lock (not recommended)")))
		self.disable_browse_mode_lock.SetValue(bool(c.get("disable_browse_mode_lock", False)))

	def onSave(self):
		if "WhatsAppEnhancer" not in config.conf:
			config.conf["WhatsAppEnhancer"] = {}
		c = config.conf["WhatsAppEnhancer"]
		c["filter_phone_numbers_chat"] = self.filter_phone_numbers_chat.IsChecked()
		c["filter_phone_numbers_messages"] = self.filter_phone_numbers_messages.IsChecked()
		c["read_usage_hints"] = self.read_usage_hints.IsChecked()
		c["disable_browse_mode_lock"] = self.disable_browse_mode_lock.IsChecked()
		config.conf.save()

class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	def __init__(self):
		super().__init__()
		config.conf.spec['WhatsAppEnhancer'] = SPEC
		appModuleHandler.registerExecutableWithAppModule("WhatsApp", "whatsapp_root")
		appModuleHandler.registerExecutableWithAppModule("WhatsApp.Root", "whatsapp_root")
		NVDASettingsDialog.categoryClasses.append(WhatsAppEnhancerSettings)

	def terminate(self):
		appModuleHandler.unregisterExecutable("WhatsApp")
		appModuleHandler.unregisterExecutable("WhatsApp.Root")
		if WhatsAppEnhancerSettings in NVDASettingsDialog.categoryClasses:
			NVDASettingsDialog.categoryClasses.remove(WhatsAppEnhancerSettings)
		config.conf.spec.pop('WhatsAppEnhancer', None)
		super().terminate()
