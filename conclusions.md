# Conclusions

Reason to use algorithm modulo 11 as it is stated in Estonian standard EVS 585:2007 to calculate check digit of Estonian ID is unknown.

Algorithm (modulo 11) to calculate check digit of Estonian ID (isikukood) does NOT guarantee non-existence of human or input errors. 

Use of only 9 different weights (123456789) to calculate check digit for 10-digit ID is not enough.

At least 3 different-level weaknesses are available in implementation of Estonian ID:

1. Use of century/sex (G) and birth date (YYMMDD) in Estonian ID might reveal sensitive information about person (in opposite, it is also strength of implementation as it leaves Estonian ID to be memorable and spellable and easily checkable)
2. Structure of Estonian ID, use of area SSS is short enough to enable millions of users (10 million e-residents).
3. Algorithm to calculate check digit of Estonian ID (C) does not guarantee non-existence of human or input errors.

Note: according to reader's views there are other opinions as well about weaknesses or strengths of Estonian ID.
