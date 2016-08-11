'''
Created on Jul 28, 2016
Encapsulates a single problem

@author: Manujinda Wathugala
'''
import ConfigParser
import os
import sys

from AgGlobals import AgGlobals


class Problem( object ):
    """
        A class to represent a single problem or a Homework
    """

    def __init__( self, no, prob_type ):
        self._01_prob_no = no
        self._02_name = 'Problem name'
        self._03_prob_type = prob_type
        self._04_prob_desc = 'Problem description'

        if self._03_prob_type == 'prog':
            self._05_files_provided = 'provided_1 provided_2 provided_3 ; List the names of the provided files before the ; separated by spaces'

            # Describe the nature of the inputs and outputs to be used in grading
            # this programming problem.
            # The actual inputs and outputs are not described here. They are described
            # in a separate directory. The format to describe inputs and outputs is:
            #    Input_ID:Input_Lenght:Output_location
            #    Input_ID          -      A unique identifier to identify a single and complete set of inputs to a since execution of the program
            #    Input_Length      -      How long the input is and the nature of the input. Possible values are:
            #                              cmd    - command-line input. Described in the input configuration file itself.
            #                              short  - short single line inputs provided when the program prompts for them.
            #                                       These inputs are described in the input configuration file itself.
            #                              long   - multi-line input that are fed into the program at a single prompt or several prompts
            #                                       These inputs are described in separate files one for each set of inputs
            #                                       The input configuration file only records the link to the file that holds the actual input
            #    Output_Location   -      Where the output will be produced. The possible values are:
            #                              stdout    - Output is printed on standard output
            #                              file      - Output is produced in a specific file.
            self._07_inp_outps = '1:short:stdout 2:long:file ; List the nature of inputs and outputs to test submissions for this programming problem. Format - Input_ID:Input_Lenght:Output_location'

            self._09_command_line_options = False
            self._10_student_make_file = False
            self._11_make_targs = []

            # Timeout interval to decide infinite loop
            # -1 means do not timeout
            self._13_timeout = -1

        if self._03_prob_type == 'prog' or self._03_prob_type == 'code':
            self._08_language = ''

        self._06_files_submitted = 'file_1:alias_1_1:alias_1_2 file_2:alias_2_1 ; List the names of the files students are supposed to submit before the ; separated by spaces. To handle naming errors, for each file a student is supposed to submit you can give a : separated list of aliases'

        # self._12_scores = []

        # self._14_depends_on = ' ; Problem numbers of other problems that this problem is dependent on. These problems should be specified prior to this problem'
        self._14_depends_on = ''


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

        # Check whether the problem configuration file exists.
        if not os.path.exists( config_file ):
            print '\nProblem configuration file {} does not exist, exit...'.format( config_file )
            sys.exit()

        config = ConfigParser.SafeConfigParser()
        config.read( config_file )

        for key in sorted( self.__dict__.keys() ):
            self.__dict__[key] = config.get( section, key[4:] ).strip()

        if self._03_prob_type == 'prog':
            self._05_files_provided = self._05_files_provided.split()

            # self._07_inp_outps = '1:short:stdout 2:long:file
            in_out = AgGlobals.parse_config_line( self._07_inp_outps )
            temp_io = {}
            for io in in_out:
                if io[0] in temp_io:
                    print 'Error: Duplicate input id for problem: {} - {}'.format( self._01_prob_no, self._02_name )
                    print '\t{} -> ( {}, {} ) and {0} -> ( {}, {} )'.format( io[0], temp_io[io[0]][0], temp_io[io[0]][1], io[1], io[2] )
                    print 'Exiting...'
                    sys.exit()
                else:
                    temp_io[io[0]] = ( io[1], io[2] )
                    # temp_io.append( {'id':io[0], 'length':io[1], 'out_to':io[2]} )

            # self._07_inp_outps is a dictionary with the format:
            #    input_id -> ( Input_Length, Output_Location )
            self._07_inp_outps = temp_io

        # self._06_files_submitted = 'file_1:alias_1_1:alias_1_2 file_2:alias_2_1 ; List the names of the files students are supposed to submit before the ; separated by spaces. To handle naming errors, for each file a student is supposed to submit you can give a : separated list of aliases'
        # This is a list of lists with all the submitted file names and their file name aliases.
        # The first entry is the expected file name
        self._06_files_submitted = AgGlobals.parse_config_line( self._06_files_submitted )

        self._14_depends_on = self._14_depends_on.split()
        if self._01_prob_no in self._14_depends_on:
            print 'Error: Problem {} - {} is dependent on itself. Exiting...'.format( self._01_prob_no, self._02_name )
            sys.exit()

        print self
        return True



    def get_files_provided( self ):
        return self._05_files_provided


    def get_files_submitted( self ):
        files_submitted = []
        for f in self._06_files_submitted:
            files_submitted.append( f[0] )

        return files_submitted


    def get_dependencies( self ):
        return set( self._14_depends_on )


    def get_name( self ):
        return self._02_name


    def get_prob_type( self ):
        return self._03_prob_type
