#!/usr/bin/env python3

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
import configparser
import gettext
import locale
import os
import random
import string
import threading
from gi.repository import GObject


# Used as a decorator to run things in the background
def _async(func):
    def wrapper(*args, **kwargs):
        thread = threading.Thread(target=func, args=args, kwargs=kwargs)
        thread.daemon = True
        thread.start()
        return thread
    return wrapper

# Used as a decorator to run things in the main loop, from another thread
def idle(func):
    def wrapper(*args):
        GObject.idle_add(func, *args)
    return wrapper

# i18n
APP = 'simple-pwgen'
LOCALE_DIR = "/usr/share/locale"
locale.bindtextdomain(APP, LOCALE_DIR)
gettext.bindtextdomain(APP, LOCALE_DIR)
gettext.textdomain(APP)
_ = gettext.gettext

# Constants
CONFIG_DIR = os.path.expanduser('~/.config/simple-pwgen/')
CONFIG_FILE = os.path.join(CONFIG_DIR+'config.cfg')


# This is the backend.
# It contains utility functions generate
# passwords.
class PasswordGenerator():
    
    def __init__(self):
        # Always use cryptographically secure
        # SystemRandom functions
        self.TrueRand = random.SystemRandom()
        
        if os.path.exists(CONFIG_DIR):
            pass
        else:
            os.makedirs(CONFIG_DIR)
        
        self.config = configparser.ConfigParser()
        self.save_config()
        
    def load_config(self):
        """Loads configurations from config file.
        
        Tries to read and parse from config file.
        If the config file is missing or not readable,
        then it triggers default configurations.
        """
        
        self.config.read(CONFIG_FILE)
        try:
            self.pwlength = int(self.config["user"]['pwlength'])
            self.lowercase = int(self.config["user"]['lowercase'])
            self.lowercase_num = int(self.config["user"]['lowercase_num'])
            self.excludeLowercase = self.config["user"]['excludeLowercase']
            self.uppercase = int(self.config["user"]['uppercase'])
            self.uppercase_num = int(self.config["user"]['uppercase_num'])
            self.excludeUppercase = self.config["user"]['excludeUppercase']
            self.digit = int(self.config["user"]['digit'])
            self.digit_num = int(self.config["user"]['digit_num'])
            self.excludeDigit = self.config["user"]['excludeDigit']
            self.symbol = int(self.config["user"]['symbol'])
            self.symbol_num = int(self.config["user"]['symbol_num'])
            self.excludeSymbol = self.config["user"]['excludeSymbol']
        except:
            print('User configuration is missing or not readable. Trying default configuration')
            self.pwlength = int(self.config["default"]['pwlength'])
            self.lowercase = int(self.config["default"]['lowercase'])
            self.lowercase_num = int(self.config["default"]['lowercase_num'])
            self.excludeLowercase = self.config["default"]['excludeLowercase']
            self.uppercase = int(self.config["default"]['uppercase'])
            self.uppercase_num = int(self.config["default"]['uppercase_num'])
            self.excludeUppercase = self.config["default"]['excludeUppercase']
            self.digit = int(self.config["default"]['digit'])
            self.digit_num = int(self.config["default"]['digit_num'])
            self.excludeDigit = self.config["default"]['excludeDigit']
            self.symbol = int(self.config["default"]['symbol'])
            self.symbol_num = int(self.config["default"]['symbol_num'])
            self.excludeSymbol = self.config["default"]['excludeSymbol']
            
        self.check_config()
    
    def save_config(self):
        """Saves configurations to config file.

        Saves user-defined configurations to config file.
        If the config file does not exist, it creates a new config file
        (~/.config/simple-pwgen/config.cfg)
        in user's home directory.
        """
        if os.path.exists(CONFIG_FILE):
            pass
        else:
            self.config['default'] = {
                'pwlength': 8,
                'lowercase': 1,
                'lowercase_num': 1,
                'excludeLowercase': "",
                'uppercase': 1,
                'uppercase_num': 1,
                'excludeUppercase': "",
                'digit': 1,
                'digit_num': 1,
                'excludeDigit': "",
                'symbol': 0,
                'symbol_num': 0,
                'excludeSymbol': ""
            }
            with open(CONFIG_FILE, 'w') as f:
                self.config.write(f)
        
    def check_config(self):
        min_required_length = 0
        if self.lowercase == True:
            if self.lowercase_num == 0:
                print("Warning: minimum number of lowercases should be greater than 0")
            else:
                min_required_length += self.lowercase_num
            
        if self.uppercase == True:
            if self.uppercase_num == 0:
                print("Warning: minimum number of UPPERcases should be greater than 0")
            else:
                min_required_length += self.uppercase_num
            
        if self.digit == True:
            if self.digit_num == 0:
                print("Warning: minimum number of Digits should be greater than 0")
            else:
                min_required_length += self.digit_num
            
        if self.symbol == True:
            if self.symbol_num == 0:
                print("Warning: minimum number of Symbols should be greater than 0")
            else:
                min_required_length += self.symbol_num
        
        if min_required_length > self.pwlength:
            print("Error: Minimum required length exceeded given length!")
            
            return 1
        
    def includeonlyChars(self):
        Lowercaselist = []
        Uppercaselist = []
        Digitslist = []
        Symbollist = []
        charslist = {}
        
        if self.lowercase == True:
            if self.lowercase_num >0:
                Lowercaselist = list(string.ascii_lowercase)
                excludelist = list(self.excludeLowercase)
                for i in excludelist:
                    del(Lowercaselist[Lowercaselist.index(i)])
                
        charslist["Lowercases"] = Lowercaselist
        # print(Lowercaselist)
        
        if self.uppercase == True:
            if self.uppercase_num >0:
                Uppercaselist = list(string.ascii_uppercase)
                excludelist = list(self.excludeUppercase)
                for i in excludelist:
                    del(Uppercaselist[Uppercaselist.index(i)])
                
        charslist["Uppercases"] = Uppercaselist
        # print(Uppercaselist)
        
        if self.digit == True:
            if self.digit_num >0:
                Digitslist = list(string.digits)
                excludelist = list(self.excludeDigit)
                for i in excludelist:
                    del(Digitslist[Digitslist.index(i)])
                
        charslist["Digits"] = Digitslist
        # print(Digitslist)
        
        if self.symbol == True:
            if self.symbol_num >0:
                Symbollist = list(string.punctuation)
                excludelist = list(self.excludeSymbol)
                for i in excludelist:
                    del(Symbollist[Symbollist.index(i)])
                    
        charslist["Symbols"] = Symbollist
        # print(Symbollist)
        
        return charslist
    
    def includeCases(self, pwlength):
        
        lowercase_location = []
        uppercase_location = []
        digit_location = []
        symbol_location = []
        all_cases = []
        include_num_cases = {}
        
        if self.lowercase == True:
            i = 0
            while True:
                if i == self.lowercase_num:
                    break
                x = self.TrueRand.randint(0, pwlength-1)
                if x not in all_cases:
                    all_cases += [x]
                    lowercase_location += [x]  # random location of uppercase
                    i += 1
        
        include_num_cases["Lowercases"] = lowercase_location
        # print(lowercase_location)
        
        if self.uppercase == True:
            i = 0
            while True:
                if i == self.uppercase_num:
                    break
                x = self.TrueRand.randint(0, pwlength-1)
                if x not in all_cases:
                    all_cases += [x]
                    uppercase_location += [x]  # random location of lowercase
                    i += 1
        
        include_num_cases["Uppercases"] = uppercase_location
        # print(uppercase_location)
        
        if self.digit == True:
            i = 0
            while True:
                if i == self.digit_num:
                    break
                x = self.TrueRand.randint(0, pwlength-1)
                if x not in all_cases:
                    all_cases += [x]
                    digit_location += [x]  # random location of digits
                    i += 1
        
        include_num_cases["Digits"] = digit_location
        # print(digit_location)
        
        if self.symbol == True:
            i = 0
            while True:
                if i == self.symbol_num:
                    break
                x = self.TrueRand.randint(0, pwlength-1)
                if x not in all_cases:
                    all_cases += [x]
                    symbol_location += [x]  # random location of symbols
                    i += 1
        
        include_num_cases["Symbols"] = symbol_location
        # print(symbol_location)
        
        return include_num_cases
    
    def GeneratePW(self):
        
        # load, check and save user configuration if available
        # use default configuration
        self.load_config()
        
        includechars = PasswordGenerator.includeonlyChars(self)
        includecases = PasswordGenerator.includeCases(self, self.pwlength)
        
        pool = "".join(includechars["Lowercases"] + includechars["Uppercases"] + includechars["Digits"] + includechars["Symbols"])  # don't include symbol
        
        password = ''  # empty string for password
        
        for i in range(self.pwlength):
            if i in includecases["Lowercases"]:  # this is to ensure there is at least one uppercase
                password += self.TrueRand.choice(includechars["Lowercases"])
            
            elif i in includecases["Uppercases"]:   # this is to ensure there is at least one uppercase
                password += self.TrueRand.choice(includechars["Uppercases"])
            
            elif i in includecases["Digits"]:  # this is to ensure there is at least one uppercase
                password += self.TrueRand.choice(includechars["Digits"])
            
            elif i in includecases["Symbols"]:  # this is to ensure there is at least one symbol
                password += self.TrueRand.choice(includechars["Symbols"])
            
            else:  # adds a random character from pool
                password += self.TrueRand.choice(pool)
            
        return password  # returns the string
    
if __name__ == "__main__":
    PasswordGenerator()
    passw = PasswordGenerator().GeneratePW()
    print(passw)
    