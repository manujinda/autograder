'''
Created on Jul 6, 2016
A class the encapsulate the environment which the autograder is
operating on.

@author: manujinda
'''

from os.path import expanduser
import platform


class Environment( object ):
    '''
    classdocs
    '''


    def __init__( self, params ):
        '''
        Constructor
        '''
        self.os = platform.system()
        self.home = expanduser( "~" )
