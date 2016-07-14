'''
Created on Jul 4, 2016
Encapsulates a single student

@author: Manujinda Wathugala
'''

from Repository import Repository

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
        self._8_repo = Repository( data_dict['Repo'] )

    def __str__( self ):
        desc = ''
        for f in sorted( self.__dict__.keys() ):
            desc += '{} > {} \n'.format( f[3:], self.__dict__[f] )
        return desc

    def get_dir( self, index_len ):
        # If index_len = 3, this creates a string of the form:
        # {:3}_{}
        ret = '{}{}{}_{}'.format( '{:0>', index_len, '}', '{}' )

        # Use the format string created above to format the student
        # directory name appropriately
        return ret.format( self._1_no, self._7_dirname )

    def get_index( self ):
        return '{}'.format( self._1_no )

    def get_name( self ):
        return '{} {}'.format( self._5_first_name, self._4_last_name )

    def clone_student_repo( self, destination = '' ):
        self._8_repo.clone( destination )

    def pull_student_repo( self, local_path = '' ):
        self._8_repo.pull( local_path )

    def copy_student_repo( self, source, destination, student ):
        self._8_repo.copy( source, destination, student )

