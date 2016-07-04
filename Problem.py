import csv
import os
import sys


class Problem( object ):
    """
        A class to represent a single problem or a Homework
    """

    def __init__( self, no ):
        self._01_prob_no = no
        self._02_name = 'Problem name'
        self._03_proj_desc = 'Problem description'
        self._04_files_provided = []
        self._05_files_submitted = []
        self._06_inp_outps = {}  # A dictionalry that maps test inputs to anticipated outputs
        self._07_language = ''
        self._08_command_line_options = False
        self._09_student_make_file = False
        self._10_make_targs = []
        self._11_scores = []

    def __str__( self ):
        desc = ''
        for f in sorted( self.__dict__.keys() ):
            desc += '{} > {} \n'.format( f, self.__dict__[f] )
        return desc
        # return '{} {}'.format( self._01_prob_no, self._02_name )

    def setup_problem( self, config_path ):
        # Check whether the problem configuration file exisits.
        if not os.path.exists( config_path ):
            print '\nProblem configuration file {} does not exist, exit...'.format( config_path )
            sys.exit()

        with open( config_path ) as config_file:
            reader = csv.DictReader( config_file )
            for row in reader:
                key = row['Key'].strip()
                value = row[' Value'].strip()
                if key == '_01_prob_no':
                    self._01_prob_no = int( value )
                elif key == '_02_name':
                    self._02_name = value
                elif key == '_03_proj_desc':
                    self._03_proj_desc = value
                elif key == '_04_files_provided':
                    self._04_files_provided = value.split()
                elif key == '_05_files_submitted':
                    self._05_files_submitted = value.split()
                elif key == '_06_inp_outps':
                    temp_inp_outps = value.split()
                    for io in temp_inp_outps:
                        i_o = io.strip().split( ':' )
                        self._06_inp_outps[i_o[0]] = i_o[1].strip()
                elif key == '_07_language':
                    self._07_language = value
                elif key == '_08_command_line_options':
                    self._08_command_line_options = value.split()
                elif key == '_09_student_make_file':
                    self._09_student_make_file = eval( value )
                elif key == '_10_make_targs':
                    self._10_make_targs = value.split()
                elif key == '_11_scores':
                    temp_scores = value.split()
                    for s in temp_scores:
                        self._11_scores.append( int( s.strip() ) )

