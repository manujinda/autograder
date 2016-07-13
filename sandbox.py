'''
Created on Jul 11, 2016

@author: Manujinda Wathugala

This is where I test new code, try out new stuff and learn new things before adding them to the main files.
This chages rapidly. Not a part of the main project. This is just my playground :)
'''
import ConfigParser
import sys


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

