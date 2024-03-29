# Copyright (C) 2021-2023 Himadri Sekhar Basu <hsb10@iitbbs.ac.in>
#
# This file is part of simple-pwgen.
#
# simple-pwgen is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# simple-pwgen is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with simple-pwgen. If not, see <http://www.gnu.org/licenses/>
# or write to the Free Software Foundation, Inc., 51 Franklin Street,
# Fifth Floor, Boston, MA 02110-1301, USA..
#
# Author: Himadri Sekhar Basu <hsb10@iitbbs.ac.in>
#

# import the necessary modules!
import gettext
import gi
import locale
import setproctitle
import warnings

# Suppress GTK deprecation warnings
warnings.filterwarnings("ignore")

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gio, Gdk

from SimplePwgen.common import APP, CONFIG_FILE, LOCALE_DIR, UI_PATH, __version__, methods, PasswordGenerator

setproctitle.setproctitle(APP)

# i18n
locale.bindtextdomain(APP, LOCALE_DIR)
gettext.bindtextdomain(APP, LOCALE_DIR)
gettext.textdomain(APP)
_ = gettext.gettext

class simple_pwgen(Gtk.Application):
	# Main initialization routine
	def __init__(self, application_id, flags):
		Gtk.Application.__init__(self, application_id=application_id, flags=flags)
		self.connect("activate", self.activate)

	def activate(self, application):
		windows = self.get_windows()
		if (len(windows) > 0):
			window = windows[0]
			window.present()
			window.show()
		else:
			window = SimplepwgenWindow(self)
			self.add_window(window.window)
			window.window.show()
	
class SimplepwgenWindow():
	
	def __init__(self, application):
		
		self.application = application
		self.settings = Gio.Settings(schema_id="org.mamolinux.simple-pwgen")
		self.generator = PasswordGenerator()
		self.icon_theme = Gtk.IconTheme.get_default()
		
		# Set the Glade file
		main_window = UI_PATH + "simple-pwgen.ui"
		defaultmethod = UI_PATH + "default-method.ui"
		dicemethod = UI_PATH + "diceware-method.ui"
		pin_generation = UI_PATH + "pin-generation.ui"
		self.builder = Gtk.Builder()
		self.builder.add_from_file(main_window)
		self.builder.add_from_file(defaultmethod)
		self.builder.add_from_file(dicemethod)
		self.builder.add_from_file(pin_generation)
		self.window = self.builder.get_object("MainWindow")
		main_box = self.builder.get_object("main_box")
		self.window.set_title(_("Simple Password Generator"))
		
		# Create variables to quickly access dynamic widgets
		# Combo box
		methods_store = Gtk.ListStore(str)
		self.methods = methods
		for method in self.methods:
			methods_store.append([method])
		self.method_combo = self.builder.get_object("method_name_combo")
		renderer = Gtk.CellRendererText()
		self.method_combo.pack_start(renderer, True)
		self.method_combo.add_attribute(renderer, "text", 0)
		self.method_combo.set_model(methods_store)
		
		# Attach input UIs
		# default method
		self.default_method = self.builder.get_object("default_input")
		main_box.pack_start(self.default_method, True, True, 0)
		main_box.reorder_child(self.default_method, 1)
		
		# # PIN Generation
		# self.gen_pin = self.builder.get_object("pin_input")
		# main_box.pack_start(self.gen_pin, True, True, 0)
		# main_box.reorder_child(self.gen_pin, 1)
		# self.gen_pin.set_visible(False)
		
		# # Diceware method
		# self.dice_method = self.builder.get_object("diceware_input")
		# main_box.pack_start(self.dice_method, True, True, 0)
		# main_box.reorder_child(self.dice_method, 1)
		# self.gen_pin.set_visible(False)
		
		# input values
		self.pwlengthfield = self.builder.get_object("pwlengthfield")
		self.lcase_switch = self.builder.get_object("lcase_switch")
		self.minlcase_num = self.builder.get_object("minlcase")
		self.excludelcases_field = self.builder.get_object("excludelcases")
		self.ucase_switch = self.builder.get_object("ucase_switch")
		self.minUcase_num = self.builder.get_object("minucase")
		self.excludeUcases_field = self.builder.get_object("excludeucases")
		self.digit_switch = self.builder.get_object("digit_switch")
		self.mindigits_num = self.builder.get_object("mindigits")
		self.excludedigits_field = self.builder.get_object("excludedigits")
		self.symbol_switch = self.builder.get_object("symbol_switch")
		self.minsymbol_num = self.builder.get_object("minsymbol")
		self.excludesymbol_field = self.builder.get_object("excludesymbols")
		
		# output values
		self.passwordfield = self.builder.get_object("passwordfield")
		self.strength_bar = self.builder.get_object("strength_bar")
		self.pw_strength_field = self.builder.get_object("pw_strength_field")
		self.pw_score_field = self.builder.get_object("pw_score_field")
		self.pw_guesses_field = self.builder.get_object("pw_guesses_field")
		self.pw_entropy_field = self.builder.get_object("pw_entropy_field")
		self.pw_crack_time_field = self.builder.get_object("pw_crack_time_field")
		self.pw_comment_field = self.builder.get_object("pw_comment_field")
		
		# Buttons
		self.reset_button = self.builder.get_object("reset_button")
		self.save_button = self.builder.get_object("save_button")
		self.generate_button = self.builder.get_object("generate_button")
		self.copy_button = self.builder.get_object("copy_button")
		self.quit_button = self.builder.get_object("quit_button")
		
		# Widget signals
		# self.method_combo.connect("changed", self.method_combo_changed)
		
		self.reset_button.connect("clicked", self.on_reset_button)
		self.save_button.connect("clicked", self.on_save_button)
		self.generate_button.connect("clicked", self.on_generate_button)
		self.passwordfield.connect("icon-press", self.on_showhide_button)
		self.copy_button.connect("clicked", self.on_copy_button)
		self.quit_button.connect("clicked", self.on_quit)
		self.passwordfield.connect("changed", self.show_pwstrength)
		
		# Menubar
		accel_group = Gtk.AccelGroup()
		self.window.add_accel_group(accel_group)
		menu = self.builder.get_object("main_menu")
		# Add "Shortcuts" option in drop-down menu
		item = Gtk.ImageMenuItem()
		item.set_image(Gtk.Image.new_from_icon_name("preferences-desktop-keyboard-shortcuts-symbolic", Gtk.IconSize.MENU))
		item.set_label(_("Keyboard Shortcuts"))
		item.connect("activate", self.open_keyboard_shortcuts)
		key, mod = Gtk.accelerator_parse("<Control>K")
		item.add_accelerator("activate", accel_group, key, mod, Gtk.AccelFlags.VISIBLE)
		menu.append(item)
		# Add "About" option in drop-down menu
		item = Gtk.ImageMenuItem()
		item.set_image(Gtk.Image.new_from_icon_name("help-about-symbolic", Gtk.IconSize.MENU))
		item.set_label(_("About"))
		item.connect("activate", self.open_about)
		key, mod = Gtk.accelerator_parse("<Control>F1")
		item.add_accelerator("activate", accel_group, key, mod, Gtk.AccelFlags.VISIBLE)
		menu.append(item)
		# Add "Quit" option in drop-down menu
		item = Gtk.ImageMenuItem(label=_("Quit"))
		image = Gtk.Image.new_from_icon_name("application-exit-symbolic", Gtk.IconSize.MENU)
		item.set_image(image)
		item.connect('activate', self.on_quit)
		key, mod = Gtk.accelerator_parse("<Control>Q")
		item.add_accelerator("activate", accel_group, key, mod, Gtk.AccelFlags.VISIBLE)
		key, mod = Gtk.accelerator_parse("<Control>W")
		item.add_accelerator("activate", accel_group, key, mod, Gtk.AccelFlags.VISIBLE)
		menu.append(item)
		# Show all drop-down menu options
		menu.show_all()
		
		self.load_conf()
		self.load_css(color="inherit")
		
	def load_conf(self):
		
		self.generator.load_config()
		
		self.method_combo.set_active(self.generator.gen_method)
		self.pwlengthfield.set_text(str(self.generator.pwlength))
		
		self.lcase_switch.set_active(self.generator.lowercase)
		self.minlcase_num.set_text(str(self.generator.lowercase_num))
		self.excludelcases_field.set_text(str(self.generator.excludeLowercase))
		if not self.generator.lowercase:
			self.minlcase_num.set_sensitive(False)
			self.excludelcases_field.set_sensitive(False)
		else:
			self.minlcase_num.set_sensitive(True)
			self.excludelcases_field.set_sensitive(True)
		
		self.ucase_switch.set_active(self.generator.uppercase)
		self.minUcase_num.set_text(str(self.generator.uppercase_num))
		self.excludeUcases_field.set_text(str(self.generator.excludeUppercase))
		if not self.generator.uppercase:
			self.minUcase_num.set_sensitive(False)
			self.excludeUcases_field.set_sensitive(False)
		else:
			self.minUcase_num.set_sensitive(True)
			self.excludeUcases_field.set_sensitive(True)
		
		self.digit_switch.set_active(self.generator.digit)
		self.mindigits_num.set_text(str(self.generator.digit_num))
		self.excludedigits_field.set_text(str(self.generator.excludeDigit))
		if not self.generator.digit:
			self.mindigits_num.set_sensitive(False)
			self.excludedigits_field.set_sensitive(False)
		else:
			self.mindigits_num.set_sensitive(True)
			self.excludedigits_field.set_sensitive(True)
			
		self.symbol_switch.set_active(self.generator.symbol)
		self.minsymbol_num.set_text(str(self.generator.symbol_num))
		self.excludesymbol_field.set_text(str(self.generator.excludeSymbol))
		if not self.generator.symbol:
			self.minsymbol_num.set_sensitive(False)
			self.excludesymbol_field.set_sensitive(False)
		else:
			self.minsymbol_num.set_sensitive(True)
			self.excludesymbol_field.set_sensitive(True)
	
	# def method_combo_changed(self, combo):
	# 	method_iter = combo.get_active_iter()
	# 	if method_iter is not None:
	# 		model = combo.get_model()
	# 		method = model[method_iter][0]
	# 		if method == methods[0]:
	# 			# Attach input fields of Default Method
	# 			self.default_method.set_visible(True)
	# 			self.dice_method.set_visible(False)
	# 			self.gen_pin.set_visible(False)
	# 		elif method == methods[1]:
	# 			# Attach input fields of Diceware Method
	# 			self.default_method.set_visible(False)
	# 			self.dice_method.set_visible(True)
	# 			self.gen_pin.set_visible(False)
	# 		elif method == methods[2]:
	# 			# Attach input fields of PIN generation
	# 			self.default_method.set_visible(False)
	# 			self.dice_method.set_visible(False)
	# 			self.gen_pin.set_visible(True)
	
	def open_keyboard_shortcuts(self, widget):
		gladefile = UI_PATH + "shortcuts.ui"
		builder = Gtk.Builder()
		builder.set_translation_domain(APP)
		builder.add_from_file(gladefile)
		window = builder.get_object("shortcuts-simplepwgen")
		window.set_title(_("Simple Password Generator"))
		window.show()
	
	def open_about(self, widget):
		dlg = Gtk.AboutDialog()
		dlg.set_transient_for(self.window)
		dlg.set_icon_name("simple-pwgen")
		dlg.set_logo_icon_name("simple-pwgen")
		dlg.set_title(_("About"))
		
		dlg.set_program_name(_("Simple Password Generator"))
		dlg.set_version(__version__)
		dlg.set_comments(_("Very simple Python3-based GUI application to generate secure and random password."))
		dlg.set_website("https://hsbasu.github.io/simple-pwgen")
		dlg.set_copyright("Copyright \xa9 2022 Himadri Sekhar Basu")
		dlg.set_authors(["Himadri Sekhar Basu <https://hsbasu.github.io>"])
		dlg.set_documenters(["Himadri Sekhar Basu <https://hsbasu.github.io>"])
		try:
			h = open('/usr/share/common-licenses/GPL', encoding="utf-8")
			s = h.readlines()
			gpl = ""
			for line in s:
				gpl += line
			h.close()
			dlg.set_license(gpl)
		except Exception as e:
			print (e)
		
		def close(w, res):
			if res == Gtk.ResponseType.CANCEL or res == Gtk.ResponseType.DELETE_EVENT:
				w.destroy()
		dlg.connect("response", close)
		dlg.show()
	
	def on_quit(self, widget):
		self.application.quit()
	
	def on_reset_button(self, widget):
		try:
			self.config.read(CONFIG_FILE)
			self.pwlengthfield.set_text(self.config["default"]['pwlength'])
			self.lcase_switch.set_active(int(self.config["default"]['lowercase']))
			self.minlcase_num.set_text(self.config["default"]['lowercase_num'])
			self.excludelcases_field.set_text(self.config["default"]['excludeLowercase'])
			self.ucase_switch.set_active(int(self.config["default"]['uppercase']))
			self.minUcase_num.set_text(self.config["default"]['uppercase_num'])
			self.excludeUcases_field.set_text(self.config["default"]['excludeUppercase'])
			self.digit_switch.set_active(int(self.config["default"]['digit']))
			self.mindigits_num.set_text(self.config["default"]['digit_num'])
			self.excludedigits_field.set_text(self.config["default"]['excludeDigit'])
			self.symbol_switch.set_active(int(self.config["default"]['symbol']))
			self.minsymbol_num.set_text(self.config["default"]['symbol_num'])
			self.excludesymbol_field.set_text(self.config["default"]['excludeSymbol'])
		except:
			self.pwlengthfield.set_text("8")
			self.lcase_switch.set_active(1)
			self.minlcase_num.set_text("1")
			self.excludelcases_field.set_text("")
			self.ucase_switch.set_active(1)
			self.minUcase_num.set_text("1")
			self.excludeUcases_field.set_text("")
			self.digit_switch.set_active(1)
			self.mindigits_num.set_text("1")
			self.excludedigits_field.set_text("")
			self.symbol_switch.set_active(0)
			self.minsymbol_num.set_text("0")
			self.excludesymbol_field.set_text("")
	
	def on_save_button(self, widget):
		"""Saves user configurations to config file.

		Saves user-defined configurations to config file.
		If the config file does not exist, it creates a new
		config file (~/.config/simple-pwgen/config.cfg)
		in user's home directory.
		"""
		if self.lcase_switch.get_active():
			lcase = 1
		else:
			lcase = 0
		if self.ucase_switch.get_active():
			ucase = 1
		else:
			ucase = 0
		if self.digit_switch.get_active():
			digit = 1
		else:
			digit = 0
		if self.symbol_switch.get_active():
			symbol = 1
		else:
			symbol = 0
		
		self.generator.config['user'] = {
			'generation-method': self.method_combo.get_active(),
			'pwlength': self.pwlengthfield.get_text(),
			'lowercase': lcase,
			'lowercase_num': self.minlcase_num.get_text(),
			'excludeLowercase': self.excludelcases_field.get_text(),
			'uppercase': ucase,
			'uppercase_num': self.minUcase_num.get_text(),
			'excludeUppercase': self.excludeUcases_field.get_text(),
			'digit': digit,
			'digit_num': self.mindigits_num.get_text(),
			'excludeDigit': self.excludedigits_field.get_text(),
			'symbol': symbol,
			'symbol_num': self.minsymbol_num.get_text(),
			'excludeSymbol': self.excludesymbol_field.get_text()
		}
		with open(CONFIG_FILE, 'w') as f:
				self.generator.config.write(f)
		
		self.load_conf()
	
	def on_generate_button(self, widget):
		[self.ferVar, self.encpasswd] = self.generator.GeneratePW()
		self.passwordfield.set_text(self.ferVar.decrypt(self.encpasswd).decode())
	
	def on_showhide_button(self, entry, icon_pos, event):
		if entry.get_visibility() == False:
			self.passwordfield.set_visibility(True)
			entry.set_icon_from_icon_name(icon_pos, 'view-conceal-symbolic')
		else:
			self.passwordfield.set_visibility(False)
			entry.set_icon_from_icon_name(icon_pos, 'view-reveal-symbolic')
	
	def on_copy_button(self, widget):
		self.clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
		self.clipboard.set_text(self.ferVar.decrypt(self.encpasswd).decode(), -1)
	
	def load_css(self, color: str):
		css_provider = Gtk.CssProvider()
		Priority = Gtk.STYLE_PROVIDER_PRIORITY_USER
		css = open(UI_PATH+'style.css', 'r')
		css_rawdata = css.read() % (color, color)
		# print(css_rawdata)
		css_data = bytes(css_rawdata, 'utf-8')
		css.close()
		css_provider.load_from_data(css_data)
		Gtk.StyleContext.add_provider_for_screen(Gdk.Screen.get_default(), css_provider, Priority)
		
	def show_pwstrength(self, widget):
		password = self.passwordfield.get_text()
		[pw_score, pw_comment, color] = self.generator.check_pwstrength(password)
		[pw_strength, pw_entropy, num_guess_crack, timerq_crack] = self.generator.check_pwentrpy(password)
		
		self.load_css(color)
		
		self.strength_bar.set_value(pw_score/10)
		self.pw_strength_field.set_text(pw_strength)
		self.pw_score_field.set_text(str(pw_score))
		self.pw_guesses_field.set_text(str(num_guess_crack))
		self.pw_entropy_field.set_text(str(pw_entropy))
		self.pw_crack_time_field.set_text(str(timerq_crack))
		self.pw_comment_field.set_text(pw_comment)
		
def run_SPGwindow():
	application = simple_pwgen("org.mamolinux.simple-pwgen", Gio.ApplicationFlags.FLAGS_NONE)
	application.run()
