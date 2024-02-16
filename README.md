# [Simple Password Generator](https://hsbasu.github.io/simple-pwgen)

<p align="center">
  	<img src="https://raw.githubusercontent.com/mamolinux/simple-pwgen/master/data/icons/simple-pwgen.svg?sanitize=true" height="128" alt="Logo">
</p>

<p align="center">
	<a href="#">
		<img src="https://img.shields.io/github/actions/workflow/status/mamolinux/simple-pwgen/ci.yml?branch=master&label=CI%20Build" alt="CI build">
	</a>
	<a href="#">
		<img src="https://img.shields.io/github/actions/workflow/status/mamolinux/simple-pwgen/codeql-analysis.yml?branch=master&label=CodeQL%20Build" alt="CodeQL build">
	</a>
	<a href="https://github.com/mamolinux/simple-pwgen/blob/master/LICENSE">
		<img src="https://img.shields.io/github/license/mamolinux/simple-pwgen?label=License" alt="License">
	</a>
  	<a href="#">
		<img src="https://img.shields.io/github/repo-size/mamolinux/simple-pwgen?label=Repo%20size" alt="GitHub repo size">
  	</a>
	<a href="https://github.com/mamolinux/simple-pwgen/issues" target="_blank">
		<img src="https://img.shields.io/github/issues/mamolinux/simple-pwgen?label=Issues" alt="Open Issues">
	</a>
	<a href="https://github.com/mamolinux/simple-pwgen/pulls" target="_blank">
		<img src="https://img.shields.io/github/issues-pr/mamolinux/simple-pwgen?label=PR" alt="Open PRs">
	</a>
  	<a href="https://github.com/mamolinux/simple-pwgen/releases/latest">
    	<img src="https://img.shields.io/github/v/release/mamolinux/simple-pwgen?label=Latest%20Stable%20Release" alt="GitHub release (latest by date)">
  	</a>
	<a href="#download-latest-version">
		<img src="https://img.shields.io/github/downloads/mamolinux/simple-pwgen/total?label=Downloads" alt="Downloads">
	</a>
	<a href="https://github.com/mamolinux/simple-pwgen/releases/download/1.1.2/simple-pwgen_1.1.2_all.deb">
		<img src="https://img.shields.io/github/downloads/mamolinux/simple-pwgen/1.1.1/simple-pwgen_1.1.2_all.deb?color=blue&label=Downloads%40Latest%20Binary" alt="GitHub release (latest by date and asset)">
	</a>
</p>

Very simple Python3-based GUI application to generate secure and random password.

## Contents
- [Download Latest Version](#download-latest-version)
	- [Stores/Ubuntu Private Archive](#storesubuntu-private-archive)
	- [Github Releases](#github-releases)
- [Features and Screenshots](#features-and-screenshots)
- [Dependencies](#dependencies)
	- [Debian/Ubuntu based systems](#debianubuntu-based-distro)
	- [Other Linux-based systems](#other-linux-based-distro)
- [Installation](#installation)
	- [1. Download and install binary files](#1-download-and-install-binary-files)
	- [2. Build and Install from source](#2-build-and-install-from-source)
		- [Debian/Ubuntu based systems](#debianubuntu-based-systems)
		- [Other Linux-based systems](#other-linux-based-systems)
- [User Manual](#user-manual)
- [Issue Tracking and Contributing](#issue-tracking-and-contributing)
	- [For Developers](#for-developers)
	- [Translation](#translation)
- [Contributors](#contributors)
	- [Authors](#author)

## Download Latest Version

### Stores/Ubuntu Private Archive
[![Get it from the Snap Store](https://snapcraft.io/static/images/badges/en/snap-store-black.svg)](https://snapcraft.io/simple-pwgen)

Add the Launchpad PPA
```$
sudo add-apt-repository ppa:mamolinux/gui-apps
sudo apt update
sudo apt install simple-pwgen
```

### Github Releases
If you want to generate passwords from terminal, download and install the CLI Backend. To use the graphical interface download both the backend and frontend. For installation, check [here](#installation).
<p align="center">
	<a href="https://github.com/mamolinux/simple-pwgen/zipball/master">Download Source (.zip)</a></br>
	<a href="https://github.com/mamolinux/simple-pwgen/tarball/master">Download Source (.tar.gz)</a></br>
	<a href="https://github.com/mamolinux/simple-pwgen/releases/download/1.1.1/python3-simple-pwgen_1.1.2_all.deb">Download Binary (Dependency for GUI) (.deb)</a></br>
	<a href="https://github.com/mamolinux/simple-pwgen/releases/download/1.1.1/simple-pwgen_1.1.2_all.deb">Download Binary for GUI (.deb)</a>
</p>

## Features and Screenshots

The main purpose of this application is to generate random and strong passwords. It lets an user choose:
1. Whether to include lowercase, uppercase, digit or punctuation individually or all of them.
2. Minimum number of each cases to be included in a password.
3. Whether to exclude some characters for each cases individually while generating a password.
4. By default, the generated password is hidden with `*` characters in the generated field to avoid shoulder-surfers. The user has the choice to view it using `Show/Hide` button.
5. Show password strength and comments on generated password to help users create strong passwords.

<p align="center">
	<img src="https://github.com/mamolinux/simple-pwgen/raw/gh-pages/screenshots/main-window-light.png" alt="Main Window (Light)">
	<img src="https://github.com/mamolinux/simple-pwgen/raw/gh-pages/screenshots/main-window-dark.png" alt="Main Window (Dark)">
</p>

**N.B.: This application does not save the generated password. So make sure you save it somewhere safe like using Firefox Lockwise.**

## Dependencies
```
gir1.2-gtk-3.0
python3
python3-configobj
python3-gi
python3-setproctitle
python3-tldextract
```
To use or test **Simple Password Generator**, you need these dependencies to be installed.

**Note**: If you are using `gdebi` to install **Simple Password Generator** from a `.deb` file, it will automatically install the dependencies and you can skip this step.

### Debian/Ubuntu based distro
To install dependencies on Debian/Ubuntu based systems, run:
```
sudo apt install gir1.2-gtk-3.0 python3 python3-configobj \
python3-gi python3-setproctitle python3-tldextract
```
**Note**: If you are using `gdebi` to install **Simple Password Generator** from a `.deb` file, it will automatically install the dependencies and you can skip this step.

### Other Linux-based distro
Remove `apt install` in the command given in [Debian/Ubuntu based distros](#debianubuntu-based-distro) and use the command for the package manager of the target system(eg. `yum install`, `dnf install`, `pacman -S` etc.)

**Note**: There might be cases where one or more dependencies might not be available for your system. But that is highly unlikely. In such situations, please [create an issue](#issue-tracking-and-contributing).

## Installation
There are two ways, this app can be installed on a Debian/Ubuntu based system. For other distros, install from [Snap Store](#download-latest-version).

### 1. Download and install binary files
Download the latest binary .deb files from [here](https://github.com/mamolinux/simple-pwgen/releases/latest).
First install the CLI Backend. Then install the GUI Frontend as
```$
sudo dpkg -i python3-simple-pwgen*.deb	# dependency to simple-pwgen*.deb
sudo dpkg -i simple-pwgen*.deb
```

### 2. Build and Install From Source
If you are having trouble installing the pre-built binary , build them from source.
#### Debian/Ubuntu based systems
There are two methods, this app can be installed/used on a Debian/Ubuntu based system. First, download and unzip the source package using:
```
wget https://github.com/mamolinux/simple-pwgen/archive/refs/heads/master.zip
unzip master.zip
cd simple-pwgen-master
```

1. **Option 1:** Manually copying necessary files to root (`/`). For that, follow the steps below:
	1. Install python package using `pip3`:
		```
		sudo pip3 install .
		```
		It will install all files under `/usr/local/`
	2. Compile `schemas` using:
		```
		sudo glib-compile-schemas /usr/local/share/glib-2.0/schemas
		```

2. **Option 2:** Build a debian package and install it. To build a debian package on your own:
	1. from the `simple-pwgen-master` run:
		```
		dpkg-buildpackage --no-sign
		```
		This will create a `simple-pwgen_*.deb` and `python3-simple-pwgen_*.deb` package at `../simple-pwgen-master`.
	
	2. Install the debian package using
		```
		sudo dpkg -i ../*simple-pwgen_*.deb
		sudo apt install -f
		```
After it is installed, run `simple-pwgen` from terminal or use the `simple-pwgen.desktop`.

#### Other Linux-based systems
1. Install the [dependencies](#other-linux-based-distro).
2. From instructions for [Debian/Ubuntu based systems](#debianubuntu-based-systems), follow **Option 1**.

## User Manual
Coming Soon or create a PR.

## Issue Tracking and Contributing
If you are interested to contribute and enrich the code, you are most welcome. You can do it by:
1. If you find a bug, to open a new issue with details: [Click Here](https://github.com/mamolinux/simple-pwgen/issues)

2. If you know how to fix a bug or want to add new feature/documentation to the existing package, please create a [Pull Request](https://github.com/mamolinux/simple-pwgen/compare).

### For Developers
1. Make desired modifications.
2. Manually install using [option 2](#2-build-and-install-from-source).
3. Test it by running `simple-pwgen -g` from terminal.

### Translation
All translations are done using using [Launchpad Tranlations](https://translations.launchpad.net/mamolinux). To help translate **Simple Password Generator** in your favourite language follow these steps:
1. Go to [translations page](https://translations.launchpad.net/mamolinux/trunk/+pots/simple-pwgen) on Launchpad.
2. Click on the language, you want to translate.
3. Translate strings.
4. Finally, click on **Save & Continue**.

## Contributors

### Author
[Himadri Sekhar Basu](https://github.com/hsbasu) is the author and current maintainer.

## Donations
I am a freelance programmer. So, If you like this app and would like to offer me a coffee ( &#9749; ) to motivate me further, you can do so via:

[![](https://liberapay.com/assets/widgets/donate.svg)](https://liberapay.com/hsbasu/donate)
[![](https://www.paypalobjects.com/webstatic/i/logo/rebrand/ppcom.svg)](https://paypal.me/hsbasu)
[![](https://hsbasu.github.io/styles/icons/logo/svg/upi-logo.svg)](https://hsbasu.github.io/images/upi-qr.jpg)
