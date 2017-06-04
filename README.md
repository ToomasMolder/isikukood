# isikukood
Stuff around Estonian ID (Eesti isikukood), scripts in Python

In Estonia, a Personal Identification Code (Estonian: isikukood (IK)) is defined as a number formed on the basis of the 
sex and date of birth of a person which allows the identification of the person and used by government and other systems
where identification is required, as well as by digital signatures using the nation ID-card and its associated certificates. 
An Estonian Personal identification code consists of 11 digits, generally given without any whitespace or other delimiters. 
The form is GYYMMDDSSSC, where G shows sex and century of birth (odd number male, even number female, 1-2 19th century, 
3-4 20th century, 5-6 21st century), SSS is a serial number separating persons born on the same date and C a checksum.

Main program: [isikukood.py](isikukood.py)

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
    # 1 = echo user input (useful when output is redirected into file, Linux)
    # 2 = Warnings as well
    # 3 = Info
    # 4 = GUI
    # 5 = ... (for future use)

To use os.environ['DEBUG'] = '4' # GUI, [easygui.py](easygui.py) is required in running directory, original source: http://easygui.sourceforge.net/

The most complicated part is 5 - Find, how many similarities in ID (isikukood) is available when using check digit calculation algorithm
   according to [article in Wikipedia about Estonian ID](https://et.wikipedia.org/wiki/Isikukood)

According to user input, calculations might take a looooooong time (many hours or even couple of days). Warning is displayed and cancel of script is possible.

Some sample result files are added into repository (sample_gyymmdd000-gyymmdd999_similarities_id.json)

User input can be given in form of:

    cat sample_input.txt | python3 isikukood.py

Additionally, standard output can be redirected into file and script can be run as background process:

    cat sample_input.txt | python3 isikukood.py > sample_output.txt &

Sample input: [sample_input.txt](sample_input.txt)

Sample output: [sample_output.txt](sample_output.txt)

Extracts from results with different G (century): [isikukood_getmaxlen.md](isikukood_getmaxlen.md)

Author: Toomas Mölder <toomas.molder@gmail.com>, +372 5522000  

NB! Might be buggy and crappy, written for own purposes  
NB! Global configuration signature is not checked. Use this program at your own risk.  

TODO: implement different algorithms (Luhn, Luhn mod N, Verhoeff, Damm) to calculate check digit of ID and find their level of goodness (percentage of possible similarities).
