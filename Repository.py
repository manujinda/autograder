'''
Created on Jul 6, 2016
A class to encapsulate a version control repository such as Git

@author: manujinda
'''

class Repository( object ):
    '''
    classdocs
    '''


    def __init__( self, repo ):
        '''
        Constructor
        '''
        self.uri = repo

    def __str__( self ):
        return self.uri
