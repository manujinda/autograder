'''
Created on Jul 4, 2016
Encapsulates a single student

@author: Manujinda Wathugala
'''

from AgGlobals import AgGlobals
from Repository import Repository


class Student( object ):
    '''
    classdocs
    '''


    def __init__( self, data_dict ):
        '''
        Constructor
        '''
        self._1_no = data_dict[ AgGlobals.STUDENT_DB_FIED_NO ]
        self._2_uoid = data_dict[ AgGlobals.STUDENT_DB_FIED_UOID ]
        self._3_duckid = data_dict[ AgGlobals.STUDENT_DB_FIED_DUCKID ]
        self._4_last_name = data_dict[ AgGlobals.STUDENT_DB_FIED_LNAME ]
        self._5_first_name = data_dict[ AgGlobals.STUDENT_DB_FIED_FNAME ]
        self._6_email = data_dict[ AgGlobals.STUDENT_DB_FIED_EMAIL ]
        self._7_dirname = data_dict[ AgGlobals.STUDENT_DB_FIED_DIR_NAME ]
        self._8_repo = Repository( data_dict[ AgGlobals.STUDENT_DB_FIED_REPO ] )

    def __str__( self ):
        return AgGlobals.string_of( self, 3 )

    def get_dir( self, index_len ):
        # If index_len = 3, this creates a string of the form:
        # {:3}_{}
        # ret = '{}{}{}_{}'.format( '{:0>', index_len, '}', '{}' )

        # Use the format string created above to format the student
        # directory name appropriately
        # return ret.format( self._1_no, self._7_dirname )

        return AgGlobals.get_student_dir_name( index_len, self._1_no, self._7_dirname )

    def get_index( self ):
        return '{}'.format( self._1_no )

    def get_name( self ):
        return '{} {}'.format( self._5_first_name, self._4_last_name )

    def clone_student_repo( self, destination, grading_log_file, student_log_file ):
        return self._8_repo.clone( destination, grading_log_file, student_log_file )

    def pull_student_repo( self, local_path, grading_log_file, student_log_file ):
        self._8_repo.pull( local_path, grading_log_file, student_log_file )

    def copy_student_repo( self, source, destination, index_len ):
        self._8_repo.copy( source, destination, self.get_dir( index_len ) )

    def get_stud_log_file_name( self, index_len, assignment_sub_dir_name ):
        return AgGlobals.get_stud_log_file_name( self.get_dir( index_len ), assignment_sub_dir_name )

    def get_stud_grades_file_name( self, index_len, assignment_sub_dir_name ):
        return AgGlobals.get_stud_grades_file_name( self.get_dir( index_len ), assignment_sub_dir_name )
