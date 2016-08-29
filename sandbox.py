'''
Created on Jul 11, 2016

@author: Manujinda Wathugala

This is where I test new code, try out new stuff and learn new things before adding them to the main files.
This chages rapidly. Not a part of the main project. This is just my playground :)
'''
import ConfigParser
import sys
from AgGlobals import AgGlobals

# dictionaries and sets

d = {1:set( [1, 2, 3] ), 2:set( [5, 6] )}
print d
print d[1]
current = d.get( 3, set() )
current.update( [] )
print current
# new_set = d.get( 3, set() )
# print new_set
# new_set.update( set[2, 3] )
# print new_set


sys.exit( 0 )


# Bitwise operations
x = ( 1 << 3 )
print x
y = 2
z = x | y
print z & x
w = 4
print w & z

if z & x == x:
    print 'x is set'

inp = 1
comp = 2
other = 4

state = inp | comp | other
print state
print state & ( inp | other )
print inp | other
if state & ( inp | other ) == inp | other:
    print 'good'

print AgGlobals.set_flags( 2, 4, 8 )

print AgGlobals.is_flags_set( state, inp, 8 )

sys.exit( 0 )

# Reading a text file at once
inp = open( 'sandbox.py', 'r' )
f = inp.read()
print f

sys.exit()

# Playing with parsing a : seperated string.
def parse_config_line( line ):
    parts = line.split()
    ll = []
    for p in parts:
        ll.append( p.split( ':' ) )

    return ll

print parse_config_line( '111:aaa:xxx 22:bbbbb:yy 3:ccc' )

key = '_99_loaded'
print key[0:4]

# playing with parsing input
inp = '1:prog 2:mcq 3:code'
prob = inp.split()
print prob
for p in prob:
    print p.split( ':' )

d = {1:'a', 2:'b', 3:'c'}

for i in d:
    print i

sys.exit( 0 )

# playing with output formatting

ret = '{}{}{}_{}'.format( '{:0>', 3, '}', '{}' )
print ret
print ret.format( 1, 'abc' )



sys.exit( 0 )
# Playing with repository cloning

from Repository import Repository

rep = Repository( 'https://github.com/manujinda/hello-world.git' )

print rep

rep.clone( '/home/users/manu/Documents/manujinda/uo_classes/4_2016_summer/test4' )

sys.exit( 0 )
# ConfigParser testing

config = ConfigParser.RawConfigParser()

# When adding sections or items, add them in the reverse order of
# how you want them to be displayed in the actual file.
# In addition, please note that using RawConfigParser's and the raw
# mode of ConfigParser's respective set functions, you can assign
# non-string values to keys internally, but will receive an error
# when attempting to write to a file or when you get it in non-raw
# mode. SafeConfigParser does not allow such assignments to take place.
config.add_section( 'Autograder Setup' )

# All the grading for a particular class happens within this directory.
# There is a predefined directory structure that the auto-grader uses within this directory.
path = '/home/users/manu/Documents/manujinda/uo_classes/4_2016_summer/boyana/grading'
config.set( 'Autograder Setup', 'grading_root', path )


config.set( 'Autograder Setup', 'grading_master', 'assignments' )

# Writing our configuration file to 'example.cfg'
with open( 'autograder.cfg', 'wb' ) as configfile:
    config.write( configfile )

config = ConfigParser.SafeConfigParser()
config.read( '/home/users/manu/Documents/manujinda/uo_classes/4_2016_summer/boyana/autograder_ws/autograder/autograder.cfg' )

# Set the third, optional argument of get to 1 if you wish to use raw mode.
print config.get( 'Autograder Setup', 'grading_root', 0 )  # -> "Python is fun!"
print config.get( 'Autograder Setup', 'grading_master', 1 )  # -> "%(bar)s is %(baz)s!"

