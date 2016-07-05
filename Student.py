'''
Created on Jul 4, 2016

@author: manujinda
'''

class Student( object ):
    '''
    classdocs
    '''


    def __init__( self, data_dict ):
        '''
        Constructor
        '''
        self._1_no = data_dict['No']
        self._2_uoid = data_dict['UO ID']
        self._3_duckid = data_dict['Duck ID']
        self._4_last_name = data_dict['Last Name']
        self._5_first_name = data_dict['First Name']
        self._6_email = data_dict['Email']
        self._7_dirname = data_dict['Dir Name']
        self._8_git_repo = data_dict['Git Repo']

    def __str__( self ):
        desc = ''
        for f in sorted( self.__dict__.keys() ):
            desc += '{} > {} \n'.format( f[3:], self.__dict__[f] )
        return desc

    def get_dir( self ):
        return self._7_dirname

    def get_name( self ):
        return '{} {}'.format( self._5_first_name, self._4_last_name )

