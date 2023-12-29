import glob
import os
import pathlib
import subprocess

from setuptools import setup
from distutils.log import info
import distutils.command.install_data

for line in subprocess.check_output('dpkg-parsechangelog --format rfc822'.split(),
                         universal_newlines=True).splitlines():
    header, colon, value = line.lower().partition(':')
    if header == 'version':
        version = value.strip()
        break
else:
    raise RuntimeError('No version found in debian/changelog')

with open("src/SimplePwgen/VERSION", "w") as f:
    if '~' in version:
        version = version.split('~')[0]
    f.write("%s" % version)

gschema_dir_suffix = 'share/glib-2.0/schemas'

class install_data(distutils.command.install_data.install_data):
    def run(self):
        # Python 3 'super' call.
        super().run()
        
        # Compile '*.gschema.xml' to update or create 'gschemas.compiled'.
        info("compiling gsettings schemas")
        # Use 'self.install_dir' to build the path, so that it works
        # for both global and local '--user' installs.
        gschema_dir = os.path.join(self.install_dir, gschema_dir_suffix)
        self.spawn(["glib-compile-schemas", gschema_dir])

PO_FILES = 'po/simple-pwgen.po'

def create_mo_files():
	mo_files = []
	prefix = 'simple-pwgen'
	
	for po_path in glob.glob(str(pathlib.Path(prefix) / PO_FILES)):
		mo = pathlib.Path(po_path.replace('.po', '.mo'))
		
		subprocess.run(['msgfmt', '-o', str(mo), po_path], check=True)
		mo_files.append(str(mo.relative_to(prefix)))
	
	return mo_files

setup(data_files=[('share/applications', glob.glob("data/applications/*.desktop")),
			('share/icons/hicolor/scalable/apps', glob.glob("data/icons/*")),
			(gschema_dir_suffix, glob.glob("data/schema/*.xml")),
			('share/locale', create_mo_files())
			],
			cmdclass = {'install_data': install_data}
)
