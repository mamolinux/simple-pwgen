import argparse
import gettext
import locale
import sys

from SimplePwgen.common import APP, LOCALE_DIR, __version__, PasswordGenerator
from SimplePwgen.gui import run_SPGwindow


# i18n
locale.bindtextdomain(APP, LOCALE_DIR)
gettext.bindtextdomain(APP, LOCALE_DIR)
gettext.textdomain(APP)
_ = gettext.gettext

description = 'Very simple Python3-based GUI application to generate secure and random password.'

# Parse arguments
parser = argparse.ArgumentParser(prog=APP, description=description, conflict_handler='resolve')

parser.add_argument('-g', '--gui', action='store_true', dest='start_window', default=False, help=("Start GUI window"))
parser.add_argument('-V', '--version', action='store_true', dest='show_version', default=False, help=("Show version and exit"))

args = parser.parse_args()

if args.show_version:
    print("%s: version %s" % (APP, __version__))
    sys.exit(0)

def start_SPGGui():
	# initiaing app window
	run_SPGwindow()
	sys.exit(0)

def start_SPGCli():
	# generate password to stdout
	# using configurations from config file
	generator = PasswordGenerator()
	[ferVar, encpasswd] = generator.GeneratePW()
	[pw_score, pw_comment, color] = generator.check_pwstrength(ferVar.decrypt(encpasswd).decode())
	[pw_strength, pw_entropy, num_guess_crack, timerq_crack] = generator.check_pwentrpy(ferVar.decrypt(encpasswd).decode())
	
	print("")
	print("Generated Password: "+str(ferVar.decrypt(encpasswd).decode()))
	print("")
	print("Strength: "+str(pw_strength))
	print("Score: "+str(pw_score))
	print("Entropy: "+str(pw_entropy))
	print("Number of Guesses: "+str(num_guess_crack))
	print("Time required to crack: "+str(timerq_crack))
	print("Comment: "+str(pw_comment))
	print("")

if args.start_window:
	# start GUI from terminal
	start_SPGGui()

if __name__ == "__main__":
	if args.start_window:
		# start GUI from terminal
		start_SPGGui()
	else:
		start_SPGCli()
