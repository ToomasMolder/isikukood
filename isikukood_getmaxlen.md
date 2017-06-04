# Some results while running isikukood.py

In Estonia, a Personal Identification Code (Estonian: isikukood (IK)) is defined as a number formed on the basis of the 
sex and date of birth of a person which allows the identification of the person and used by government and other systems
where identification is required, as well as by digital signatures using the nation ID-card and its associated certificates. 
An Estonian Personal identification code consists of 11 digits, generally given without any whitespace or other delimiters. 
The form is GYYMMDDSSSC, where G shows sex and century of birth (odd number male, even number female, 1-2 19th century, 
3-4 20th century, 5-6 21st century), SSS is a serial number separating persons born on the same date and C a checksum.

Source: https://en.wikipedia.org/wiki/National_identification_number#Estonia

## G = 3

## G = 4

    *** Result: Total number of IDs reviewed = 36.500.000
    From them number of IDs with similarities = 9.134.728 (25.0267%)
    Max number of similarities = 9 found for these IDs:
    "45601212049": ['35601212049', '45601212039', '45601212094', '45601212409', '45601221049', '45602112049', '45610212049', '46501212049', '54601212049']

## G = 5

    *** Result: Total number of IDs reviewed = 36.500.000
    From them number of IDs with similarities = 9.134.972 (25.0273%)
    Max number of similarities = 9 found for these IDs:
    "54310210950": ['45310210950', '53410210950', '54301210950', '54310120950', '54310201950', '54310210590', '54310210905', '54310210960', '64310210950']

## G = 6

    *** Result: Total number of IDs reviewed = 36.500.000
    From them number of IDs with similarities = 9.008.340 (24.6804%)
    Max number of similarities = 8 found for these IDs:
    "62301256749": ['52301256749', '62301256739', '62301256794', '62301257649', '62301265749', '62302156749', '62310256749', '63201256749']
    "63410123049": ['53410123049', '63410123039', '63410123094', '63410123409', '63410132049', '63410213049', '63411023049', '64310123049']
    "64212318691": ['46212318691', '62412318691', '64212138691', '64212316891', '64212318591', '64212318601', '64212318961', '65212318691']
    "68901123489": ['58901123489', '68901123479', '68901123849', '68901124389', '68901132489', '68901213489', '68910123489', '69801123489']
    "68901201269": ['58901201269', '68901201259', '68901201629', '68901202169', '68901210269', '68902101269', '68910201269', '69801201269']

