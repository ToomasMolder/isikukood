# Find, how many similarities in ID (isikukood) is available when using check digit calculation algorithm
#    according to Estionian ID https://et.wikipedia.org/wiki/Isikukood and
#    according to Luhn algorithm https://en.wikipedia.org/wiki/Luhn_algorithm
# 
# Author: Toomas Mölder <toomas.molder@gmail.com>, +372 5522000
# Started: 2017-05-16
# Last modified: 2017-05-21
#
# NB! Might be buggy and crappy, written for own purposes
# NB! Global configuration signature is not checked. Use this program at your own risk.
# TODO: better logic of input from user
# TODO: rewrite similarities algorithm to find possible wrong keypresses on keyboard
# TODO: sort and collect similarities to avoid duplicate similarities found

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

# Debug levels defined in MAIN:
# 0 = Errors only
# 1 = Warnings as well
# 2 = Info
# 3 = GUI
# 4 = ... (for future use)
#
os.environ['DEBUG'] = '0'

def message(msg):
    debug = int(os.environ['DEBUG'])
    if debug >=3:
        # Do it with easygui
        msgbox(msg)
    else:
        if (("Info" in msg and debug >= 2) or
            ("Warning" in msg and debug >= 1) or
            ("Error" in msg and debug >= 0)):
            print(msg)
            # sys.stdout.flush()
    return

# See also: https://et.wikipedia.org/wiki/Isikukood
def calc_id_check(id):
    debug = int(os.environ['DEBUG'])
    weight1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 1]
    weight2 = [3, 4, 5, 6, 7, 8, 9, 1, 2, 3]
    check = 0
    id_as_list = list(id)
    for i in range(10):
        check += int(id[i]) * weight1[i]
    check = check % 11
    if check == 10:
        check = 0
        for i in range(10):
            check += int(id[i]) * weight2[i]
        check = check % 11
        if check == 10:
            check = 0
    if debug >= 2:
        message("(" + inspect.stack()[0][3] + ") " + "Info: " + "ID " + id + " check = " + str(check))
    
    return check

def is_id_len(id):
    debug = int(os.environ['DEBUG'])
    if debug >= 2:
        message("(" + inspect.stack()[0][3] + ") " + "Info: " + "ID " + id + " length = " + str(len(id)))
    if len(id) == 11:
        return True
    else:
        if debug >= 1:
            message("(" + inspect.stack()[0][3] + ") " + "Warning: " + "ID " + id + " length = " + str(len(id)))
        return False

def is_id_digit(id):
    debug = int(os.environ['DEBUG'])
    if debug >= 2:
        message("(" + inspect.stack()[0][3] + ") " + "Info: " + "ID " + id + " digit = " + str(id.isdigit()))
    if id.isdigit():
        return True
    else:
        if debug >= 1:
            message("(" + inspect.stack()[0][3] + ") " + "Warning: " + "ID " + id + " digit = " + str(id.isdigit()))
        return False

def is_id_century(id):
    debug = int(os.environ['DEBUG'])
    # Currently we do look only persons born between 1900-2099
    # Born 1900-1999 male century is 3, female century is 4
    # Born 2000-2099 male century is  5, female century is 6
    min_century = 3
    max_century = 6
    if debug >= 2:
        message("(" + inspect.stack()[0][3] + ") " + "Info: " + "ID " + id + " century = " + str(id[0]))
    if (int(id[0]) >= min_century and int(id[0]) <= max_century):
        return True
    else:
        if debug >= 1:
            message("(" + inspect.stack()[0][3] + ") " + "Warning: " + "ID " + id + " century = " + str(id[0]))
        return False

# http://stackoverflow.com/questions/9987818/in-python-how-to-check-if-a-date-is-valid
def is_date_valid(year, month, day):
    debug = int(os.environ['DEBUG'])
    if debug >= 2:
        message("(" + inspect.stack()[0][3] + ") " + "Info: Is Date Valid = " + str(year) + "-" + str(month) + "-" + str(day))
    this_date = '%d/%d/%d' % (month, day, year)
    try:
        time.strptime(this_date, '%m/%d/%Y')
    except ValueError:
        if debug:
            message("(" + inspect.stack()[0][3] + ") " + "Error: Is Date Valid = " + str(year) + "-" + str(month) + "-" + str(day))
        return False
    else:
        return True

def is_id_date(id):
    debug = int(os.environ['DEBUG'])
    century = int(id[0])
    yy = int(id[1:3])
    yyyy = (17 + (century + 1) // 2) * 100 + yy
    mm = int(id[3:5])
    dd = int(id[5:7])
    if debug >= 2:
        message("(" + inspect.stack()[0][3] + ") " + "Info Date: Century = " + str(century) +
                " Year (yy) = " + str(yy) +
                " Year (yyyy) = " + str(yyyy) +
                " Month = " + str(mm) +
                " Day = " + str(dd))
    if is_date_valid (yyyy, mm, dd):
        return True
    else:
        if debug >= 1:
            message("(" + inspect.stack()[0][3] + ") " + "Warning: Date: Century = " + str(century) +
                    " Year (yy) = " + str(yy) +
                    " Year (yyyy) = " + str(yyyy) +
                    " Month = " + str(mm) +
                    " Day = " + str(dd))
        return False

def is_id_check(id):
    debug = int(os.environ['DEBUG'])
    check = calc_id_check(id[:10])
    if debug >= 2:
        message("(" + inspect.stack()[0][3] + ") " + "Info: Given check = " + str(id[10]) + " Calculated check = " + str(check))
    if int(id[10]) == check:
        return True
    else:
        if debug >= 1:
            message("(" + inspect.stack()[0][3] + ") " + "Warning: Given check = " + str(id[10]) + " Calculated check = " + str(check))
        return False
    # return int(id[10]) == calc_id_check(id[:10])

# Basic check of ID validity
def is_id_valid(id):
    return (is_id_len(id) and
            is_id_digit(id) and
            is_id_century(id) and
            is_id_date(id) and
            is_id_check(id))

# https://en.wikipedia.org/wiki/Luhn_algorithm
def digits_of(number):
    return [int(i) for i in str(number)]

def luhn_checksum(card_number):
    digits = digits_of(card_number)
    odd_digits = digits[-1::-2]
    even_digits = digits[-2::-2]
    total = sum(odd_digits)
    for digit in even_digits:
        total += sum(digits_of(2 * digit))
    return total % 10

def is_luhn_valid(card_number):
    return luhn_checksum(card_number) == 0

def calculate_luhn(partial_card_number): 
    check_digit = luhn_checksum(int(partial_card_number) * 10)   # Append a zero check digit to the partial number and calculate checksum
    return check_digit if check_digit == 0 else 10 - check_digit # If the (sum mod 10) == 0, then the check digit is 0
                                                                 # Else, the check digit = 10 - (sum mod 10)

def find_similar(id, check):
    debug = int(os.environ['DEBUG'])
    # TODO: find 'neighbour' keypresses
    # keyboard = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]
    # keyboard_shift_left = [1, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    # keyboard_shift_right = [2, 3, 4, 5, 6, 7, 8, 9, 0, 0]
    similarities = []
    # Consider as list
    id_as_list = list(id)
    # Cycle over all digits in ID, but not the last digit (check digit)
    for i in range(0, len(id_as_list) - 1):
        tmp = copy.deepcopy(id_as_list)
        # tmp[i] = keyboard_shift_left[keyboard.index(list_koodi_algus[i])]
        # Element must be > 0, only then we calculate smaller
        if int(id_as_list[i]) > 0:
            tmp[i] = str(int(id_as_list[i]) - 1)
            message("(" + inspect.stack()[0][3] + ") " + "Info: id_as_list[" + str(i) + "] = " + id_as_list[i] + " / tmp[" + str(i) + "] = " + tmp[i])
            smaller = ''.join(tmp)
            message("(" + inspect.stack()[0][3] + ") " + "Info: Smaller = " + smaller)
            smaller_check = calc_id_check(smaller)
            if smaller_check == check:
                message("(" + inspect.stack()[0][3] + ") " + "*** Info: ID " + id + " smaller similar: " + smaller)
                similarities.append(smaller)
        
        # tmp[i] = keyboard_shift_right[keyboard.index(int(list_koodi_algus[i]))]
        # Element must be < 9, only then we calculate bigger
        if int(id_as_list[i]) < 9:
            tmp[i] = str(int(id_as_list[i]) + 1)
            message("(" + inspect.stack()[0][3] + ") " + "Info: id_as_list[" + str(i) + "] = " + id_as_list[i] + " / tmp[" + str(i) + "] = " + tmp[i])
            bigger = ''.join(tmp)
            message("(" + inspect.stack()[0][3] + ") " + "Info: Bigger = " + bigger)
            bigger_check = calc_id_check(bigger)
            if bigger_check == check:
                message("(" + inspect.stack()[0][3] + ") " + "*** Info: ID " + id + " bigger similar: " + bigger)
                similarities.append(bigger)
        # END FOR

    return similarities

# function def_sanitised from http://stackoverflow.com/questions/23294658/asking-the-user-for-input-until-they-give-a-valid-response
def sanitised_input(prompt, type_=None, min_=None, max_=None, range_=None):
    if min_ is not None and max_ is not None and max_ < min_:
        raise ValueError("min_ must be less than or equal to max_.")
    while True:
        ui = input(prompt)
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

# http://stackoverflow.com/questions/3041986/apt-command-line-interface-like-yes-no-input
def query_yes_no(question, default="yes"):
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
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")

# http://stackoverflow.com/questions/1823058/how-to-print-number-with-commas-as-thousands-separators
def group(number):
    s = '%d' % number
    groups = []
    while s and s[-1].isdigit():
        groups.append(s[-3:])
        s = s[:-3]
    return s + '.'.join(reversed(groups))


###
# MAIN
###

# NB! We assume that ID, its beginning and all elements, incl check are strings
# When needed, then transform into int or list or whatever you need but transform into string back later
#
debug = int(os.environ['DEBUG'])

'''
# For test purposes, some unit tests
id = "" # Empty
print("Info: " + str(id) + " -- " + str(is_id_valid(id)))
print()

id = "0" # Length < 11
print("Info: " + str(id) + " -- " + str(is_id_valid(id)))
print()

id = "123456789012" # Length > 11
print("Info: " + str(id) + " -- " + str(is_id_valid(id)))
print()

id = "ABCDEFGHIJK" # Nodigits
print("Info: " + str(id) + " -- " + str(is_id_valid(id)))
print()

id = "00000000000" # Century < 3
print("Info: " + str(id) + " -- " + str(is_id_valid(id)))
print()

id = "70000000000" # Century > 6
print("Info: " + str(id) + " -- " + str(is_id_valid(id)))
print()

id = "30000000000" # Date not valid
print("Info: " + str(id) + " -- " + str(is_id_valid(id)))
print()

id = "30099000000" # Month not valid
print("Info: " + str(id) + " -- " + str(is_id_valid(id)))
print()

id = "30012990000" # Day not valid
print("Info: " + str(id) + " -- " + str(is_id_valid(id)))
print()

id = "30012310000" # Check not valid
print("Info: " + str(id) + " -- " + str(is_id_valid(id)))
print()

id = "30001010004" # id valid
print("Info: " + str(id) + " -- " + str(is_id_valid(id)))
print()
'''
'''
# For test purposes, few similar known pairs 
id1 = "51107121760"
id2 = "61107121760"
print("Info: " + str(id1) + " -- " + str(is_id_valid(id1)))
print("Info: " + str(id2) + " -- " + str(is_id_valid(id2)))
print()

id1 = "39303312783"
id2 = "39303312282"
print("Info: " + str(id1) + " -- " + str(is_id_valid(id1)))
print("Info: " + str(id2) + " -- " + str(is_id_valid(id2)))
print()

id1 = "36210010120"
id2 = "46210010120"
print("Info: " + str(id1) + " -- " + str(is_id_valid(id1)))
print("Info: " + str(id2) + " -- " + str(is_id_valid(id2)))
print()
'''
'''
# For test purposes
id = "36210010120" # id = 36210010120 check = 0 -- Similarities: ['46210010120', '36210010130']
id = "46210010120" # id = 46210010120 check = 0 -- Similarities: ['36210010120', '46210010110']
id = "51107121760" # id = 51107121760 check = 0 -- Similarities: ['61107121760', '51107121770']
id = "61107121760" # id = 61107121760 check = 0 -- Similarities: ['51107121760', '61107121750']
id = "39303312282" # id = 39303312282 check = 2 -- Similarities: ['39303313282']
id = "39303312783" # Similarities not found.
id = "39303312780" # Warning: 39303312780 -- False

if is_id_valid(id):
    check = calc_id_check(id)
    message("MAIN Info: check = " + str(check))
    similarities = find_similar(id, check)
    if similarities:
        message("MAIN Info: ID = " + id + " check = " + str(check) + " -- Similarities: " + str(similarities))
    else:
        message("MAIN Info: ID: " + id + " check = " + str(check) + " -- Similarities not found.")
else:
    message("Warning: " + str(id) + " -- " + str(is_id_valid(id)))
'''

nof_eid_similarities = 0
nof_luhn_similarities = 0

# TODO: better logic of input from user
# Century
min_century = 3
max_century = 6
msg = "Starting CENTURY of ID (3 or 4 for XX (1900-1999, 3 for male, 4 for female), 5 or 6 for XXI (2000-2099, 5 for male, 6 for female): "
if debug >= 3:
    min_century = integerbox(msg, lowerbound = min_century, upperbound = max_century)
elif debug:
    min_century = sanitised_input(msg, int, min_century, max_century)

msg = "Ending CENTURY of ID (" + str(min_century) + "-" + str(max_century) + "): "
if debug >= 3:
    max_century = integerbox(msg, lowerbound = min_century, upperbound = max_century)
elif debug:
    max_century = sanitised_input(msg, int, min_century, max_century)

if min_century > max_century:
    # Swap variables
    min_century, max_century = max_century, min_century

# Year
min_year = 0
max_year = 99
msg = "Starting YEAR (two-digit, yy) of ID (" + str(min_year) + "-" + str(max_year) + "): "
if debug >= 3:
    min_year = integerbox(msg, lowerbound = min_year, upperbound = max_year)
elif debug:
    min_year = sanitised_input(msg, int, min_year, max_year)

msg = "Ending YEAR of ID (two-digit, " + str(min_year) + "-" + str(max_year) + "): "
if debug >= 3:
    max_year = integerbox(msg, lowerbound = min_year, upperbound = max_year)
elif debug:
    max_year = sanitised_input(msg, int, min_year, max_year)

if min_year > max_year:
    # Swap variables
    min_year, max_year = max_year, min_year

# Month
min_month = 1
max_month = 12
msg = "Starting MONTH of ID (" + str(min_month) + "-" + str(max_month) + "): "
if debug >= 3:
    min_month = integerbox(msg, lowerbound = min_month, upperbound = max_month)
elif debug:
    min_month = sanitised_input(msg, int, min_month, max_month)

msg = "Ending MONTH of ID (" + str(min_month) + "-" + str(max_month) + "): "
if debug >= 3:
    max_month = integerbox(msg, lowerbound = min_month, upperbound = max_month)
elif debug:
    max_month = sanitised_input(msg, int, min_month, max_month)

if min_month > max_month:
    # Swap variables
    min_month, max_month = max_month, min_month

# Day
min_day = 1
max_day = 31
msg = "Starting DAY of ID (" + str(min_day) + "-" + str(max_day) + "): "
if debug >= 3:
    min_day = integerbox(msg, lowerbound = min_day, upperbound = max_day)
elif debug:
    min_day = sanitised_input(msg, int, min_month, max_day)

msg = "Ending DAY of ID (" + str(min_day) + "-" + str(max_day) + "): "
if debug >= 3:
    max_day = integerbox(msg, lowerbound = min_day, upperbound = max_day)
elif debug:
    max_day = sanitised_input(msg, int, min_day, max_day)

if min_day > max_day:
    # Swap variables
    min_day, max_day = max_day, min_day

# Sequence
min_sequence = 0
max_sequence = 999
msg = "Starting SEQUENCE of ID (" + str(min_sequence) + "-" + str(max_sequence) + "): "
if debug >= 3:
    min_sequence = integerbox(msg, lowerbound = min_sequence, upperbound = max_sequence)
elif debug:
    min_sequence = sanitised_input(msg, int, min_sequence, max_sequence)

msg = "Ending SEQUENCE of ID (" + str(min_sequence) + "-" + str(max_sequence) + "): "
if debug >= 3:
    max_sequence = integerbox(msg, lowerbound = min_sequence, upperbound = max_sequence)
elif debug:
    max_sequence = sanitised_input(msg, int, min_sequence, max_sequence)

if min_sequence > max_sequence:
    # Swap variables
    min_sequence, max_sequence = max_sequence, min_sequence

id_min = str(min_century) + str(min_year).zfill(2) + str(min_month).zfill(2) + str(min_day).zfill(2) + str(min_sequence).zfill(3)
id_max = str(max_century) + str(max_year).zfill(2) + str(max_month).zfill(2) + str(max_day).zfill(2) + str(max_sequence).zfill(3)
message("Info: Similarities of ID-s to find: from " + id_min + " to " + id_max)

nof_id = (max_century - min_century + 1) \
         * (max_year - min_year + 1) \
         * (max_month - min_month + 1) \
         * (max_day - min_day + 1) \
         * (max_sequence - min_sequence + 1)
msg = "Warning: number of ID-s to be calculated is at least " + group(nof_id) + ". It might take a looooooong time."
if nof_id > 10000:
    if debug:
        message(msg)
    else:
        # Ensure the message is printed into console even if debug level is not set
        print(msg)
    if not query_yes_no("Are you sure to continue? "):
        sys.exit("OK, exiting.")

print("Calculating ...")
for century in range (min_century, max_century + 1): # (3, 7):
    # message("Info: Century = " + str(century))
    for year in range (min_year, max_year + 1): # (1, 100):
        # Calculate year as YYYY according to century
        yyyy = (17 + (century + 1) // 2) * 100 + year
        for month in range (min_month, max_month + 1): # (1, 13):
            for day in range (min_day, max_day + 1): # (1, 32):
                if is_date_valid (yyyy, month, day):
                    message("Info: Valid date: " + str(day) + "." + str(month) + "." + str(yyyy))
                    for sequence in range (min_sequence, max_sequence + 1): # (0, 1000):
                        id10 = str(century) + str(year).zfill(2) + str(month).zfill(2) + str(day).zfill(2) + str(sequence).zfill(3)
                        
                        # EID - Estonian ID (Eesti isikukood)
                        check_eid = calc_id_check(str(id10))
                        eid = str(id10) + str(check_eid)
                        similarities_eid = find_similar(eid, check_eid)
                        if similarities_eid:
                            # TODO: sort and collect similarities to avoid duplicate similarities found
                            # similarities_eid.append(eid).sort()
                            message("Info: EID: " + str(eid) + " -- Similarities: " + str(similarities_eid))
                            nof_eid_similarities += 1
                        else:
                            message("Info: EID: " + str(eid) + " -- Similarities not found.")
                        
                        # LUHN = Luhn ID (check digit according to Luhn algorithm)
                        check_luhn = luhn_checksum(str(id10))
                        luhn = str(id10) + str(check_luhn)
                        similarities_luhn = find_similar(luhn, check_luhn)
                        if similarities_luhn:
                            # TODO: sort and collect similarities to avoid duplicate similarities found
                            # similarities_luhn.append(luhn).sort()
                            message("Info: LUHN: " + str(luhn) + " -- Similarities: " + str(similarities_luhn))
                            nof_luhn_similarities += 1
                        else:
                            message("Info: LUHN: " + str(luhn) + " -- Similarities not found.")
                else:
                    message("Info: Date is not valid: " + str(day) + "." + str(month) + "." + str(year))
            message("Info: End of month: " + str(month))
        message("Info: End of year: " + str(year))
    message("Info: End of century: " + str(century))
message("Info: END")

print ("EID: found " + str(nof_eid_similarities) + " similarities")
print ("LUHN: found " + str(nof_luhn_similarities) + " similarities")

