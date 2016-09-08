'''
Created on Jul 11, 2016

@author: Manujinda Wathugala

This is where I test new code, try out new stuff and learn new things before adding them to the main files.
This chages rapidly. Not a part of the main project. This is just my playground :)
'''
import ConfigParser
from difflib import HtmlDiff
from difflib import SequenceMatcher
import os
import pprint
import sys

from AgGlobals import AgGlobals
from Command import Command
from Repository import Repository
from diff_match_patch import diff_match_patch


out_ref = open( 'out_ref.txt' )
out_stud = open( 'out_stud.txt' )

lines_ref = out_ref.read()
lines_stud = out_stud.read()

print lines_ref
print lines_stud

hd = HtmlDiff( tabsize = 20, wrapcolumn = 40, linejunk = lambda x: x == '5555\n', charjunk = lambda x: x == ' ' )

difference = hd.make_file( lines_stud, lines_ref )

of = open( 'difference.html', 'w+' )
of.write( difference )
of.close()

dmp = diff_match_patch()
of = open( 'difference_dmp.html', 'w+' )
of.write( dmp.diff_prettyHtml( dmp.diff_main( lines_stud, lines_ref ) ) )
of.close()

sm = SequenceMatcher( isjunk = lambda x: x in ' 58\n', a = lines_stud, b = lines_ref )

for tag, i1, i2, j1, j2 in sm.get_opcodes():
    print ( '{:>7} a[{}:{}] ({}) b[{}:{}] ({})'.format( tag, i1, i2, lines_stud[i1:i2], j1, j2, lines_ref[j1:j2] ) )

for block in sm.get_matching_blocks():
    print block

print 'ratio: ', sm.ratio()

print SequenceMatcher( None, " abcd", "abcd abcd" ).ratio()
sys.exit()

print os.path.splitext( 'abcd.edd.txt' )

inp = ( 'abc', '234', 'ef' )
print '---'.join( inp )


failCmd = 'diff -y -B -b {} {}'.format( 'out_stud.txt', 'out_ref.txt' )
ret, out, err = Command( failCmd ).run()
print 'ret: {}\nout: {}\nerr: {}\n'.format( ret, out, err )

failCmd = 'diff  -B -b {} {}'.format( 'out_stud.txt', 'out_ref.txt' )
subcmd = 'numdiffs=`' + failCmd + ' | wc -l` && echo $numdiffs'
ret, out, err = Command( subcmd ).run()
print 'ret: {}\nout: {}\nerr: {}\n'.format( ret, out, err )

# pp = pprint.PrettyPrinter( indent = 4 )
# pp.pprint( lines_ref )
# pp.pprint( lines_stud )

sys.exit()


# playing with line breaks

msg = 'abcd\ndefg\n1234'

print msg

# for line in msg.split( '\n' ):
for line in msg.splitlines():
    print line

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

print AgGlobals.clear_flags( state, comp, inp, inp )

print AgGlobals.is_flags_set( state, inp, 8 )

sys.exit( 0 )

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

