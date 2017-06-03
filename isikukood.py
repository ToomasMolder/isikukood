# Find, how many similarities in ID (isikukood) is available when using check digit calculation algorithm
#    according to Estonian ID https://et.wikipedia.org/wiki/Isikukood
##    
##   TODO: and according to Luhn algorithm https://en.wikipedia.org/wiki/Luhn_algorithm
# 
# Author: Toomas Mölder <toomas.molder@gmail.com>, +372 5522000
# Last modified: 2017-06-03
#
# NB! Might be buggy and crappy, written for own purposes
# TODO: better logic of input from user

# Imports required for different activities within main program and definitions
import os
import sys
import time
import copy
# import sys
import inspect
# Let's do also some easygui :)
# Source: http://easygui.sourceforge.net/
# Please have easygui.py in the current directory!
# You can get copy from https://courses.cs.ut.ee/2017/eprogalused/spring/uploads/Main/easygui.py
from easygui import *
import time
import json
import random

start_time = ""

# Debug levels defined in MAIN:
# 0 = Errors only
# 1 = echo user input (useful when output is redirected into file, Linux)
# 2 = Warnings as well
# 3 = Info
# 4 = GUI
# 5 = ... (for future use)
#
os.environ['DEBUG'] = '1'

def message(msg):
    debug = int(os.environ['DEBUG'])

    if debug == 4:
        # Do it with easygui
        title = msg.split(':')[0]
        tmp = ''.join(msg.split(':')[1:]).strip()
        msgbox(tmp, title, ok_button="OK")
    elif debug == 1:
        print(msg)
    else:
        # NB! msg MUST include keywords 'Info' or 'Warning' or 'Error' to be printed out
        if (("Info" in msg and debug == 3) or
            ("Warning" in msg and debug >= 2) or
            ("Error" in msg and debug >= 1) or
            ("Result" in msg)):
            print(msg)
            # sys.stdout.flush()
    
    return

# Source: http://stackoverflow.com/questions/23294658/asking-the-user-for-input-until-they-give-a-valid-response
# Added debugging
def sanitised_input(prompt, type_=None, min_=None, max_=None, range_=None):
    debug = int(os.environ['DEBUG'])
    
    if min_ is not None and max_ is not None and max_ < min_:
        raise ValueError("min_ must be less than or equal to max_.")
    
    while True:
        ui = input(prompt)
        
        if debug == 1:
            print(str(ui))

        if type_ is not None:
            try:
                ui = type_(ui)
            except ValueError:
                print("Input type must be {0}.".format(type_.__name__))
                continue
        
        if max_ is not None and ui > max_:
            print("Input must be less than or equal to {0}.".format(max_))
        elif min_ is not None and ui < min_:
            print("Input must be greater than or equal to {0}.".format(min_))
        elif range_ is not None and ui not in range_:
            if isinstance(range_, range):
                template = "Input must be between {0.start} and {0.stop}."
                print(template.format(range_))
            else:
                template = "Input must be {0}."
                if len(range_) == 1:
                    print(template.format(*range_))
                else:
                    print(template.format(" or ".join((", ".join(map(str,
                                                                     range_[:-1])),
                                                       str(range_[-1])))))
        else:
            return ui

# Source: http://stackoverflow.com/questions/3041986/apt-command-line-interface-like-yes-no-input
# Added debugging
def query_yes_no(question, default="yes"):
    debug = int(os.environ['DEBUG'])
    
    """Ask a yes/no question via input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is True for "yes" or False for "no".
    """
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        
        if debug == 1:
            print(str(choice))
        
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")

# Source: http://stackoverflow.com/questions/1823058/how-to-print-number-with-commas-as-thousands-separators
def group(number):
    s = '%d' % number
    groups = []
    
    while s and s[-1].isdigit():
        groups.append(s[-3:])
        s = s[:-3]
    
    return s + '.'.join(reversed(groups))

# Ask input from user to justify range (min, max)
# Return tuple of new (start, end)
def ask_start_end(about, min, max):
    debug = int(os.environ['DEBUG'])
    msg = "Starting " + about.upper() + " of ID (" + str(min) + "-" + str(max) + "): "
    
    if debug == 4:
        start = integerbox(msg, "Input", lowerbound = min, upperbound = max)
    else:
        start = sanitised_input(msg, int, min, max)

    if start == "" or start == None:
        return(None, None)
    
    # Use already given by user START here instead of function input MIN
    msg = "Ending " + about.upper() + " of ID (" + str(start) + "-" + str(max) + "): "
    
    if debug == 4:
        end = integerbox(msg, "Input", lowerbound = start, upperbound = max)
    else:
        end = sanitised_input(msg, int, start, max)

    if end == "" or end == None:
        return(start, None)
    
    # Probably not needed, keep it just for any case
    if start > end:
        # Swap variables
        start, end = end, start

    return (start, end)

# Calculate and return check digit of ID according to Estonian-specific rules
# See also: https://et.wikipedia.org/wiki/Isikukood
def calc_id_check(id):
    debug = int(os.environ['DEBUG'])
    weight1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 1]
    weight2 = [3, 4, 5, 6, 7, 8, 9, 1, 2, 3]
    check = 0
    id_as_list = list(id)
    
    # Only first 10 positions used
    for i in range(10):
        check += int(id[i]) * weight1[i]
    check = check % 11
    
    if check == 10:
        check = 0
        # Only first 10 positions used
        for i in range(10):
            check += int(id[i]) * weight2[i]
        check = check % 11
        
        if check == 10:
            check = 0
    
    if debug == 3:
        message("(" + inspect.stack()[0][3] + ") " + "Info: " + "ID '" + id + "' check = " + str(check))
    
    return check

# Check length of ID, return True/False
def is_id_len(id):
    debug = int(os.environ['DEBUG'])
    length = 11
    
    if debug == 3:
        message("(" + inspect.stack()[0][3] + ") " + "Info: " + "ID '" + id + "'. Length = " + str(len(id)))
    
    if len(id) == length:
        return True
    else:
        if debug == 2 or debug == 3:
            message("(" + inspect.stack()[0][3] + ") " + "Warning: " + "ID '" + id + "'. Length = " + str(len(id)) + " is not " + str(length))
        return False

# Check that ID includes only digits, return True/False
def is_id_digit(id):
    debug = int(os.environ['DEBUG'])
    
    if debug == 3:
        message("(" + inspect.stack()[0][3] + ") " + "Info: " + "ID '" + id + "'. Digit = " + str(id.isdigit()))
    
    if id.isdigit():
        return True
    else:
        if debug == 2 or debug == 3:
            message("(" + inspect.stack()[0][3] + ") " + "Warning: " + "ID '" + id + "'. Digit = " + str(id.isdigit()))
        return False

# Check that first digit of ID (century) is within given range min_century and max_century, return True/False
def is_id_century(id):
    debug = int(os.environ['DEBUG'])
    # Currently we do look only persons born between 1900-2099
    # Born 1900-1999 male century is 3, female century is 4
    # Born 2000-2099 male century is  5, female century is 6
    min_century = 3
    max_century = 6
    
    if debug == 3:
        message("(" + inspect.stack()[0][3] + ") " + "Info: " + "ID '" + id + "'. Century = " + str(id[0]))
    
    if (int(id[0]) >= min_century and int(id[0]) <= max_century):
        return True
    else:
        if debug == 2 or debug == 3:
            message("(" + inspect.stack()[0][3] + ") " + "Warning: " + "ID '" + id + "'. Century = " + str(id[0]))
        return False

# Check that date is valid date, return True/False
# Source: http://stackoverflow.com/questions/9987818/in-python-how-to-check-if-a-date-is-valid
def is_date_valid(year, month, day):
    this_date = '%d/%d/%d' % (month, day, year)
    
    try:
        time.strptime(this_date, '%m/%d/%Y')
    except ValueError:
        return False
    else:
        return True

# Check that date within Estonian ID (positions 1-7) is valid date, return True/False
# See also: https://et.wikipedia.org/wiki/Isikukood
def is_id_date(id):
    debug = int(os.environ['DEBUG'])
    century = int(id[0])
    yy = int(id[1:3])
    yyyy = (17 + (century + 1) // 2) * 100 + yy
    mm = int(id[3:5])
    dd = int(id[5:7])
    
    if debug == 3:
        message("(" + inspect.stack()[0][3] + ") " + "Info: " + "Date Century = " + str(century) +
                " Year (yy) = " + str(yy) +
                " Year (yyyy) = " + str(yyyy) +
                " Month = " + str(mm) +
                " Day = " + str(dd))
    
    if is_date_valid (yyyy, mm, dd):
        return True
    else:
        if debug == 2 or debug == 3:
            message("(" + inspect.stack()[0][3] + ") " + "Warning: " + "Date " + str(yyyy) + "-" + str(mm) + "-" + str(dd) + " is not valid.")
        return False

# Check that check digit in 11th position of Estonian ID is valid, return True/False
# Use def calc_id_check
def is_id_check(id):
    debug = int(os.environ['DEBUG'])
    check = calc_id_check(id[:10])
    
    if debug == 3:
        message("(" + inspect.stack()[0][3] + ") " + "Info: " + "ID = '" + str(id) + "'. Given check digit = " + str(id[10]) + " Calculated check digit = " + str(check))
    
    if int(id[10]) == check:
        return True
    else:
        if debug == 2 or debug == 3:
            message("(" + inspect.stack()[0][3] + ") " + "Warning: " + "ID = '" + str(id) + "'. Given check digit = " + str(id[10]) + " Calculated check digit = " + str(check))
        return False
    # return int(id[10]) == calc_id_check(id[:10])

# Full check of Estonian ID validity
def is_id_valid_full(id):
    
    return (is_id_len(id) and
            is_id_digit(id) and
            is_id_century(id) and
            is_id_date(id) and
            is_id_check(id))

# Basic check of Estonian ID validity, we know, that already, that it has length of 11 and digits only 
def is_id_valid_basic(id):
    
    return (is_id_century(id) and
            is_id_date(id) and
            is_id_check(id))

# Source: https://en.wikipedia.org/wiki/Luhn_algorithm
def digits_of(number):
    
    return [int(i) for i in str(number)]

# Calculate check digit according to Luhn algorithm
# See also, source from https://en.wikipedia.org/wiki/Luhn_algorithm
def luhn_checksum(card_number):
    digits = digits_of(card_number)
    odd_digits = digits[-1::-2]
    even_digits = digits[-2::-2]
    total = sum(odd_digits)
    
    for digit in even_digits:
        total += sum(digits_of(2 * digit))
    
    return total % 10

# Source: https://en.wikipedia.org/wiki/Luhn_algorithm
def is_luhn_valid(card_number):
    
    return luhn_checksum(card_number) == 0

# Source: https://en.wikipedia.org/wiki/Luhn_algorithm
def calculate_luhn(partial_card_number): 
    check_digit = luhn_checksum(int(partial_card_number) * 10)   # Append a zero check digit to the partial number and calculate checksum
    
    return check_digit if check_digit == 0 else 10 - check_digit # If the (sum mod 10) == 0, then the check digit is 0
                                                                 # Else, the check digit = 10 - (sum mod 10)

# Find similar IDs in conditions that check digit remains
# Use algorithm = "eid" (calc_id_check) or algorithm = "luhn" (luhn_checksum)
# Return list of similarites
def find_similar_one(id):
    debug = int(os.environ['DEBUG'])
    algorithm = "eid"
    
    # Use 'keyboards' to find 'neighbour' keypresses
    # Left from '1' is '1' (key '1' is leftmost); right from '9' is '0', left from '0' is '9' and right from '0' is still '0' ('0' is rigthmost)
    keyboard = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]
    keyboard_shift_left = [1, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    keyboard_shift_right = [2, 3, 4, 5, 6, 7, 8, 9, 0, 0]
    
    similarities = []
    # Consider ID as list
    id_as_list = list(id)
    
    # Cycle over all digits in ID, but not the last digit (check digit)
    # Limit manually range (0, 1) or other similar to find possible errors only in few digits, probably makes overall process also much faster ...
    for i in range(0, len(id_as_list) - 1):
        # Do deepcopy of id_as_listnot to mess with pointers
        tmp = copy.deepcopy(id_as_list)
                
        #
        # Method: smaller
        #
        # if int(id_as_list[i]) > 0:
        # Value of ID digit id_as_list[i] must be NOT 1, this is leftmost numeric on keyboard
        if not int(id_as_list[i]) == 1:
            tmp[i] = str(keyboard_shift_left[keyboard.index(int(id_as_list[i]))])
        
            # if debug == 3:
                # message("(" + inspect.stack()[0][3] + ") " + "Info: " + "Method: smaller " + "id_as_list[" + str(i) + "] = " + id_as_list[i] + " / tmp[" + str(i) + "] = " + tmp[i])
            
            # Join list back as string
            smaller = ''.join(tmp)
            
            if is_id_valid_basic(smaller):
                similarities.append(smaller)

        #
        # Method: bigger
        #
        # if int(id_as_list[i]) < 9:
        # Value of ID digit id_as_list[i] must be NOT 0, this is rightmost numeric on keyboard
        if not int(id_as_list[i]) == 0:
            tmp[i] = str(keyboard_shift_right[keyboard.index(int(id_as_list[i]))])
            # if debug == 3:
                # message("(" + inspect.stack()[0][3] + ") " + "Info: " + "Method: bigger " + "id_as_list[" + str(i) + "] = " + id_as_list[i] + " / tmp[" + str(i) + "] = " + tmp[i])
            
            bigger = ''.join(tmp)
            
            if is_id_valid_basic(bigger):
                similarities.append(bigger)
        
        # Restore tmp[i]
        tmp[i] = str(id_as_list[i])
        
        #
        # Method: swap
        #
        # No reason to swap equal digits
        if not tmp[i] == tmp[i+1]:
            tmp[i], tmp[i+1] = tmp[i+1], tmp[i]
            # if debug == 3:
                # message("(" + inspect.stack()[0][3] + ") " + "Info: " + "Method: swap " + "tmp[" + str(i) + "] = " + tmp[i] + " and tmp[" + str(i+1) + "] = " + tmp[i+1])
            
            swap = ''.join(tmp)
            
            # Swap back
            # Actually, no need as we restore full tmp in the beginning of cycle
            # tmp[i], tmp[i+1] = tmp[i+1], tmp[i]
            
            if is_id_valid_basic(swap):
                similarities.append(swap)
        
# END FOR

    return similarities

def what_to_do():
    debug = int(os.environ['DEBUG'])
    title = "Choices: "
    msg = "What to do? (0-5): "
    choices = ['0 = Exit',
               '1 = Check ID validity',
               '2 = Calculate ID check digit',
               '3 = Find similar IDs of one ID',
               '4 = Find similar IDs of random ID',
               '5 = Find similar IDs of range of IDs']
    choice = ''
    while choice not in range (0, 6):
        if debug == 4:
            tmp = choicebox(msg, title, choices)
            if tmp:
                choice = int(tmp.split()[0])
            else: # Cancel was pressed
                # choice = '' # Re-enter
                choice = 0 # We will exit
        else:
            print()
            print(title)
            for i in range(0, len(choices)):
                print("\t" + choices[i])
            
            choice = sanitised_input(msg, int, 0, 5)
    
    return choice

# Not in use at the moment
# TODO: implement different algorithms
def what_algorithm():
    debug = int(os.environ['DEBUG'])
    title = "Choices: "
    msg = "What algorithm to use? (0-2): "
    algorithms = ['0 = Exit',
                  '1 = Algorithm EID (https://et.wikipedia.org/wiki/Isikukood)',
                  '2 = Algorithm LUHN (https://en.wikipedia.org/wiki/Luhn_algorithm)',
                 # '3 = Algorithm LUHN MOD N (https://en.wikipedia.org/wiki/Luhn_mod_N_algorithm)',
                 # '4 = Algorithm VERHOEFF (https://en.wikipedia.org/wiki/Verhoeff_algorithm)', 
                 # '5 = Algorithm DAMM (https://en.wikipedia.org/wiki/Damm_algorithm)'
                 ]
    algorithm = ''
    while algorithm not in range (0, 3):
        if debug == 4:
            tmp = choicebox(msg, title, algorithms)
            if tmp:
                algorithm = int(tmp.split()[0])
            else: # Cancel was pressed
                # algorithm = 0 # We will exit
                algorithm = '' # Re-enter
        else:
            print()
            print(title)
            for i in range(0, len(choices)):
                print("\t" + choices[i])
        
        algorithm = sanitised_input(msg, int, 0, 2)
    
    return algorithm

def get_defaults():
    # Century
    min_century = 3
    max_century = 6
    # Year
    min_year = 0
    max_year = 99
    # Month
    min_month = 1
    max_month = 12
    # Day
    min_day = 1
    max_day = 31
    # Sequence
    min_sequence = 0
    max_sequence = 999
    
    return min_century, max_century, min_year, max_year, min_month, max_month, min_day, max_day, min_sequence, max_sequence

# Calculate approximate speed of system by executing find_similar_one within sample_sec seconds with dummy data
def calc_sample_speed():
    debug = int(os.environ['DEBUG'])
    sample_sec = 2
    sample_eid10 = '4321123456'
    sample_check_digit = '9'
    
    if debug == 3:
        message("Info: " + "Calculate approximate speed of system by executing find_similar_one within " + str(sample_sec) + " seconds with dummy data")
    
    # Keep current debug level and do set temporary debug level = 0
    tmp_debug = os.environ['DEBUG']
    os.environ['DEBUG'] = '0'
    
    sample_nof_id = 0
    start_time = time.time()
    
    while time.time() - start_time < sample_sec:
        find_similar_one(sample_eid10 + sample_check_digit)
        sample_nof_id += 1
    
    sample_time = time.time() - start_time
    
    # Restore debug level
    os.environ['DEBUG'] = tmp_debug
    
    if debug == 3:
        message("Info: " + "Sample ID speed calculation " + str(sample_nof_id) + " times within " + str(sample_time) + " seconds")
    
    return (sample_nof_id, sample_time)

def main_check_id_validity():
    debug = int(os.environ['DEBUG'])
    valid = False
    id = ""
    msg = "Enter ID to check its validity (0 to exit): "
    
    if debug == 4:
        id = enterbox(msg)
    else:
        id = sanitised_input(msg, str)
        
    # For test purposes, some unit tests
    # ID = '' # Validity = False, Empty
    # ID = '0' # Validity = False, Length < 11
    # ID = '123456789012' # Validity = False, (is_id_len) Warning: ID '123456789012'. Length = 12 is not 11
    # ID = 'ABCDEFGHIJK' # Validity = False, (is_id_digit) Warning: ID 'ABCDEFGHIJK'. Digit = False
    # ID = '00000000000' # Validity = False, (is_id_century) Warning: ID '00000000000'. Century = 0
    # ID = '70000000000' # Validity = False, (is_id_century) Warning: ID '70000000000'. Century = 7
    # ID = '30000000000' # Validity = False, (is_id_date) Warning: Date 1900-0-0 is not valid.
    # ID = '30099000000' # Validity = False, (is_id_date) Warning: Date 1900-99-0 is not valid.
    # ID = '30012990000' # Validity = False, (is_id_date) Warning: Date 1900-12-99 is not valid.
    # ID = '30012310000' # Validity = False, (is_id_check) Warning: ID = '30012310000'. Given check digit = 0 Calculated check digit = 9
    # ID = '30001010004' # Validity = True

    # if id == None: # button Cancel pressed
    if not (id == "0" or id == "" or id == None):
        valid = is_id_valid_full(id)
        # message("*** Result: " + "ID = '" + str(id) + "'. Validity = " + str(valid))
    
    return id, valid

def main_calculate_id_check_digit():
    debug = int(os.environ['DEBUG'])
    check = None
    id = ""
    msg = "Enter ID to calculate its check digit (0 to exit): "
    
    valid = False
    while not valid:
        if debug == 4:
            id = enterbox(msg)
        else:
            id = sanitised_input(msg, str)
        
        # For test purposes, some unit tests
        # ID = '' check digit = 'None'. Full ID = 'None'.
        # ID = '1' Warning: Length of ID must be at least 10 and it must include only digits. Please re-enter.
        # ID = 'a' Warning: Length of ID must be at least 10 and it must include only digits. Please re-enter.
        # ID = '0000000000' check digit = '0'. Full ID = '00000000000'.
        # ID = '9999999999' check digit = '7'. Full ID = '99999999997'.
        # ID = '36210010120' check digit = '0'. Full ID = '362100101200'. Warning: Length of ID is 11. Will use only first 10 digits to calculate check digit, ignore the rest.
        # ID = '46210010120' check digit = '0'. Full ID = '462100101200'. Warning: Length of ID is 11. Will use only first 10 digits to calculate check digit, ignore the rest.
        # ID = '51107121760' check digit = '0'. Full ID = '511071217600'. Warning: Length of ID is 11. Will use only first 10 digits to calculate check digit, ignore the rest.
        # ID = '61107121760' check digit = '0'. Full ID = '611071217600'. Warning: Length of ID is 11. Will use only first 10 digits to calculate check digit, ignore the rest.
        # ID = '39303312282' check digit = '2'. Full ID = '393033122822'. Warning: Length of ID is 11. Will use only first 10 digits to calculate check digit, ignore the rest.

        # if id == None: # button Cancel pressed
        if not (id == "0" or id == "" or id == None):
            length = len(id)
            valid = (length >= 10 and is_id_digit(id)) # True/False
            
            if valid:
                if length > 10:
                    message("Warning: " + "Length of ID is " + str(length) + ". Will use only first 10 digits to calculate check digit, ignore the rest.")
                
                check = calc_id_check(id[:10])
                # message("*** Result: " + "ID = '" + str(id[0:10]) + "' check digit = '" + str(check) + "'. Full ID = '" + str(id[0:10]) + str(check) + "'.")
            
            else:
                message("Warning: " + "Length of ID must be at least 10 and it must include only digits. Please re-enter.")
        
        else:
            # 0 or nothing entered or Cancel pressed, break from cycle
            break
    
    return id, check

def main_find_similar_ids():
    id = None
    valid = False
    id_similarities = {}
    
    msg = "Enter ID to find similar IDs (0 to exit): "
    while not valid:
        if debug == 4:
            id = enterbox(msg)
        else:
            id = sanitised_input(msg, str)

        # For test purposes, some unit tests
        # ID: '' = None # Similarities not found.
        # ID: '1' is not valid ID. Please re-enter. # (is_id_len) Warning: ID '1'. Length = 1 is not 11
        # ID: 'a' is not valid ID. Please re-enter. # (is_id_len) Warning: ID 'a'. Length = 1 is not 111
        # ID: 'aaaaaaaaaaa' is not valid ID. Please re-enter. # (is_id_digit) Warning: ID 'aaaaaaaaaaa'. Digit = False
        # ID: '11111111111' is not valid ID. Please re-enter. # (is_id_century) Warning: ID '11111111111'. Century = 1
        # ID: '39303312780' is not valid ID. Please re-enter. # (is_id_check) Warning ID = '39303312780'. Given check digit = 0 Calculated check digit = 3
        # ID: '39303312783' = None # Similarities not found.
        # ID: '36210010120' = ['36201010120', '36210010130', '46210010120']
        # ID: '46210010120' = ['36210010120', '46210010110']
        # ID: '51107121760' = ['51107112760', '51107121770', '61107121760']
        # ID: '61107121760' = ['51107121760', '61107121750']
        # ID: '39303312282' = ['39303313282']
        
        if not (id == "0" or id == "" or id == None):
            valid = is_id_valid_full(id)
        else:
            # Return empty set of similarities
            return id, id_similarities
    
        if not valid:
           message("Error: " + "ID '" + str(id) + "' is not valid ID. Please re-enter.")
        
    # Valid ID was entered
    # check = calc_id_check(id)
    tmp = find_similar_one(id)
    if tmp:
        id_similarities[id] = sorted(tmp)
        # message("*** Result: " + "ID: '" + str(id) + "' = " + str(id_similarities[id])) 
    # else:
        # message("*** Result: " + "ID: '" + str(id) + "' -- No similarities found.")

    return id, id_similarities

def main_find_similar_ids_of_random_id():
    id = None
    valid = False
    id_similarities = {}
    min_century, max_century, min_year, max_year, min_month, max_month, min_day, max_day, min_sequence, max_sequence = get_defaults()

    # For test purposes, some unit tests
    # ID: '58901081421' = ['58901081521']
    # ID: '48608052390' = ['48608053290']
    # ID: '38302111067' = ['38202111067', '38302112067']

    while not valid:
        # random.randint - generate pseudo-random century/date
        century = random.randint(min_century, max_century)
        year = max_year = random.randint(min_year, max_year)
        month = random.randint(min_month, max_month)
        day = random.randint(min_day, max_day)
        sequence = random.randint(min_sequence, max_sequence)
        id10 = str(century) + str(year).zfill(2) + str(month).zfill(2) + str(day).zfill(2) + str(sequence).zfill(3)
        check = calc_id_check(id10)
        id = str(id10) + str(check)
        valid = is_id_valid_full(id)

    message("Info: " + "Random ID = " + str(id))
    tmp = find_similar_one(id)
    
    if tmp:
        id_similarities[id] = sorted(tmp)
        # message("*** Result: " + "ID: '" + str(id) + "' = " + str(id_similarities[id])) 
    # else:
        # message("*** Result: " + "ID: '" + str(id) + "' -- No similarities found.")
    
    return id, id_similarities

def main_find_similar_ids_of_range_id(pid):
    # Argument pid is used to creat temporary files within process
    # Keep these filenames within list and return to main function
    tmp_filenames = []
    
    id_similarities = {}
    nof_id = nof_id_valid_checked = 0
    nof_id_similarities = 0 # len(id_similarities)
    min_century, max_century, min_year, max_year, min_month, max_month, min_day, max_day, min_sequence, max_sequence = get_defaults()

    # For test purposes, some unit tests
    # min_century = max_century = 3
    # min_year = max_year = 62
    # min_month = max_month = 10
    # min_day = max_day = 1
    # min_sequence = max_sequence = 12
    
    # TODO: better logic of input from user. Consider to use multenterbox http://easygui.sourceforge.net/tutorial.html#multenterbox
    # message("Info: " + "CENTURY of ID is 3 or 4 for XX century (born 1900-1999, 3 for male, 4 for female); 5 or 6 for XXI century (born 2000-2099, 5 for male, 6 for female)")
        
    # Ask century, year, month, day and sequence from user
    min_century, max_century = ask_start_end("century", min_century, max_century)
    min_id = max_id = None
    
    if min_century == None or max_century == None:
        message("Warning: " + "Cancel pressed.")
        return min_id, max_id, nof_id, nof_id_valid_checked, nof_id_similarities, tmp_filenames
    
    min_year, max_year = ask_start_end("year", min_year, max_year)
    if min_year == None or max_year == None:
        message("Warning: " + "Cancel pressed.")
        return min_id, max_id, nof_id, nof_id_valid_checked, nof_id_similarities, tmp_filenames
    
    min_month, max_month = ask_start_end("month", min_month, max_month)
    if min_month == None or max_month == None:
        message("Warning: " + "Cancel pressed.")
        return min_id, max_id, nof_id, nof_id_valid_checked, nof_id_similarities, tmp_filenames
    
    min_day, max_day = ask_start_end("day", min_day, max_day)
    if min_day == None or max_day == None:
        message("Warning: " + "Cancel pressed.")
        return min_id, max_id, nof_id, nof_id_valid_checked, nof_id_similarities, tmp_filenames
    
    min_sequence, max_sequence = ask_start_end("sequence", min_sequence, max_sequence)
    if min_sequence == None or max_sequence == None:
        message("Warning: " + "Cancel pressed.")
        return min_id, max_id, nof_id, nof_id_valid_checked, nof_id_similarities, tmp_filenames

    min_id = str(min_century) + str(min_year).zfill(2) + str(min_month).zfill(2) + str(min_day).zfill(2) + str(min_sequence).zfill(3)
    max_id = str(max_century) + str(max_year).zfill(2) + str(max_month).zfill(2) + str(max_day).zfill(2) + str(max_sequence).zfill(3)
    message("Info: " + "Similarities of ID-s to find: from " + min_id + " to " + max_id)
    
    # start_eid10 is used to create temporary files
    start_eid10 = min_id

    nof_id = (max_century - min_century + 1) \
        * (max_year - min_year + 1) \
        * (max_month - min_month + 1) \
        * (max_day - min_day + 1) \
        * (max_sequence - min_sequence + 1)
        
    if nof_id > 1000:
        sample_nof_id, sample_time = calc_sample_speed()
    
        # Every sample_nof_id IDs calculation takes appr str(sample_time) seconds
        estimated_time_seconds = int(nof_id * sample_time / sample_nof_id)
        if debug == 3:
            message("Info: " + "Estimated time to calculate: " + str(estimated_time_seconds) + " seconds")
    
        # Calculate days, hours, minutes and seconds of estimated time
        # Idea source: https://stackoverflow.com/questions/775049/python-time-seconds-to-hms
        m, s = divmod(estimated_time_seconds, 60)
        h, m = divmod(m, 60)
        d, h = divmod(h, 24)
        msg = "Warning: " + "Number of ID-s to be calculated is at least " + group(nof_id) + ".\nIt might take a looooooong time (appr. " + "%d days %d hrs %d min %d sec" % (d, h, m, s) + ")"
    
        # More than one month to calculate or computer slower than 60 seconds
        if nof_id > 31000 or estimated_time_seconds > 60:
            if debug:
                message(msg)
            else:
                # Ensure the message is printed into console even if debug level is not set
                print(msg)
            
            msg = "Do you want to continue? "
            choices = ('YES', 'no')
            if debug == 4:
                result = ynbox(msg, "Please confirm (" + ', '.join(choices) + ")") # show a Yes/no dialog
            else:
                result = query_yes_no(msg)
        
            if not result: # True (for continue) or False (for cancel)
                # Get out of current elif, continue with main while-cycle
                return min_id, max_id, nof_id, nof_id_valid_checked, nof_id_similarities, tmp_filenames
                # sys.exit("OK, exiting.")

    if debug == 3:
        message("Info: " + "Calculating ... Press Enter/OK to start")
    
    start_time = time.time()
    
    for century in range (min_century, max_century + 1): # (3, 7):
        if debug == 3:
            message("Info: " + "Century = " + str(century))
        
        for year in range (min_year, max_year + 1): # (1, 100):
            if debug == 3:
                message("Info: " + "Year = " + str(year))
            
            # start_eid10 is used to create temporary files for found similarities of every year
            # We do it to keep need for RAM as low as possible
            # This will be done only on accuracy / level of year, therefor we do use min_month, min_day and min_sequence
            start_eid10 = str(century) + str(year).zfill(2) + str(min_month).zfill(2) + str(min_day).zfill(2) + str(min_sequence).zfill(3)
            
            # Calculate year as YYYY according to century
            yyyy = (17 + (century + 1) // 2) * 100 + year
            for month in range (min_month, max_month + 1): # (1, 13):
                if debug == 3:
                    message("Info: " + "Month = " + str(month))
                    
                for day in range (min_day, max_day + 1): # (1, 32):
                    if debug == 3:
                        message("Info: " + "Day = " + str(day))
                        
                    if is_date_valid (yyyy, month, day):
                        if debug == 3:
                            message("Info: " + "Valid date: " + str(day) + "." + str(month) + "." + str(yyyy))
                            
                        if (max_sequence > min_sequence):
                            print(str(century) + str(year).zfill(2) + str(month).zfill(2) + str(day).zfill(2) + " " + str(min_sequence).zfill(3), end = "")
                            
                        for sequence in range (min_sequence, max_sequence + 1): # (0, 1000):
                            # message("Info: " + "Sequence = " + str(sequence))
                            # Print progress bar ...
                            if not sequence % 10:
                                print(".", end = "")
                        
                            # Create 10-digit length ID, without check digit
                            id10 = str(century) + str(year).zfill(2) + str(month).zfill(2) + str(day).zfill(2) + str(sequence).zfill(3)
                        
                            check_id = calc_id_check(str(id10))
                            # compile together first 10 digits of ID and Estonian-specific check_id
                            id = str(id10) + str(check_id)
                            # 
                            # Call of find_similar_one
                            # ----------
                            tmp = find_similar_one(id)
                            # ----------
                            #
                            nof_id_valid_checked += 1
                            
                            if tmp:
                                id_similarities[id] = sorted(tmp)
                                nof_id_similarities += 1
                                if debug == 3:
                                    message("Info: " + "ID: " + "id_similarities[" + str(id) + "] = " + str(id_similarities[id])) 
                            
                            else:
                                if debug == 3:
                                    message("Info: " + "ID: " + str(id) + " -- No similarities found.")
                        # End of for cycle
                        
                    else:
                        # Date was not valid, set sequence as negative. We will use it in following not to print out end of sequence
                        sequence = -1
                        if debug == 3:
                            message("Info: " + "Date is not valid: " + str(day) + "." + str(month) + "." + str(year))
                        
                    # Check sequence. If sequence is negative, we will not print out end of sequence
                    if (max_sequence > min_sequence) and sequence >=0:
                        print(str(max_sequence) + " - 100%")
                        sys.stdout.flush()
                        
                    if debug == 3:
                        message("Info: " + "End of day: " + str(day))
                    
                if debug == 3:
                    message("Info: " + "End of month: " + str(month))
                
            if debug == 3:
                message("Info: " + "End of year: " + str(year))
            
            # Keep similarities within temporary file
            # start_eid10 was initiated earlier, id10 is current id to find similarities within cycle
            # We do it to keep need for RAM as low as possible
            # This will be done only on accuracy / level of year
            tmp_filename = "tmp_" + str(pid) + "_" + start_eid10 + "-" + id10 + "_similarities_id.json"
            with open(tmp_filename, 'w') as fp:
                    json.dump(id_similarities, fp, indent = 4)
            tmp_filenames.append(tmp_filename)
            
            # Flush similarities
            id_similarities = {}
        
        if debug == 3:
            message("Info: " + "End of century: " + str(century))
        
    if debug == 3:
        message("Info: " + "END")

    end_time = time.time()
        
    if start_time:
        message("*** Result: " + "--- %s seconds ---" % (end_time - start_time))

    return min_id, max_id, nof_id, nof_id_valid_checked, nof_id_similarities, tmp_filenames

# Find similarities with maximum length
# TODO: it is not the best solution as it keeps also all current max length elements, growing from first until to final max
# ... but we will remove them within additional cycle. It seems to me little bit crappy
def GetMaxLen(id_similarities):
    max_length = 0
    tmp_id_similarities = {}
    
    for key, value in id_similarities.items():
            if len(value) >= max_length:
                    max_length = len(value)
                    tmp_id_similarities[key] = value
                    # max_key = key
                    # max_value = value
    
    # Another cycle to remove shorter elements from the beginning ...
    max_id_similarities = {}
    for key, value in tmp_id_similarities.items():
        if len(value) == max_length:
            max_id_similarities[key] = value
    
    return max_length, max_id_similarities

######################################################################
# MAIN
######################################################################

debug = int(os.environ['DEBUG'])
choice = ''

#
# NB! We assume that ID, its beginning and all elements, incl check are strings
# When needed, then transform into int or list or whatever you need but transform into string back later
#

while True:
    # Get current process id to be used as identifier in temporary files during choice = 5
    pid = os.getpid()
    if debug == 3:
        message("Info: " + "Current PID = " + str(pid))
    
    choice = what_to_do()
    if debug == 3:
        message("Info: " + "Your choice was: " + str(choice))

    if choice == 0:
        # Exit
        message("*** Result: " + "Exiting")
        sys.exit(0)
    
    # TODO: implement different algorithms
    # algorithm = what_algorithm()
    # message("Info: " + "Algorithm is: " + str(algorithm))
    
    id = min_id = max_id = None
    check = None
    id_similarities = {}
    # Check ID validity (algorithm EID)
    if choice == 1:
        id, valid = main_check_id_validity()
        message("*** Result: " + "ID = '" + str(id) + "'. Validity = " + str(valid))
   
    # Calculate ID check digit (algorithm EID)
    elif choice == 2:
        id, check = main_calculate_id_check_digit()
        message("*** Result: " + "ID = '" + str(id) + "' check digit = '" + str(check) + "'. Full ID = '" + str(id) + str(check) + "'.")
        
    # Find similar IDs of one ID (algorithm EID)
    elif choice == 3:
        id, id_similarities = main_find_similar_ids()
        message("*** Result: " + "ID: '" + str(id) + "' = " + str(id_similarities.get(id, None)))

    # Find similar IDs of random ID (algorithm EID)
    elif choice == 4:
        id, id_similarities = main_find_similar_ids_of_random_id()
        message("*** Result: " + "ID: '" + str(id) + "' = " + str(id_similarities.get(id, None)))

    # Find similar IDs of range of IDs
    elif choice == 5:
        # Get current process id to be used as identifier in temporary files during choice = 5
        # Use it as argument for main_find_similar_ids_of_range_id()
        pid = os.getpid()
        if debug == 3:
            message("Info: " + "Current PID = " + str(pid))
    
        min_id, max_id, nof_id, nof_id_valid_checked, nof_id_similarities, tmp_filenames = main_find_similar_ids_of_range_id(pid)
        message("*** Result: " + "ID range '" + str(min_id) + "' - '" + str(max_id) + "' - found " + str(nof_id_similarities) + " similarities")
        
        # If found some similarities
        if nof_id_similarities > 0:
            filename = min_id + "-" + max_id + "_similarities_id.json"
            message("*** Result: " + "write file: " + filename)
            
            # If filename exists
            result = True
            if os.path.exists(filename):
                msg = "Warning: " + filename + " exists.\nDo you want to overwrite? "
                choices = ('YES', 'no')
                if debug == 4:
                    result = ynbox(msg, "Please confirm (" + ', '.join(choices) + ")") # show a Yes/no dialog
                else:
                    result = query_yes_no(msg)
            
            # Ask for new filename
            if result == False:
                msg = "Enter filename: "
                if debug == 4:
                    filename = filesavebox(msg=msg, title=msg, default=filename, filetypes=None)
                else:
                    filename = sanitised_input(msg, str)
            
            # Save into file
            # Do cycle over tmp_filenames to read
            if not filename == None:
                id_similarities = {}
                for tmp_filename in tmp_filenames:
                    with open(tmp_filename, "r") as fi:
                        tmp_id_similarities = json.load(fi)
                    
                    id_similarities.update(tmp_id_similarities)
                    # Remove tmp_filenames
                    # os.remove(tmp_filename)
                    
                with open(filename, 'w') as fp:
                    json.dump(id_similarities, fp, indent = 4)
                
                # Find similarities with maximum length
                max_length, max_id_similarities = GetMaxLen(id_similarities)
                
                msg = ""
                # return min_id, max_id, nof_id, nof_id_valid_checked, nof_id_similarities, tmp_filenames
                msg = msg + "\n" + "*** Result: " + "Total number of IDs reviewed = " + str(nof_id_valid_checked)
                msg = msg + "\n" + "From them number of IDs with similarities = " + str(len(id_similarities))
                if nof_id_valid_checked:
                    msg = msg + " " + '({0:.2f}%)'.format(len(id_similarities) /  nof_id_valid_checked)
                
                msg = msg + "\n" + "Max number of similarities = " + str(max_length) + " found for these IDs:"
                
                for key, value in max_id_similarities.items():
                    msg = msg + "\n" + "\"" + key + "\"" + ": " + str(value)
                
                message(msg)
                
                # Temporary solution - Exit immediately
                # sys.exit(0)
            
    # All the rest of choices if in whatever reason they came through until here
    else:
        message("Error: " + "Unknown choice: " + str(choice))

'''
# TODO: different algorithms to implement
# LUHN
luhn_similarities = {}
nof_luhn_similarities = 0 # len(luhn_similarities)
# LUHN = Luhn ID (check digit according to Luhn algorithm)
check_luhn = luhn_checksum(str(id10))
# compile together first 10 digits of ID and Estonian-specific check_id
luhn = str(id10) + str(check_luhn)
tmp = find_similar_one(luhn, "luhn")
if tmp:
    luhn_similarities[luhn] = sorted(tmp)
    print("Info: " + "LUHN: " + "luhn_similarities[" + str(luhn) + "] = " + str(luhn_similarities[luhn]))
    nof_luhn_similarities += 1
else:
    message("Info: " + "LUHN: " + str(luhn) + " -- Similarities not found.")
'''
'''
print ("Info" + "LUHN: found " + str(nof_luhn_similarities) + " similarities")
print("Info: " + "write file: " + min_id + "-" + max_id + "_similarities_luhn.json")
with open(min_id + "-" + max_id + "_similarities_luhn.json", 'w') as fp:
    json.dump(luhn_similarities, fp, indent = 4)
# f = open(min_id + "-" + max_id + "_similarities_luhn.txt", "w")
# f.write(str(luhn_similarities))
# f.close()
'''

