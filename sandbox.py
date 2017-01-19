'''
Created on Jul 11, 2016

@author: Manujinda Wathugala

This is where I test new code, try out new stuff and learn new things before adding them to the main files.
This chages rapidly. Not a part of the main project. This is just my playground :)
'''

# Generating Gradebook
import ConfigParser
from collections import OrderedDict
import csv
from datetime import datetime, timedelta
from difflib import HtmlDiff
from difflib import SequenceMatcher
import os
import pprint
import re
import sys

from AgGlobals import AgGlobals
from Assignment import Assignment
from Command import Command
from Repository import Repository
from diff_match_patch import diff_match_patch


# Playing with adding random seed.
c_file = open( 'sticks_sol.c', 'r' )
lines = c_file.readlines()
c_file.close()

stdlib_found = False
for l in lines:
    if '#include' in l:
        if '<stdlib.h>' in l:
            stdlib_found = True
            print 'lib found'

if not stdlib_found:
    for i in range( len( lines ) ):
        if '#include' in lines[i]:
            lines.insert( i, '#include <stdlib.h>\r\n' )
            break

for i in range( len( lines ) ):
    if 'srand' in lines[i]:
        lines[i] = 'srand(1)\r\n'
        break


line = 'abc srand(time(NULL)); def srand(34); aaaaa srand(4);'
line = 'aaa srand(time(NULL)); def srand(34); aaaa srand(3);\n adfdsf );'
# line = 'aaa bbb aaa bbb aaa ccc'
print line
regex = re.compile( "srand\s*\(.*?\)\s*;" )
# regex = re.compile( "aaa" )
# line = regex.sub( 'srand(3);', line )
# print re.findall( r"srand\s*\(.*\)\s*;", line )
# line = re.sub( r"srand\s*\(.*\)\s*;", 'srand(3);', line )
line = regex.sub( 'srand(3);', line )
print line
# for line in some_file:
#     line = regex.sub( "interfaceOpDataFile %s" % fileIn, line )
# print lines

# print lines
print 'open'

c_file = open( 'sticks_sol.c', 'wb' )
c_file.writelines( lines )
c_file.close()


exit()



# Playing with data and time
dt = datetime.strptime( '01/03/2017::16:00', '%m/%d/%Y::%H:%M' )
now = datetime.now()

print dt
print dt + timedelta( minutes = 30 )
print now

if now > dt + timedelta( 30 ):
    print 'grater'
else:
    print 'lesser'
exit()



# Checking the current directory of a python script

print os.getcwd()

print __file__

print os.path.realpath( __file__ )

print( os.path.dirname( os.path.realpath( __file__ ) ) )

print sys.path[0]


exit()

# Playing with sets to get all the dependencies of a problem

a = set( [5] )

if a:
    print 'not empty'
else:
    print 'empty'

get_dependencies = {5:[4], 4:[3, 2], 3:[1], 2:[], 1:[]}

search_dependencis_for = set( [5] )
dept_probs = []

while search_dependencis_for:
    p = search_dependencis_for.pop()
    if p not in dept_probs:
        dept_probs.append( p )
        deps = get_dependencies[p]

        for d in deps:
            if d not in dept_probs:
                search_dependencis_for.add( d )

print dept_probs
exit()

# Playing with ordered dictionary

od = OrderedDict()

od[5] = 'abc'
od[2] = 'def'
od[4] = 'ghi'
od[7] = 'jkl'

print od[next( reversed( od ) )]
print od
exit()


# Manupulating date time
dt = datetime.now()


print dt.strftime( '%m - %d - %Y :: ' )
print dt.strftime( '%x %X' )
exit()


# Hacking difflib
# stud = '1**2*'
# our = '1*2'
our = "*\n**\n***\n****\n"
stud = "      *\n    * *\n  * * *\n* * * *\n"

space_match = 36


s = SequenceMatcher( lambda x: x == " ", stud, our )

def_ratio = s.ratio()
comb_len = len( stud ) + len( our )
def_match = def_ratio * comb_len
new_match = def_match + space_match
new_ratio = new_match / comb_len
print "space match : ", space_match
print "old ratio : ", def_ratio
print "new ratio : ", new_ratio

print our
print stud
# exit()

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

diffs = dmp.diff_main( lines_stud, lines_ref )
of.write( dmp.diff_prettyHtml( diffs ) )
of.close()

dmp.diff_cleanupSemantic( diffs )

for ( flag, data ) in diffs:
    if ( data != ' ' ):
        print flag, data
    else:
        print 'space'


sm = SequenceMatcher( isjunk = lambda x: x in ' 58\n', a = lines_stud, b = lines_ref )

for tag, i1, i2, j1, j2 in sm.get_opcodes():
    print ( '{:>7} a[{}:{}] ({}) b[{}:{}] ({})'.format( tag, i1, i2, lines_stud[i1:i2], j1, j2, lines_ref[j1:j2] ) )

for block in sm.get_matching_blocks():
    print block

print 'ratio: ', sm.ratio()

print dmp.diff_levenshtein( diffs )

print SequenceMatcher( None, " abcd", "abcd abcd" ).ratio()

stud = "12344"
our = "12345"

# stud = "private Thread currentThread;"
# our = "private volatile Thread currentThread;"

# stud = "*\n* *\n* * *\n* * * *\n"
# our = "*\n**\n***\n****\n"
#
stud = "   *\n  **\n ***\n****\n"
# stud = "   *\n   **\n   ***\n   ****\n"
# stud = "*\n**\n***\n****\n"
our = "      *\n    * *\n  * * *\n* * * *\n"

# stud = "      *\n    *   *\n  *   *   *\n*   *   *  *\n"
# our = "   *\n  * *\n * * *\n* * * *\n"


#   def diff_levenshtein( self, diffs ):
#     """Compute the Levenshtein distance; the number of inserted, deleted or
#     substituted characters.


# s = SequenceMatcher( lambda x: x == " ",
#                     "private Thread currentThread;",
#                     "private volatile Thread currentThread;" )

s = SequenceMatcher( lambda x: x == " ", stud, our )

print round( s.ratio(), 3 )

for block in s.get_matching_blocks():
    print "a[%d] and b[%d] match for %d elements" % block

for op, a_start, a_end, b_start, b_end in s.get_opcodes():
    # print "%6s a[%d:%d] b[%d:%d]" % opcode
    # print opcode
    print op, stud[a_start:a_end], our[b_start:b_end]


def create_diff_html( old_txt, new_txt, changes, ignore_spaces = False ):
    html = []
    html.append( "<pre>" )

    space_match = 0
    # tot_elms = 0

    for op, ob, oe, nb, ne in changes.get_opcodes():

        ot = old_txt[ob:oe].replace( "&", "&amp;" ).replace( "<", "&lt;" ).replace( ">", "&gt;" ).replace( "\n", "&para;<br>" )
        nt = new_txt[nb:ne].replace( "&", "&amp;" ).replace( "<", "&lt;" ).replace( ">", "&gt;" ).replace( "\n", "&para;<br>" )

        # tot_elms += 1

        if op == 'insert':
            if ( nt.strip() or not ignore_spaces ):
                html.append( "<ins style=\"background:#e6ffe6;\">{}</ins>".format( nt ) )
            else:
                space_match += len( nt )
        elif op == 'delete':
            if ( ot.strip() or not ignore_spaces ):
                html.append( "<del style=\"background:#ffe6e6;\">{}</del>".format( ot ) )
            else:
                html.append( "<span>{}</span>".format( ot ) )
                space_match += len( ot )
        elif op == 'replace':
            html.append( "<del style=\"background:#ffe6e6;\">{}</del>".format( ot ) )
            html.append( "<ins style=\"background:#e6ffe6;\">{}</ins>".format( nt ) )
            # tot_elms += 1
        elif op == 'equal':
            html.append( "<span>{}</span>".format( ot ) )
            # tot_elms += 1

    html.append( "</pre>" )
    def_ratio = changes.ratio()
    comb_len = len( old_txt ) + len( new_txt )
    def_match = def_ratio * comb_len
    new_match = def_match + space_match
    new_ratio = new_match / comb_len
    print "space match : ", space_match
    # print 'tot elms : ', tot_elms
    print "old ratio : ", def_ratio
    print "new ratio : ", new_ratio
    return "".join( html )



of = open( 'my_diff.html', 'w+' )
of.write( create_diff_html( stud, our, s, False ) )
of.close()

print
print create_diff_html( stud, our, s, True )

# diffs = dmp.diff_main( "private Thread currentThread;",
#                     "private volatile Thread currentThread;" )
diffs = dmp.diff_main( stud, our )

# for ( flag, data ) in diffs:
#    print flag, data

print our
print stud
sys.exit()




# Dictionary sorting

d = {0:34.0, 10:50, 80:100, 'compile':5, 'compwarn':4, 'link':6, 'linkwarn':8}

print sorted( d, reverse = True )

e = {t:d[t] if isinstance( t, int ) else None for t in d}

print e

d2 = {}
for t in d:
    if isinstance( t, int ):
        d2[t] = d[t]

print d2
exit()






# Dictionary to CSV file writing
my_dict = {"x": 2, "a": 1}

with open( 'mycsvfile.csv', 'wb' ) as f:  # Just use 'w' mode in 3.x
    w = csv.DictWriter( f, ['x', 'a'] )
    w.writeheader()
    w.writerow( my_dict )

exit()

asmnt = Assignment()

asmnt.load_assignment( \
'C:\Users\manujinda\Documents\Manujinda\UOregon\Classes\\4_2016_Summer\Boyana\grading', \
'assignments', 'assignment_2' )

asmnt.load_problems()

headers = asmnt.generate_gradebook_headers()

print headers

asmnt_master_sub_dir = asmnt.get_masterdir()
log_directory_path = os.path.join( asmnt_master_sub_dir, AgGlobals.LOG_FILE_DIRECTORY )
gradebook = open( os.path.join( log_directory_path, 'gradebook.csv' ), 'w' )
AgGlobals.write_to_log( gradebook, 'Assignment 2 Marks\n' )
AgGlobals.write_to_log( gradebook, headers[0] )
AgGlobals.write_to_log( gradebook, headers[1] )

gradebook.close()

exit()




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

