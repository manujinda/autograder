'''
Created on Jul 28, 2016
Encapsulates a single problem

@author: Manujinda Wathugala
'''
import ConfigParser
import os
import re
import sys

from AgGlobals import AgGlobals
from Command import Command
from Input import Input


class Problem( object ):
    """
        A class to represent a single problem or a Homework
    """

    def __init__( self, no, prob_type ):
        self._01_prob_no = no
        self._02_name = AgGlobals.PROBLEM_INIT_NAME
        self._03_prob_type = prob_type
        self._04_prob_desc = AgGlobals.PROBLEM_INIT_DESCRIPTION

        if self._03_prob_type == AgGlobals.PROBLEM_TYPE_PROG:
            self._05_files_provided = AgGlobals.PROBLEM_INIT_FILES_PRVIDED

            # Describe the nature of the inputs and outputs to be used in grading
            # this programming problem.
            # The actual inputs and outputs are not described here. They are described
            # in a separate directory. The format to describe inputs and outputs is:
            #    Input_ID:Input_Lenght:Output_location
            #    Input_ID          -      A unique identifier to identify a single and complete set of inputs to a since execution of the program
            #    Input_Length      -      How long the input is and the nature of the input. Possible values are:
            #                              short  - short single line inputs provided when the program prompts for them.
            #                                       These inputs are described in the input configuration file itself.
            #                              long   - multi-line input that are fed into the program at a single prompt or several prompts
            #                                       These inputs are described in separate files one for each set of inputs
            #                                       The input configuration file only records the link to the file that holds the actual input
            #    Output_Location   -      Where the output will be produced. The possible values are:
            #                              stdout    - Output is printed on standard output
            #                              file      - Output is produced in a specific file.
            #                              both      - Part of the output is to stdout and part to a file
            self._07_inp_outps = AgGlobals.PROBLEM_INIT_INP_OUTPS  # '1:short:stdout 2:long:file 3:long:both ; List the nature of inputs and outputs to test submissions for this programming problem. Format - Input_ID:Input_Lenght:Output_location'

            self._09_command_line_options = AgGlobals.PROBLEM_INIT_COMMAND_LINE_OPTIONS
            self._10_student_make_file = AgGlobals.PROBLEM_INIT_STUDENT_MAKE_FILE
            self._11_make_targs = AgGlobals.PROBLEM_INIT_MAKE_TARGS

            # Timeout interval to decide infinite loop
            # -1 means do not timeout
            self._13_timeout = AgGlobals.PROBLEM_INIT_TIMEOUT

        if self._03_prob_type == AgGlobals.PROBLEM_TYPE_PROG or self._03_prob_type == AgGlobals.PROBLEM_TYPE_CODE:
            self._08_language = AgGlobals.PROBLEM_INIT_LANGUAGE

        self._06_files_submitted = AgGlobals.PROBLEM_INIT_FILES_SUBMITTED

        # self._12_scores = []

        # self._14_depends_on = ' ; Problem numbers of other problems that this problem is dependent on. These problems should be specified prior to this problem'
        self._14_depends_on = AgGlobals.PROBLEM_INIT_DEPENDS_ON

        self._99_state = AgGlobals.PROBLEM_STATE_INITIALIZED


    def __str__( self ):
#         desc = ''
#         for f in sorted( self.__dict__.keys() ):
#             desc += '{} > {} \n'.format( f[4:], self.__dict__[f] )
#         return desc
        return AgGlobals.string_of( self, 4 )

    '''
    Read problem configuration file and populate the instance variables
    '''
    def load_problem( self, config_file, section ):

        # Check whether the problem configuration file exists.
        if not os.path.exists( config_file ):
            print '\nProblem configuration file {} does not exist, exit...'.format( config_file )
            sys.exit()

        config = ConfigParser.SafeConfigParser()
        config.read( config_file )

        try:
            for key in sorted( self.__dict__.keys() ):
                if key[0:4] != '_99_':
                    self.__dict__[key] = config.get( section, key[4:] ).strip()
        except ConfigParser.NoSectionError as no_sec_err:
            print 'Error: {} in problem configuration file {}. Exiting...'.format( no_sec_err, config_file )
            sys.exit()
        except ConfigParser.NoOptionError as no_op_err:
            print 'Error: {} in problem configuration file {}. Exiting...'.format( no_op_err, config_file )
            sys.exit()

        if self._03_prob_type == AgGlobals.PROBLEM_TYPE_PROG:
            self._05_files_provided = self._05_files_provided.split()
            self._99_compiled = False

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

            self._13_timeout = int( self._13_timeout )

        # self._06_files_submitted = 'file_1:alias_1_1:alias_1_2 file_2:alias_2_1 ; List the names of the files students are supposed to submit before the ; separated by spaces. To handle naming errors, for each file a student is supposed to submit you can give a : separated list of aliases'
        # This is a list of lists with all the submitted file names and their file name aliases.
        # The first entry is the expected file name
        self._06_files_submitted = AgGlobals.parse_config_line( self._06_files_submitted )

        self._14_depends_on = self._14_depends_on.split()
        if self._01_prob_no in self._14_depends_on:
            print 'Error: Problem {} - {} is dependent on itself. Exiting...'.format( self._01_prob_no, self._02_name )
            sys.exit()

        self._99_state = AgGlobals.PROBLEM_STATE_LOADED
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


    def get_inp_outps( self ):
        if self._03_prob_type == AgGlobals.PROBLEM_TYPE_PROG:
            return self._07_inp_outps
        else:
            return {}


    def generate_input_config( self, assignment, in_out_dir, cfg ):
        if self._03_prob_type == AgGlobals.PROBLEM_TYPE_PROG and self._99_state == AgGlobals.PROBLEM_STATE_LOADED:
            for io in sorted( self._07_inp_outps ):
                print io, self._07_inp_outps[io]
                section = AgGlobals.get_input_section( assignment, self._01_prob_no, io )
                cfg.add_section( section )

                temp_in = Input( self._07_inp_outps[io][0], self._07_inp_outps[io][1] )
                for key in sorted( temp_in.__dict__.keys() ):
                    # Filter only the instances variables that are necessary for the configuration file
                    if key[0:4] != '_99_':
                        cfg.set( section, key[3:], ' {}'.format( temp_in.__dict__[key] ) )

                if self._07_inp_outps[io][0] == AgGlobals.INPUT_NATURE_LONG:
                    input_file_path = os.path.join( in_out_dir, AgGlobals.get_input_file_name( assignment, self._01_prob_no, io ) )
                    cfg.set( section, 'input_file', input_file_path )
                    fo = open( input_file_path, 'a' )
                    fo.close()


    def load_input( self, assignment, input_conf ):
        if self._03_prob_type == AgGlobals.PROBLEM_TYPE_PROG and self._99_state & AgGlobals.PROBLEM_STATE_LOADED == AgGlobals.PROBLEM_STATE_LOADED:
            # Check whether the input configuration file exists.
            if not os.path.exists( input_conf ):
                print '\Input configuration file {} does not exist, exit...'.format( input_conf )
                sys.exit()

            self._99_inputs = {}

            for io in sorted( self._07_inp_outps ):
                self._99_inputs[io] = Input( self._07_inp_outps[io][0], self._07_inp_outps[io][1] )

                section = AgGlobals.get_input_section( assignment, self._01_prob_no, io )
                self._99_inputs[io].load_input( input_conf, section )

            self._99_state |= AgGlobals.PROBLEM_STATE_INPUTS_LOADED

        return self._99_state & AgGlobals.PROBLEM_STATE_INPUTS_LOADED == AgGlobals.PROBLEM_STATE_INPUTS_LOADED


    def compile( self ):
        if self._03_prob_type == AgGlobals.PROBLEM_TYPE_PROG and self._99_state & AgGlobals.PROBLEM_STATE_LOADED == AgGlobals.PROBLEM_STATE_LOADED:
            compile_success = 0
            if self._08_language in ['c', 'C', 'cpp', 'CPP']:
                # Cleanup
                # os.system( 'make clean' )
                retcode, out, err = Command( 'make clean' ).run()
                # retcode, out, err = Command( './main 4 5' ).run( inputs = '5' )

                print 'return: ', retcode
                print 'output: ', out
                print 'error: ', err

                source_pattern = re.compile( '^([_a-zA-Z0-9]+)\.(?:c|C|cpp|CPP)$' )

                for f in self._06_files_submitted:
                    # print f[0]
                    source_file = source_pattern.match( f[0] )
                    if source_file:
                        # print source_file.group( 1 )

                        cmd = 'make {}.o'.format( source_file.group( 1 ) )
                        retcode, out, err = Command( cmd ).run()

                        print retcode
                        print out
                        print err

                        compile_success += retcode

                        # warning = warning_pattern.match( err )
                        if err.find( 'warning' ) >= 0:
                            print '**** Warnings present ****'

                if compile_success == 0:
                    # self._99_state = AgGlobals.PROBLEM_STATE_COMPILED
                    self._99_state |= AgGlobals.PROBLEM_STATE_COMPILED

        return self._99_state & AgGlobals.PROBLEM_STATE_COMPILED == AgGlobals.PROBLEM_STATE_COMPILED


    def link( self ):
        # self._99_linked = False
        if self._03_prob_type == AgGlobals.PROBLEM_TYPE_PROG and self._99_state & AgGlobals.PROBLEM_STATE_COMPILED == AgGlobals.PROBLEM_STATE_COMPILED:
            link_success = 0
            if self._08_language in ['c', 'C', 'cpp', 'CPP']:
                cmd = 'make {}'.format( self._11_make_targs )
                retcode, out, err = Command( cmd ).run()

                print retcode
                print out
                print err

                link_success += retcode

                # warning = warning_pattern.match( err )
                if err.find( 'warning' ) >= 0:
                    print '**** Warnings present ****'

                # self._99_linked = ( link_success == 0 )
                # self._99_state = AgGlobals.PROBLEM_STATE_LINKED
                self._99_state |= AgGlobals.PROBLEM_STATE_LINKED

        return self._99_state & AgGlobals.PROBLEM_STATE_LINKED == AgGlobals.PROBLEM_STATE_LINKED


    def generate_output2( self, assignment, in_out_dir ):
        if self._03_prob_type == AgGlobals.PROBLEM_TYPE_PROG:
            # Check whether the program has been successfully compiled, linked and inputs has been loaded
            if self._99_state & ( AgGlobals.PROBLEM_STATE_LINKED | AgGlobals.PROBLEM_STATE_INPUTS_LOADED ) == AgGlobals.PROBLEM_STATE_LINKED | AgGlobals.PROBLEM_STATE_INPUTS_LOADED:
                for io in sorted( self._99_inputs ):
                    cmd = './{} {}'.format( self._11_make_targs, self._99_inputs[io].get_cmd_line_input() )
                    retcode, out, err = Command( cmd ).run( self._99_inputs[io].get_inputs(), self._13_timeout )
                    print retcode
                    print out
                    print err

                    if retcode == 0:
                        output_file_path = os.path.join( in_out_dir, AgGlobals.get_output_file_name( assignment, self._01_prob_no, io ) )
                        fo = open( output_file_path, 'w' )
                        fo.write( out )
                        fo.close()
                    else:
                        print 'Error Running: {}'.format( cmd )


    def generate_output( self, assignment, in_out_dir ):
        if self._03_prob_type == AgGlobals.PROBLEM_TYPE_PROG:
            # Check whether the program has been successfully compiled, linked and inputs has been loaded
            if self._99_state & ( AgGlobals.PROBLEM_STATE_LINKED | AgGlobals.PROBLEM_STATE_INPUTS_LOADED ) == AgGlobals.PROBLEM_STATE_LINKED | AgGlobals.PROBLEM_STATE_INPUTS_LOADED:
                for io in sorted( self._99_inputs ):
                    output_file_path = os.path.join( in_out_dir, AgGlobals.get_output_file_name( assignment, self._01_prob_no, io ) )
                    fo = open( output_file_path, 'w' )
                    cmd = '../{} {}'.format( self._11_make_targs, self._99_inputs[io].get_cmd_line_input() )
                    retcode, out, err = Command( cmd ).run( self._99_inputs[io].get_inputs(), self._13_timeout, fo, in_out_dir )
                    fo.close()
                    print retcode
                    print out
                    print err

                    for out_file in self._99_inputs[io].get_output_files_generated():
                        cmd = 'mv {0} {1}_{0}'.format( out_file, AgGlobals.get_output_file_name( assignment, self._01_prob_no, io ) )
                        retcode, out, err = Command( cmd ).run( cwd = in_out_dir )
