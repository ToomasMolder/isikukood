# isikukood
Stuff around Estonian ID (Eesti isikukood), scripts in Python

Main program: isikukood.py

Choices:

    0 = Exit  
    1 = Check ID validity  
    2 = Calculate ID check digit  
    3 = Find similar IDs of one ID  
    4 = Find similar IDs of random ID  
    5 = Find similar IDs of range of IDs  

Explanation of term 'similarities' - ID is still valid (length = 11, isdigit, date is valid, checksum is valid) even when:
- one digit value within ID is different by one (instead of correct '2' incorrect '1' or '3' was used)
- two digits within ID are swapped (instead of correct '12', it has swapped '21')

It is possible to run script with different debug level, controlled with os.environ['DEBUG']

    # 0 = Errors only
    # 1 = Warnings as well
    # 2 = Info
    # 3 = GUI
    # 4 = ... (for future use)

To use os.environ['DEBUG'] = '3' # GUI, easygui.py is required in running directory, original source: http://easygui.sourceforge.net/

The most complicated part is 5 - Find, how many similarities in ID (isikukood) is available when using check digit calculation algorithm
   according to Estonian ID https://et.wikipedia.org/wiki/Isikukood

According to user input, calculations might take a looooooong time (many hours or even couple of days). Warning is displayed and cancel of script is possible.

Some sample result files are added into repository (sample_cyymmdd000-cyymmdd999_similarities_id.json)

User input can be given in form of:

    cat sample_input.txt | python3 isikukood.py

Additionally, standard output can be redirected into file and script can be run as background process:

    cat sample_input.txt | python3 isikukood.py > sample_output.txt &

Author: Toomas Mölder <toomas.molder@gmail.com>, +372 5522000  

NB! Might be buggy and crappy, written for own purposes  
NB! Global configuration signature is not checked. Use this program at your own risk.  

TODO: better logic of input from user  
TODO: rewrite similarities algorithm to find possible wrong keypresses on keyboard  
