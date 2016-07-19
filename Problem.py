'''
Created on Jul 28, 2016
Encapsulates a single problem

@author: Manujinda Wathugala
'''
import ConfigParser
import os
import sys


class Problem( object ):
    """
        A class to represent a single problem or a Homework
    """

    def __init__( self, no ):
        self._01_prob_no = no
        self._02_name = 'Problem name'
        self._03_prob_desc = 'Problem description'
        self._04_files_provided = []
        self._05_files_submitted = []

        # A dictionary that maps sandbox inputs to anticipated outputs
        # both inputs and outputs are stored in files. So the dictionary
        # has the form input file --> output file.
        #
        # !!! need more thought as to how to handle different kinds of
        # inputs such as: command line arguments, inputs read by the program
        # using a prompt, file inputs etc.
        self._06_inp_outps = {}

        self._07_language = ''
        self._08_command_line_options = False
        self._09_student_make_file = False
        self._10_make_targs = []
        self._11_scores = []

        # Timeout interval to decide infinite loop
        # -1 means do not timeout
        self._12_timeout = -1

    def __str__( self ):
        desc = ''
        for f in sorted( self.__dict__.keys() ):
            desc += '{} > {} \n'.format( f[4:], self.__dict__[f] )
        return desc
        # return '{} {}'.format( self._01_prob_no, self._02_name )

    '''
    Read problem configuration file and populate the instance variables
    '''
    def setup_problem( self, config_file, section ):

        # Check whether the project configuration file exists.
        if not os.path.exists( config_file ):
            print '\nProblem configuration file {} does not exist, exit...'.format( config_file )
            sys.exit()

        config = ConfigParser.SafeConfigParser()
        config.read( config_file )

        for key in sorted( self.__dict__.keys() ):
            self.__dict__[key] = config.get( section, key ).strip()

        print self
        return True



    def get_files_provided( self ):
        return self._04_files_provided


    def get_files_submitted( self ):
        return self._05_files_submitted
