# --------------------------------------------------------------------------------------
# File: Exercise_2.2.py
# Name: Amie Davis
# Date: 9/5/2019
# Course: DSC540 - Data Preparation
# Assignment Number: 2.2
#
# Purpose: To review Python Basics
#
# Usage: Uses Python 3.7.
#        Developed using PyCharm 2019.1.3.
#
# --------------------------------------------------------------------------------------

# Import libraries
from decimal import getcontext, Decimal

# Change case in a string
v_name = 'Amie'
print('The uppercase name is {} and the lowercase name is {}.'.format(v_name.upper(), v_name.lower()))

# Strip space off the end of a string
v_school = 'Bellevue '
str_school = v_school.strip()
print('The stripped off length of {} is {}.'.format(str_school, len(str_school)))

# Split a string
v_fullname = 'Davis, Amie'
l_name = v_fullname.split(',')
first_name = l_name[1]
last_name = l_name[0]
print('The full name is {} {}.'.format(first_name.strip(), last_name))

# Add and Subtract integers and decimals
i = 5
j = 8
isum = i + j
idiff = i - j
print('The sum of integers is {} and the difference is {}.'.format(isum, idiff))

f1 = 10.1
f2 = 32.4
fsum = f1 + f2
fdiff = f1 - f2
print('The sum of floats is {} and the difference is {}.'.format(fsum, fdiff))

getcontext().prec = 3
d1 = Decimal(10.1)
d2 = Decimal(32.4)
dsum = d1 + d2
ddiff = d1 - d2
print('The sum of decimals is {} and the difference is {}.'.format(dsum, ddiff))

# Create a list
mylist = ['peanuts','milk','soda','cheese','bread']
print('The original list is {}.'.format(mylist))

# Add to the list
mylist.append('coffee')
print('The new list is {}.'.format(mylist))

# Subtract from the list
mylist.remove('soda')
print('The updated list is {}.'.format(mylist))

# Remove the last item from the list
mylist.pop()
print('The popped list is {}.'.format(mylist))

# Re-order the list
# by switching two items
mylist[0], mylist[1] = mylist[1], mylist[0]
print('The re-ordered list is {}.'.format(mylist))

# Sort the list
mylist.sort()
print('The sorted list is {}.'.format(mylist))

# Create a dictionary
mydict = {'quantity': 20, 'description': 'book', 'total': 54.15}
print('The original dictionary is {}.'.format(mydict))

# Add a key-value to the dictionary
mydict['color'] = 'blue'
print('The new dictionary is {}.'.format(mydict))

# Set a new value to corresponding key in dictionary
mydict['description'] = 'shirt'
print('The updated dictionary is {}.'.format(mydict))

# Look up a value by the key in dictionary
v_description = mydict['description']
print('The value for the description key in the dictionary is {}.'.format(v_description))
