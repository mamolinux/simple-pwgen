<h1 align="center">Simple Password Generator</h1>
<p align="center">
    <img src="https://github.com/hsbasu/simple-pwgen/blob/master/usr/share/icons/hicolor/scalable/apps/simple-pwgen.svg?sanitize=true"
        height="130">
</p>

![GitHub Workflow Status (master)](https://img.shields.io/github/workflow/status/hsbasu/simple-pwgen/CI/master?label=CI%20Build)
![GitHub Workflow Status (master)](https://img.shields.io/github/workflow/status/hsbasu/simple-pwgen/CodeQL/master?label=CodeQL%20Build)
[![License](https://img.shields.io/github/license/hsbasu/simple-pwgen?label=License)](https://github.com/hsbasu/simple-pwgen/blob/master/LICENSE)

![GitHub repo size](https://img.shields.io/github/repo-size/hsbasu/simple-pwgen?label=Repo%20size)
[![GitHub release (latest by date)](https://img.shields.io/github/v/release/hsbasu/simple-pwgen?label=Latest%20Stable%20Release)](https://github.com/hsbasu/simple-pwgen/releases/latest)

![Downloads](https://img.shields.io/github/downloads/hsbasu/simple-pwgen/total?label=Downloads&style=flat-square)
[![GitHub release (latest by date and asset)](https://img.shields.io/github/downloads/hsbasu/simple-pwgen/1.0.4/simple-pwgen_1.0.4_all.deb?color=blue&label=Downloads%40Latest)](https://github.com/hsbasu/simple-pwgen/releases/download/1.0.4/simple-pwgen_1.0.4_all.deb)

Very simple Python3-based GUI application to generate secure and random password.

### Contents

  - [Features](#features)
  - [Dependencies](#dependencies)
  - [Installation](#how-to-build-and-install)
    - [Debian/Ubuntu based systems](#debianubuntu-based-systems)
    - [Other Linux-based systems](#other-linux-based-systems)

### Features

It lets an user choose:
1. Whether to include lowercase, uppercase, digit or punctuation individually or all of them.
2. Minimum number of each cases to be included in a password.
3. Whether to exclude some characters for each cases individually while generating a password.

### Dependencies
```
python3
python3-configobj
python3-gi
python3-setproctitle
python3-tldextract
```

### How to Build and install
#### Debian/Ubuntu based systems
1. Install dependencies:
	```
	sudo apt install python3 python3-configobj python3-gi \
    python3-setproctitle python3-tldextract
    ```

2. There are two methods, this app can be installed/used:
	1. **Option 1:** Manually copying necessary files to root (`/`). For that, follow the steps below:
		1. [**Optional**] To make translations/locales in languages other than **English**, run:
			```
			make
			```
			from the `/path/to/repo` in a terminal. It will create the translations/locales in `usr/share/locale`.
        
		2. Copy the contents of `usr/` to `/usr/`:
			```
			sudo cp -R usr /
			```
		3. Compile `schemas` using:
			```
			sudo glib-compile-schemas /usr/share/glib-2.0/schemas
			```
		4. Run `simple-pwgen` from terminal or use the `simple-pwgen.desktop`.
    
	2. **Option 2:** Build a debian package and install it. To build a debian package on your own:
        1. from the `/path/to/repo` run:
			```
			dpkg-buildpackage --no-sign
			```
		
		This will create a `webapp-manager_*.deb` package at `../path/to/repo`.
        2. Install the debian package using
	        ```
	        sudo dpkg -i *.deb
	        sudo apt install -f
	        ```

#### Other Linux-based systems
From instructions for [Debian/Ubuntu based systems](#debianubuntu-based-systems), follow:
1. **Step _1_** replacing `apt install` with the *package manager* of target system(eg. yum, dnf, pacman etc.).
2. **Option 1** from **Step _2_**

### Author
[Himadri Sekhar Basu](https://github.com/hsbasu)
