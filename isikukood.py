# Find, how many similarities in ID (isikukood) is available when using check digit calculation algorithm
#    according to Estionian ID https://et.wikipedia.org/wiki/Isikukood
##    
##   and according to Luhn algorithm https://en.wikipedia.org/wiki/Luhn_algorithm
# 
# Author: Toomas Mölder <toomas.molder@gmail.com>, +372 5522000
# Last modified: 2017-05-23
#
# NB! Might be buggy and crappy, written for own purposes
# NB! Global configuration signature is not checked. Use this program at your own risk.
# TODO: better logic of input from user
# TODO: rewrite similarities algorithm to find possible wrong keypresses on keyboard

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
# 1 = Warnings as well
# 2 = Info
# 3 = GUI
# 4 = ... (for future use)
#
os.environ['DEBUG'] = '1'

def message(msg):
    debug = int(os.environ['DEBUG'])
    if debug >=3:
        # Do it with easygui
        msgbox(msg)
    else:
        # NB! msg MUST include keywords 'Info' or 'Warning' or 'Error' to be printed out
        if (("Info" in msg and debug >= 2) or
            ("Warning" in msg and debug >= 1) or
            ("Error" in msg and debug >= 0)):
            print(msg)
            # sys.stdout.flush()
    return

# Source: http://stackoverflow.com/questions/23294658/asking-the-user-for-input-until-they-give-a-valid-response
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

# Source: http://stackoverflow.com/questions/3041986/apt-command-line-interface-like-yes-no-input
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
def ask_start_end(msg, min, max):
    debug = int(os.environ['DEBUG'])
    message = "Starting " + msg.upper() + " of ID (" + str(min) + "-" + str(max) + "): "
    if debug >= 3:
        start = integerbox(message, lowerbound = min, upperbound = max)
    elif debug:
        start = sanitised_input(message, int, min, max)

    # Use already given by user START here instead of function input MIN
    message = "Ending " + msg.upper() + " of ID (" + str(start) + "-" + str(max) + "): "
    if debug >= 3:
        end = integerbox(message, lowerbound = start, upperbound = max)
    elif debug:
        end = sanitised_input(message, int, start, max)

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

# Check length of ID, return True/False
def is_id_len(id):
    debug = int(os.environ['DEBUG'])
    length = 11
    if debug >= 2:
        message("(" + inspect.stack()[0][3] + ") " + "Info: " + "ID " + id + " length = " + str(len(id)))
    if len(id) == length:
        return True
    else:
        if debug >= 1:
            message("(" + inspect.stack()[0][3] + ") " + "Warning: " + "ID " + id + " length = " + str(len(id)) + " is not " + str(length))
        return False

# Check that ID includes only digits, return True/False
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

# Check that first digit of ID (century) is within given range min_century and max_century, return True/False
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
    ''' else:
        if debug >= 1:
            message("(" + inspect.stack()[0][3] + ") " + "Warning: " + "ID " + id + " century = " + str(id[0]))
        return False''' 

# Check that date is valid date, return True/False
# Source: http://stackoverflow.com/questions/9987818/in-python-how-to-check-if-a-date-is-valid
def is_date_valid(year, month, day):
    debug = int(os.environ['DEBUG'])
    if debug >= 2:
        message("(" + inspect.stack()[0][3] + ") " + "Info: Is Date Valid = " + str(year) + "-" + str(month) + "-" + str(day))
    this_date = '%d/%d/%d' % (month, day, year)
    try:
        time.strptime(this_date, '%m/%d/%Y')
    except ValueError:
        '''if debug:
            message("(" + inspect.stack()[0][3] + ") " + "Error: Is Date Valid = " + str(year) + "-" + str(month) + "-" + str(day))'''
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
            '''message("(" + inspect.stack()[0][3] + ") " + "Warning: Date: Century = " + str(century) +
                    " Year (yy) = " + str(yy) +
                    " Year (yyyy) = " + str(yyyy) +
                    " Month = " + str(mm) +
                    " Day = " + str(dd))
                    '''
        return False

# Check that check digit in 11th position of Estonian ID is valid, return True/False
# Use def calc_id_check
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

# Basic check of Estonian ID validity
def is_id_valid(id):
    return (is_id_len(id) and
            is_id_digit(id) and
            is_id_century(id) and
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
def find_similar(id, check, algorithm='eid'):
    debug = int(os.environ['DEBUG'])
    # TODO: find 'neighbour' keypresses
    # keyboard = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]
    # keyboard_shift_left = [1, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    # keyboard_shift_right = [2, 3, 4, 5, 6, 7, 8, 9, 0, 0]
    #
    # TODO 2: find occasional swaps of digits, ie keypresses '2' and '1' instead of '1' and '2'
    similarities = []
    # Consider ID as list
    id_as_list = list(id)
    # Cycle over all digits in ID, but not the last digit (check digit)
    # Limit manually range (0, 1) or other similar to find possible errors only in few digits, probably makes overall process also much faster ...
    for i in range(0, len(id_as_list) - 1):
        tmp = copy.deepcopy(id_as_list)
        # tmp[i] = keyboard_shift_left[keyboard.index(id_as_list[i])]
        # Element must be > 0, only then we calculate smaller
        if int(id_as_list[i]) > 0:
            tmp[i] = str(int(id_as_list[i]) - 1)
            message("(" + inspect.stack()[0][3] + ") " + "Info: id_as_list[" + str(i) + "] = " + id_as_list[i] + " / tmp[" + str(i) + "] = " + tmp[i])
            smaller = ''.join(tmp)
            message("(" + inspect.stack()[0][3] + ") " + "Info: Smaller = " + smaller)
            smaller_check = None
            if is_id_century(smaller) and is_id_date(smaller):
                if algorithm == "eid":
                    smaller_check = calc_id_check(smaller[:10])
                elif algorithm == "luhn":
                    smaller_check = luhn_checksum(smaller[:10])
                else:
                    message("(" + inspect.stack()[0][3] + ") " + "Error: no method to calculate (smaller) cheksum")
            if smaller_check == check:
                message("(" + inspect.stack()[0][3] + ") " + "*** Info: ID " + id + " smaller similar: " + smaller)
                similarities.append(smaller)
                
        # tmp[i] = keyboard_shift_right[keyboard.index(int(id_as_list[i]))]
        # Element must be < 9, only then we calculate bigger
        if int(id_as_list[i]) < 9:
            tmp[i] = str(int(id_as_list[i]) + 1)
            message("(" + inspect.stack()[0][3] + ") " + "Info: id_as_list[" + str(i) + "] = " + id_as_list[i] + " / tmp[" + str(i) + "] = " + tmp[i])
            bigger = ''.join(tmp)
            message("(" + inspect.stack()[0][3] + ") " + "Info: Bigger = " + bigger)
            bigger_check = None
            if is_id_century(bigger) and is_id_date(bigger):
                if algorithm == "eid":
                    bigger_check = calc_id_check(bigger[:10])
                elif algorithm == "luhn":
                    bigger_check = luhn_checksum(bigger[:10])
                else:
                   message("(" + inspect.stack()[0][3] + ") " + "Error: no method to calculate (bigger) cheksum")
            if bigger_check == check:
                message("(" + inspect.stack()[0][3] + ") " + "*** Info: ID " + id + " bigger similar: " + bigger)
                similarities.append(bigger)
        # END FOR

    return similarities

###
# MAIN
###

# NB! We assume that ID, its beginning and all elements, incl check are strings
# When needed, then transform into int or list or whatever you need but transform into string back later
#
debug = int(os.environ['DEBUG'])

# Keep return from find_similarities in dictionary
eid_similarities = {}
luhn_similarities = {}
nof_eid_similarities = 0 # len(eid_similarities)
nof_luhn_similarities = 0 # len(luhn_similarities)

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
    # EID - Estonian ID (Eesti isikukood)
    check_eid = calc_id_check(id)
    # compile together first 10 digits of ID and Estonian-specific check_eid
    eid = str(id) + str(check_eid)
    tmp = find_similar(eid, check_eid, "eid")
    if tmp:
        eid_similarities[eid] = sorted(tmp)
        message("Info: EID: " + "eid_similarities[" + str(eid) + "] = " + str(eid_similarities[eid])) 
    else:
        message("Info: EID: " + str(eid) + " -- Similarities not found.")

'''
'''
# TODO: better logic of input from user
# Century
message("CENTURY of ID is 3 or 4 for XX century (born 1900-1999, 3 for male, 4 for female); 5 or 6 for XXI century (born 2000-2099, 5 for male, 6 for female)")
min_century = 3
max_century = 6
min_century, max_century = ask_start_end("century", min_century, max_century)

# Year
min_year = 0
max_year = 99
min_year, max_year = ask_start_end("year", min_year, max_year)

# Month
min_month = 1
max_month = 12
min_month, max_month = ask_start_end("month", min_month, max_month)

# Day
min_day = 1
max_day = 31
min_day, max_day = ask_start_end("day", min_day, max_day)

# Sequence
min_sequence = 0
max_sequence = 999
min_sequence, max_sequence = ask_start_end("sequence", min_sequence, max_sequence)
'''

# Random century/date
min_century = max_century = random.randint(3, 6)
min_year = max_year = random.randint(0, 99)
min_month = max_month = random.randint(1, 12)
min_day = max_day = random.randint(1, 31)
min_sequence = 0
max_sequence = 999

start_time = time.time()

id_min = str(min_century) + str(min_year).zfill(2) + str(min_month).zfill(2) + str(min_day).zfill(2) + str(min_sequence).zfill(3)
id_max = str(max_century) + str(max_year).zfill(2) + str(max_month).zfill(2) + str(max_day).zfill(2) + str(max_sequence).zfill(3)
message("Info: Similarities of ID-s to find: from " + id_min + " to " + id_max)

nof_id = (max_century - min_century + 1) \
         * (max_year - min_year + 1) \
         * (max_month - min_month + 1) \
         * (max_day - min_day + 1) \
         * (max_sequence - min_sequence + 1)
# Every 1000 IDs calculation takes appr 100 seconds
estimated_time_seconds = int(nof_id * 100 / 1000)
# Idea source: https://stackoverflow.com/questions/775049/python-time-seconds-to-hms
m, s = divmod(estimated_time_seconds, 60)
h, m = divmod(m, 60)
d, h = divmod(h, 24)
msg = "Warning: number of ID-s to be calculated is at least " + group(nof_id) + ". It might take a looooooong time (" + "%d days %d hrs : %d min : %d sec" % (d, h, m, s) + ")"
if nof_id > 1000:
    if debug:
        message(msg)
    else:
        # Ensure the message is printed into console even if debug level is not set
        print(msg)
    if not query_yes_no("Are you sure to continue? "):
        sys.exit("OK, exiting.")

print("Calculating ...")
for century in range (min_century, max_century + 1): # (3, 7):
    print("Info: Century = " + str(century))
    for year in range (min_year, max_year + 1): # (1, 100):
        print("Info: Year = " + str(year))
        # Calculate year as YYYY according to century
        yyyy = (17 + (century + 1) // 2) * 100 + year
        for month in range (min_month, max_month + 1): # (1, 13):
            print("Info: Month = " + str(month))
            for day in range (min_day, max_day + 1): # (1, 32):
                print("Info: Day = " + str(day))
                if is_date_valid (yyyy, month, day):
                    message("Info: Valid date: " + str(day) + "." + str(month) + "." + str(yyyy))
                    for sequence in range (min_sequence, max_sequence + 1): # (0, 1000):
                        # print("Info: Sequence = " + str(sequence))
                        # Print progress bar ...
                        if not sequence % 10:
                            print(".", end = "")
                        
                        # Create 10-digit length ID, without check digit
                        id10 = str(century) + str(year).zfill(2) + str(month).zfill(2) + str(day).zfill(2) + str(sequence).zfill(3)
                        
                        # EID - Estonian ID (Eesti isikukood)
                        check_eid = calc_id_check(str(id10))
                        # compile together first 10 digits of ID and Estonian-specific check_eid
                        eid = str(id10) + str(check_eid)
                        tmp = find_similar(eid, check_eid, "eid")
                        if tmp:
                            eid_similarities[eid] = sorted(tmp)
                            message("Info: EID: " + "eid_similarities[" + str(eid) + "] = " + str(eid_similarities[eid])) 
                            nof_eid_similarities += 1
                        else:
                            message("Info: EID: " + str(eid) + " -- Similarities not found.")
                        
                        '''# LUHN = Luhn ID (check digit according to Luhn algorithm)
                        check_luhn = luhn_checksum(str(id10))
                        # compile together first 10 digits of ID and Estonian-specific check_eid
                        luhn = str(id10) + str(check_luhn)
                        tmp = find_similar(luhn, check_luhn, "luhn")
                        if tmp:
                            luhn_similarities[luhn] = sorted(tmp)
                            print("Info: LUHN: " + "luhn_similarities[" + str(luhn) + "] = " + str(luhn_similarities[luhn]))
                            nof_luhn_similarities += 1
                        else:
                            message("Info: LUHN: " + str(luhn) + " -- Similarities not found.")'''
                else:
                    message("Info: Date is not valid: " + str(day) + "." + str(month) + "." + str(year))
            print("\nInfo: End of month: " + str(month))
        print("Info: End of year: " + str(year))
    print("Info: End of century: " + str(century))
print("Info: END")

print ("EID: found " + str(nof_eid_similarities) + " similarities")
print("Info: write file: " + id_min + "-" + id_max + "_similarities_eid.json")
with open(id_min + "-" + id_max + "_similarities_eid.json", 'w') as fp:
    json.dump(eid_similarities, fp, indent = 4)
# f = open(id_min + "-" + id_max + "_similarities_eid.txt", "w")
# f.write(str(eid_similarities))
# f.close()

'''
print ("LUHN: found " + str(nof_luhn_similarities) + " similarities")
print("Info: write file: " + id_min + "-" + id_max + "_similarities_luhn.json")
with open(id_min + "-" + id_max + "_similarities_luhn.json", 'w') as fp:
    json.dump(luhn_similarities, fp, indent = 4)
# f = open(id_min + "-" + id_max + "_similarities_luhn.txt", "w")
# f.write(str(luhn_similarities))
# f.close()
'''

if start_time:
    print("--- %s seconds ---" % (time.time() - start_time))

