#!/usr/bin/python3

# Copyright (C) 2021 Himadri Sekhar Basu <hsb10@iitbbs.ac.in>
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

from common import CONFIG_FILE, PasswordGenerator

setproctitle.setproctitle("simple-pwgen")

# i18n
APP = 'simple-pwgen'
LOCALE_DIR = "/usr/share/locale"
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
		self.settings = Gio.Settings(schema_id="org.x.simple-pwgen")
		self.generator = PasswordGenerator()
		self.icon_theme = Gtk.IconTheme.get_default()
		
		# Set the Glade file
		gladefile = "/usr/share/simple-pwgen/simple-pwgen.ui"
		self.builder = Gtk.Builder()
		self.builder.add_from_file(gladefile)
		self.window = self.builder.get_object("MainWindow")
		self.window.set_title(_("Simple Password Generator"))
		
		# Create variables to quickly access dynamic widgets
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
		
		# Buttons
		self.reset_button = self.builder.get_object("reset_button")
		self.save_button = self.builder.get_object("save_button")
		self.generate_button = self.builder.get_object("generate_button")
		self.showhide_button = self.builder.get_object("showhide_button")
		self.copy_button = self.builder.get_object("copy_button")
		self.quit_button = self.builder.get_object("quit_button")
		
		# Widget signals
		self.reset_button.connect("clicked", self.on_reset_button)
		self.save_button.connect("clicked", self.on_save_button)
		self.generate_button.connect("clicked", self.on_generate_button)
		self.showhide_button.connect("clicked", self.on_showhide_button)
		self.copy_button.connect("clicked", self.on_copy_button)
		self.quit_button.connect("clicked", self.on_quit)
		
		# Menubar
		accel_group = Gtk.AccelGroup()
		self.window.add_accel_group(accel_group)
		menu = self.builder.get_object("main_menu")
		# Add "About" option in drop-down menu
		item = Gtk.ImageMenuItem()
		item.set_image(Gtk.Image.new_from_icon_name("help-about-symbolic", Gtk.IconSize.MENU))
		item.set_label(_("About"))
		item.connect("activate", self.open_about)
		key, mod = Gtk.accelerator_parse("F1")
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
		
	def load_conf(self):
		
		self.generator.load_config()
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
			
	def open_about(self, widget):
		dlg = Gtk.AboutDialog()
		dlg.set_transient_for(self.window)
		dlg.set_icon_name("simple-pwgen")
		dlg.set_logo_icon_name("simple-pwgen")
		dlg.set_title(_("About"))
		
		dlg.set_program_name(_("Simple Password Generator"))
		dlg.set_version("__DEB_VERSION__")
		dlg.set_comments(_("Very simple Python3-based GUI application to generate secure and random password."))
		dlg.set_website("https://hsbasu.github.io/simple-pwgen")
		dlg.set_copyright("Copyright \xa9 2021 Himadri Sekhar Basu")
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
		self.password = self.generator.GeneratePW()
		self.passwordfield.set_text(self.password)
	
	def on_showhide_button(self, widget):
		if self.passwordfield.get_visibility() == False:
			self.passwordfield.set_visibility(True)
			self.showhide_button.set_label("Hide")
		else:
			self.passwordfield.set_visibility(False)
			self.showhide_button.set_label("Show")
	
	def on_copy_button(self, widget):
		self.clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
		self.clipboard.set_text(self.password, -1)
		

if __name__ == "__main__":
	application = simple_pwgen("org.x.simple-pwgen", Gio.ApplicationFlags.FLAGS_NONE)
	application.run()
	