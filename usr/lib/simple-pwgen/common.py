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
import math
import os
import random
import threading
from gi.repository import GObject
from string import ascii_uppercase, ascii_lowercase, digits, punctuation


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
# It contains utility functions to generate
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
        self.pool = ascii_lowercase+ascii_uppercase+digits+punctuation
        
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
                Lowercaselist = list(ascii_lowercase)
                excludelist = list(self.excludeLowercase)
                for i in excludelist:
                    del(Lowercaselist[Lowercaselist.index(i)])
                
        charslist["Lowercases"] = Lowercaselist
        # print(Lowercaselist)
        
        if self.uppercase == True:
            if self.uppercase_num >0:
                Uppercaselist = list(ascii_uppercase)
                excludelist = list(self.excludeUppercase)
                for i in excludelist:
                    del(Uppercaselist[Uppercaselist.index(i)])
                
        charslist["Uppercases"] = Uppercaselist
        # print(Uppercaselist)
        
        if self.digit == True:
            if self.digit_num >0:
                Digitslist = list(digits)
                excludelist = list(self.excludeDigit)
                for i in excludelist:
                    del(Digitslist[Digitslist.index(i)])
                
        charslist["Digits"] = Digitslist
        # print(Digitslist)
        
        if self.symbol == True:
            if self.symbol_num >0:
                Symbollist = list(punctuation)
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
        
        self.pool = "".join(includechars["Lowercases"] + includechars["Uppercases"] + includechars["Digits"] + includechars["Symbols"])
        
        password = ''  # empty string for password
        
        for i in range(self.pwlength):
            # this is to ensure there is minimum number of lowercases desired by user
            if i in includecases["Lowercases"]:
                password += self.TrueRand.choice(includechars["Lowercases"])
            
            # this is to ensure there is minimum number of uppercases desired by user
            elif i in includecases["Uppercases"]:
                password += self.TrueRand.choice(includechars["Uppercases"])
            
            # this is to ensure there is minimum number of digits desired by user
            elif i in includecases["Digits"]:
                password += self.TrueRand.choice(includechars["Digits"])
            
            # this is to ensure there is minimum number of symbols/characters desired by user
            elif i in includecases["Symbols"]:
                password += self.TrueRand.choice(includechars["Symbols"])
            
            else:  # adds a random character from pool
                password += self.TrueRand.choice(self.pool)
        
        # shuffle the password again
        password = list(password)
        random.shuffle(password)
        password = ''.join(password)
        
        return password  # returns the password string
    
    def check_pwstrength(passwd):
        score = 0
        comment = _("Bad Password.")
        if len(passwd) <6:
            comment += _(" Password is too short!")
            score += 0
        elif len(passwd) <8:
            score += 20
        elif len(passwd) <10:
            score += 40
        else:
            score += 60
        
        if any(c in ascii_lowercase for c in passwd):
            # check for lower case in password
            score += 10
            if passwd == passwd.lower():
                # check if password is only lower case
                comment += _(" Only lower case used.")
                score -= 5
        else:
            comment += _(" No lower case used.")
        
        if any(c in ascii_uppercase for c in passwd):
            # check for upper case in password
            score += 10
            if passwd == passwd.upper():
                # check if password is only upper case
                comment += _(" Only UPPER case used.")
                score -= 5
        else:
            comment += _(" No UPPER case used.")
        
        if any(c in punctuation for c in passwd):
            score += 10
        else:
            comment += _(" No special character used.")
        
        if any(c in digits for c in passwd):
            # check for digits in password
            score += 10
            if passwd.isdigit():
                # check if password is only digit
                comment += _(" Only digits used. Is It a PIN?")
                score -= 5
        else:
            comment += _(" No digit used.")
        
        if (score >90):
            comment = _("Looks like you know how to generate a Good Password. All types of characters are used.")
        
        return [score, comment]
        
    def check_pwentrpy(self, passwd):
        strength_comment = ["Very Weak", "Weak", "Reasonable", "Fairly Strong", "Strong", "Very Strong", "Super Strong"]
        length = len(passwd)
        pool_size = len(self.pool)
        entropy = length*math.log2(pool_size)
        strength = strength_comment[0]
        
        if entropy < 28:
            # Might keep out family members
            strength = strength_comment[0]
        elif (entropy >= 28 and entropy < 36):
            # Should keep out most people, often good for desktop login passwords
            strength = strength_comment[1]
        elif (entropy >= 36 and entropy < 64):
            # Fairly secure passwords for network and company passwords
            strength = strength_comment[2]
        elif (entropy >= 64 and entropy < 80):
            # Suitable for guarding financial information
            strength = strength_comment[3]
        elif (entropy >= 80 and entropy < 100):
            # Suitable for guarding financial information
            strength = strength_comment[4]
        elif (entropy >= 100 and entropy < 128):
            # Suitable for guarding financial information
            strength = strength_comment[5]
        elif entropy >= 128:
            # Suitable for guarding financial information
            strength = strength_comment[6]
        
        num_guess = round(pow(2, (entropy-1)))
        timerq_sc = num_guess/1e15   # Time taken by a modern supecomputer to guess the password with 50% probability
        if (num_guess > 1e8):
            # in case number of guess is greater than 1e8, use scientific notation
            num_guess = "{:e}".format(num_guess)
        
        minute, secnd = divmod(timerq_sc, 60)
        hour, minute = divmod(minute, 60)
        day, hour = divmod(hour, 24)
        month, day = divmod(day, 30)
        year, month = divmod(month, 12)
        timerq = _("%s years %s months %s days %s hours %s minutes %s seconds") % (year, month, day, hour, minute, secnd)
        
        return [strength, entropy, num_guess, timerq]

if __name__ == "__main__":
    generator = PasswordGenerator()
    passwd = generator.GeneratePW()
    [pw_score, pw_comment] = generator.check_pwstrength(passwd)
    [pw_strength, pw_entropy, num_guess_crack, timerq_crack] = generator.check_pwentrpy(passwd)
    
    print("Generated Password: "+str(passwd))
    print("")
    print("Strength: "+str(pw_strength))
    print("Score: "+str(pw_score))
    print("Entropy: "+str(pw_entropy))
    print("Number of Guesses: "+str(num_guess_crack))
    print("Time required to crack: "+str(timerq_crack))
    print("Comment: "+str(pw_comment))
    print("")
    