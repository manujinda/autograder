'''
Created on Jul 28, 2016
Encapsulates a single problem

@author: Manujinda Wathugala
'''
import ConfigParser
from difflib import SequenceMatcher
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
        try:
            self._01_prob_no = int( self._01_prob_no )
        except ValueError:
            print 'Error: Problem number "{}" of problem type "{}" must be an integer. Exiting...'.format( self._01_prob_no, prob_type )
            sys.exit()

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
            self._11_make_target = AgGlobals.PROBLEM_INIT_MAKE_TARGET

            # Timeout interval to decide infinite loop
            # -1 means do not timeout
            self._13_timeout = AgGlobals.PROBLEM_INIT_TIMEOUT

        if self._03_prob_type == AgGlobals.PROBLEM_TYPE_PROG or self._03_prob_type == AgGlobals.PROBLEM_TYPE_CODE:
            self._08_language = AgGlobals.PROBLEM_INIT_LANGUAGE

        self._06_files_submitted = AgGlobals.PROBLEM_INIT_FILES_SUBMITTED

        # self._12_scores = []

        # self._14_depends_on = ' ; Problem numbers of other problems that this problem is dependent on. These problems should be specified prior to this problem'
        self._14_depends_on = AgGlobals.PROBLEM_INIT_DEPENDS_ON

        # The percentage the student outputs for all grading input for this problem should
        # match with the reference outputs and the amount of marks granted if student output achieves that level.
        # Format: a list of matching_%:marks and compile:marks compwarn:marks link:makrs linkwarn:marks memleaks:marks
        # 0 means no matching at all and 100 means perfect matching.
        self._15_marks = AgGlobals.PROBLEM_INIT_MARKS

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

        self._99_state = AgGlobals.clear_flags( self._99_state, AgGlobals.PROBLEM_STATE_LOADED )

        prob_no_in_assignment = self._01_prob_no
        prob_type_in_assignment = self._03_prob_type

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


        try:
            self._01_prob_no = int( self._01_prob_no )
        except ValueError:
            print 'Error: Problem number {} for problem {} must be an integer. Exiting...'.format( self._01_prob_no, self._02_name )
            sys.exit()

        if self._01_prob_no != prob_no_in_assignment:
            print 'Error:  Problem number mismatch for problem "{}" of type "{}"'.format( self._02_name, self._03_prob_type )
            print '\tProblem number in assignment configuration : {}'.format( prob_no_in_assignment )
            print '\tProblem number in problem configuration    : {}'.format( self._01_prob_no )
            print '\tExiting...'
            sys.exit()

        if self._03_prob_type != prob_type_in_assignment:
            print 'Error:  Problem type mismatch for problem "{} - {}"'.format( self._01_prob_no, self._02_name )
            print '\tProblem type in assignment configuration : {}'.format( prob_type_in_assignment )
            print '\tProblem type in problem configuration    : {}'.format( self._03_prob_type )
            print '\tExiting...'
            sys.exit()

        temp_dept = []
        for p in self._14_depends_on.split():
            try:
                temp_dept.append( int( p ) )
            except ValueError:
                print 'Error: Problem {} - {} is dependent on problem id "{}" which is not an integer problem id. Exiting...'.format( self._01_prob_no, self._02_name, p )
                sys.exit()

        self._14_depends_on = temp_dept  # self._14_depends_on.split()
#         if self._01_prob_no in self._14_depends_on:
#             print 'Error: Problem {} - {} is dependent on itself. Exiting...'.format( self._01_prob_no, self._02_name )
#             sys.exit()

        for p in self._14_depends_on:
            if p == self._01_prob_no:
                print 'Error: Problem {} - {} is dependent on itself. Exiting...'.format( self._01_prob_no, self._02_name )
                sys.exit()
            elif p > self._01_prob_no:
                print 'Error: Problem {} - {} is dependent on problem {} that comes after it. Exiting...'.format( self._01_prob_no, self._02_name, p )
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

        temp_marks = AgGlobals.parse_config_line( self._15_marks )
        self._15_marks = {}

        # The marks that have the form <outpu matching %> --> <grade>
        # These are needed separately to grade student output.
        # So, they are kept in a separate dictionary for the ease of processing.
        self._99_threshold_marks = {}

        for mark in temp_marks:
            try:
                thresh = float( mark[0] )
            except ValueError:
                thresh = mark[0]

            try:
                self._15_marks[thresh] = float( mark[1] )
            except ValueError as e:
                print 'Error: Problem Configuration File: {}'.format( config_file )
                print '\tMarks should be Integer or Real valued. Check'
                print '\t\tProblem: {}'.format( self._01_prob_no )
                print '\t\tMarks = {}:{}'.format( mark[0], mark[1] )
                exit()

            if isinstance( thresh, float ):
                self._99_threshold_marks[thresh] = self._15_marks[thresh]

        self._99_state = AgGlobals.set_flags( self._99_state, AgGlobals.PROBLEM_STATE_LOADED )
        # print self
        return True


    def get_files_provided( self ):
        return self._05_files_provided


    def get_files_submitted( self ):
        files_submitted = []
        for f in self._06_files_submitted:
            files_submitted.append( f[0] )

        return files_submitted


    def get_files_submitted_with_aliases( self ):
        return self._06_files_submitted


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
        if self._03_prob_type == AgGlobals.PROBLEM_TYPE_PROG and AgGlobals.is_flags_set( self._99_state, AgGlobals.PROBLEM_STATE_LOADED ):
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
        if self._03_prob_type == AgGlobals.PROBLEM_TYPE_PROG and AgGlobals.is_flags_set( self._99_state, AgGlobals.PROBLEM_STATE_LOADED ):
            # Check whether the input configuration file exists.
            self._99_state = AgGlobals.clear_flags( self._99_state, AgGlobals.PROBLEM_STATE_INPUTS_LOADED )
            if not os.path.exists( input_conf ):
                print '\Input configuration file {} does not exist, exit...'.format( input_conf )
                sys.exit()

            self._99_inputs = {}

            for io in sorted( self._07_inp_outps ):
                self._99_inputs[io] = Input( self._07_inp_outps[io][0], self._07_inp_outps[io][1] )

                section = AgGlobals.get_input_section( assignment, self._01_prob_no, io )
                self._99_inputs[io].load_input( input_conf, section )

            self._99_state = AgGlobals.set_flags( self._99_state, AgGlobals.PROBLEM_STATE_INPUTS_LOADED )

            return True

        return False


    def compile( self, cwd, grading_log_file, student_log_file, gradebook ):
        # rubric = self._15_marks.keys()

        # if AgGlobals.RUBRIC_COMPILE in rubric:
        #    gradebook['{}_Compile'.format( self._01_prob_no )] = self._15_marks[AgGlobals.RUBRIC_COMPILE]

        # if AgGlobals.RUBRIC_COMPILE_WARNING in rubric:
        #    gradebook['{}_No Warnings Compiling'.format( self._01_prob_no )] = self._15_marks[AgGlobals.RUBRIC_COMPILE_WARNING]

        # return True

        if self._03_prob_type == AgGlobals.PROBLEM_TYPE_PROG and AgGlobals.is_flags_set( self._99_state, AgGlobals.PROBLEM_STATE_LOADED ):

            self._99_state = AgGlobals.clear_flags( self._99_state, AgGlobals.PROBLEM_STATE_COMPILED, AgGlobals.PROBLEM_STATE_LINKED )
            compile_success = 0
            warnings_present = False

            if self._08_language in ['c', 'C', 'cpp', 'CPP']:
                # Cleanup
                retcode, out, err = Command( 'make clean' ).run( cwd = cwd )

                # print 'return: ', retcode
                # print 'output: ', out
                # print 'error: ', err

                source_pattern = re.compile( '^([_a-zA-Z0-9]+)\.(?:c|C|cpp|CPP)$' )

                for f in self._06_files_submitted:
                    source_file = source_pattern.match( f[0] )
                    if source_file:
                        # print source_file.group( 1 )

                        cmd = 'make {}.o'.format( source_file.group( 1 ) )
                        retcode, out, err = Command( cmd ).run( cwd = cwd )

                        print retcode
                        print out
                        print err

                        compile_success += retcode

                        # warning = warning_pattern.match( err )
                        if err.find( 'error' ) >= 0:
                            AgGlobals.write_to_log( grading_log_file, 'Error: Compiling file {}\n'.format( f[0] ), 1 )
                            AgGlobals.write_to_log( student_log_file, '<div class=error>Error: Compiling file {}</div>'.format( f[0] ), 1 )

                            AgGlobals.write_to_log( student_log_file, '<div class=error_out><pre>', 1 )
                            err = err.replace( "&", "&amp;" ).replace( "<", "&lt;" ).replace( ">", "&gt;" )
                            AgGlobals.write_to_log( student_log_file, err, 2 )
                            AgGlobals.write_to_log( student_log_file, '</pre></div>', 1 )
                            print '**** Compilation Errors present ****'

                        elif err.find( 'warning' ) >= 0:
                            AgGlobals.write_to_log( grading_log_file, 'Warning: Compiling file {}\n'.format( f[0] ), 1 )
                            # AgGlobals.write_to_log( student_log_file, '\tWarning: Compiling file {}\n'.format( f[0] ) )
                            AgGlobals.write_to_log( student_log_file, '<div class=warning>Warning: Compiling file {}</div>'.format( f[0] ), 1 )

                            # AgGlobals.write_to_log( grading_log_file, err, 2 )

                            AgGlobals.write_to_log( student_log_file, '<div class=warning_out><pre>', 1 )
                            err = err.replace( "&", "&amp;" ).replace( "<", "&lt;" ).replace( ">", "&gt;" )
                            AgGlobals.write_to_log( student_log_file, err, 2 )
                            AgGlobals.write_to_log( student_log_file, '</pre></div>', 1 )
                            print '**** Compilation Warnings present ****'
                            warnings_present = True

                if compile_success == 0:
                    # self._99_state = AgGlobals.PROBLEM_STATE_COMPILED
                    self._99_state = AgGlobals.set_flags( self._99_state, AgGlobals.PROBLEM_STATE_COMPILED )

                    if gradebook:
                        AgGlobals.write_to_log( grading_log_file, 'Success: Compiling problem: {}) {}\n'.format( self._01_prob_no, self._02_name ) )
                        # AgGlobals.write_to_log( student_log_file, 'Success: Compiling problem: {}) {}\n'.format( self._01_prob_no, self._02_name ) )
                        AgGlobals.write_to_log( student_log_file, '<h3 class=success>Success: Compiling problem: {}) {}</h3>'.format( self._01_prob_no, self._02_name ), 1 )

                        rubric = self._15_marks.keys()
                        if AgGlobals.RUBRIC_COMPILE in rubric:
                            gradebook[AgGlobals.get_gradebook_heading( AgGlobals.RUBRIC_COMPILE, self._01_prob_no )] = self._15_marks[AgGlobals.RUBRIC_COMPILE]

                        if ( not warnings_present ) and AgGlobals.RUBRIC_COMPILE_WARNING in rubric:
                            gradebook[AgGlobals.get_gradebook_heading( AgGlobals.RUBRIC_COMPILE_WARNING, self._01_prob_no )] = self._15_marks[AgGlobals.RUBRIC_COMPILE_WARNING]

                    else:
                        print 'Success: Compiling sample solution'

        return AgGlobals.is_flags_set( self._99_state, AgGlobals.PROBLEM_STATE_COMPILED )


    def link( self, cwd, grading_log_file, student_log_file, gradebook ):
        # rubric = self._15_marks.keys()

        # if AgGlobals.RUBRIC_LINK in rubric:
        #    gradebook['{}_Link'.format( self._01_prob_no )] = self._15_marks[AgGlobals.RUBRIC_LINK]

        # if AgGlobals.RUBRIC_LINK_WARNING in rubric:
        #    gradebook['{}_No Warnings Linking'.format( self._01_prob_no )] = self._15_marks[AgGlobals.RUBRIC_LINK_WARNING]

        # return True

        # self._99_linked = False
        if self._03_prob_type == AgGlobals.PROBLEM_TYPE_PROG and AgGlobals.is_flags_set( self._99_state, AgGlobals.PROBLEM_STATE_COMPILED ):

            self._99_state = AgGlobals.clear_flags( self._99_state, AgGlobals.PROBLEM_STATE_LINKED )
            link_success = 0
            warnings_present = False

            if self._08_language in ['c', 'C', 'cpp', 'CPP']:
                cmd = 'make {}'.format( self._11_make_target )
                retcode, out, err = Command( cmd ).run( cwd = cwd )

                print retcode
                print out
                print err

                link_success += retcode

                if err.find( 'error' ) >= 0:
                    AgGlobals.write_to_log( grading_log_file, 'Error: Linking target {} in problem: {} ) {}\n'.format( self._11_make_target, self._01_prob_no, self._02_name ), 1 )
                    AgGlobals.write_to_log( student_log_file, '<div class=error>Error: Linking target {} in problem: {} ) {}</div>'.format( self._11_make_target, self._01_prob_no, self._02_name ), 1 )

                    AgGlobals.write_to_log( student_log_file, '<div class=error_out><pre>', 1 )
                    err = err.replace( "&", "&amp;" ).replace( "<", "&lt;" ).replace( ">", "&gt;" )
                    AgGlobals.write_to_log( student_log_file, err, 2 )
                    AgGlobals.write_to_log( student_log_file, '</pre></div>', 1 )
                    print '**** Linking Errors present ****'

                # warning = warning_pattern.match( err )
                elif err.find( 'warning' ) >= 0:
                    AgGlobals.write_to_log( grading_log_file, 'Warning: Linking target {} in problem: {} ) {}\n'.format( self._11_make_target, self._01_prob_no, self._02_name ), 1 )
                    # AgGlobals.write_to_log( student_log_file, '\tWarning: Linking target {} in problem: {} ) {}\n'.format( self._11_make_target, self._01_prob_no, self._02_name ) )
                    AgGlobals.write_to_log( student_log_file, '<div class=warning>Warning: Linking target {} in problem: {} ) {}</div>'.format( self._11_make_target, self._01_prob_no, self._02_name ), 1 )

                    # AgGlobals.write_to_log( grading_log_file, err, 2 )

                    AgGlobals.write_to_log( student_log_file, '<div class=warning_out><pre>', 1 )
                    err = err.replace( "&", "&amp;" ).replace( "<", "&lt;" ).replace( ">", "&gt;" )
                    AgGlobals.write_to_log( student_log_file, err, 2 )
                    AgGlobals.write_to_log( student_log_file, '</pre></div>', 1 )
                    print '**** Linking Warnings present ****'
                    warnings_present = True

                # self._99_linked = ( link_success == 0 )
                # self._99_state = AgGlobals.PROBLEM_STATE_LINKED
                if link_success == 0:
                    self._99_state = AgGlobals.set_flags( self._99_state, AgGlobals.PROBLEM_STATE_LINKED )

                    if gradebook:
                        AgGlobals.write_to_log( grading_log_file, 'Success: Linking target {} in problem: {}) {}\n'.format( self._11_make_target, self._01_prob_no, self._02_name ) )
                        # AgGlobals.write_to_log( student_log_file, 'Success: Linking target {} in problem: {}) {}\n'.format( self._11_make_target, self._01_prob_no, self._02_name ) )
                        AgGlobals.write_to_log( student_log_file, '<h3 class=success>Success: Linking target {} in problem: {}) {}</h3>'.format( self._11_make_target, self._01_prob_no, self._02_name ), 1 )

                        rubric = self._15_marks.keys()
                        if AgGlobals.RUBRIC_LINK in rubric:
                            gradebook[AgGlobals.get_gradebook_heading( AgGlobals.RUBRIC_LINK, self._01_prob_no )] = self._15_marks[AgGlobals.RUBRIC_LINK]

                        if ( not warnings_present ) and AgGlobals.RUBRIC_LINK_WARNING in rubric:
                            gradebook[AgGlobals.get_gradebook_heading( AgGlobals.RUBRIC_LINK_WARNING, self._01_prob_no )] = self._15_marks[AgGlobals.RUBRIC_LINK_WARNING]
                    else:
                        print 'Success: Linking sample solution'

        return AgGlobals.is_flags_set( self._99_state, AgGlobals.PROBLEM_STATE_LINKED )


    def generate_output( self, assignment, in_out_dir, assignment_master_dir_path, grading_log_file = None, student_log_file = None, gradebook = None ):
        if self._03_prob_type == AgGlobals.PROBLEM_TYPE_PROG:
            # Check whether the program has been successfully compiled, linked and inputs has been loaded
            if AgGlobals.is_flags_set( self._99_state, AgGlobals.PROBLEM_STATE_LINKED, AgGlobals.PROBLEM_STATE_INPUTS_LOADED ):
                matching_ratio_all_inputs = 0
                for io in sorted( self._99_inputs ):
                    output_file_path = os.path.join( in_out_dir, AgGlobals.get_output_file_name( assignment, self._01_prob_no, io ) )
                    fo = open( output_file_path, 'w' )
                    cmd = '../{} {}'.format( self._11_make_target, self._99_inputs[io].get_cmd_line_input() )
                    retcode, out, err = Command( cmd ).run( self._99_inputs[io].get_inputs(), self._13_timeout, fo, in_out_dir )
                    fo.close()
                    # print 'running return code: ', retcode
                    # print out
                    # print err

                    # print os.path.pardir( in_out_dir )
                    # print assignment

                    if gradebook:
                        AgGlobals.write_to_log( student_log_file, '<h4 class=output>$ {}</h4>'.format( cmd[3:] ), 1 )
                        AgGlobals.write_to_log( student_log_file, '<div>Inputs provided in order</div>', 1 )
                        AgGlobals.write_to_log( student_log_file, '<div class=input><pre>', 1 )
                        AgGlobals.write_to_log( student_log_file, self._99_inputs[io].get_inputs().replace( "&", "&amp;" ).replace( "<", "&lt;" ).replace( ">", "&gt;" ), 2 )
                        AgGlobals.write_to_log( student_log_file, '</pre></div>'.format( self._99_inputs[io].get_inputs() ), 1 )
                        if self._99_inputs[io].does_output_to_stdout():
                            referenec_output_file_path = os.path.join( assignment_master_dir_path, AgGlobals.INPUT_OUTPUT_DIRECTORY, AgGlobals.get_output_file_name( assignment, self._01_prob_no, io ) )
                            # print referenec_output_file_path
                            rf = open( referenec_output_file_path, 'r' )
                            r_lines = rf.read()
                            rf.close()

                            # print output_file_path
                            sf = open( output_file_path )
                            s_lines = sf.read()
                            sf.close()

                            sm = SequenceMatcher( None, s_lines, r_lines )
                            matching_ratio, outpu_diff = self.grade_student_output( s_lines, r_lines, False )
                            print matching_ratio
                            print outpu_diff

                            AgGlobals.write_to_log( student_log_file, '<h5 class=stdout>Standard Output</h5>', 1 )
                            AgGlobals.write_to_log( student_log_file, '<div class=output_diff>', 1 )
                            AgGlobals.write_to_log( student_log_file, outpu_diff, 2 )
                            AgGlobals.write_to_log( student_log_file, '</div>', 1 )

                            matching_ratio_all_inputs += matching_ratio
                            # print sm.ratio()
                            # sm = SequenceMatcher( None, output_file_path, referenec_output_file_path )

                            # cmd = 'diff {} {}'.format( output_file_path, referenec_output_file_path )
                            # retcode, out, err = Command( cmd ).run()
                            # print out, err
                            # for tag, i1, i2, j1, j2 in sm.get_opcodes():
                            #    print ( '{:>7} a[{}:{}] b[{}:{}]'.format( tag, i1, i2, j1, j2 ) )

                            for out_file in self._99_inputs[io].get_output_files_generated():
                                output_file_path = os.path.join( in_out_dir, out_file )
                                if os.path.exists( output_file_path ):
                                    referenec_output_file_path = os.path.join( assignment_master_dir_path, AgGlobals.INPUT_OUTPUT_DIRECTORY, '{}_{}'.format( AgGlobals.get_output_file_name( assignment, self._01_prob_no, io ), out_file ) )
                                    # print referenec_output_file_path
                                    rf = open( referenec_output_file_path, 'r' )
                                    r_lines = rf.read()
                                    rf.close()

                                    sf = open( output_file_path )
                                    s_lines = sf.read()
                                    sf.close()

                                    sm = SequenceMatcher( None, s_lines, r_lines )
                                    matching_ratio, outpu_diff = self.grade_student_output( s_lines, r_lines, False )
                                    # print matching_ratio
                                    # print outpu_diff

                                    AgGlobals.write_to_log( student_log_file, '<h5 class=fileout>Output of file: {}</h5>'.format( out_file ), 1 )
                                    AgGlobals.write_to_log( student_log_file, '<div class=output_diff>', 1 )
                                    AgGlobals.write_to_log( student_log_file, outpu_diff, 2 )
                                    AgGlobals.write_to_log( student_log_file, '</div>', 1 )
                                else:
                                    AgGlobals.write_to_log( grading_log_file, 'Error: Output file {} not created\n'.format( out_file ), 1 )
                                    AgGlobals.write_to_log( student_log_file, '<div class=error>Error: Output file {} not created</div>'.format( out_file ), 1 )

                    for out_file in self._99_inputs[io].get_output_files_generated():
                        cmd = 'mv {0} {1}_{0}'.format( out_file, AgGlobals.get_output_file_name( assignment, self._01_prob_no, io ) )
                        retcode, out, err = Command( cmd ).run( cwd = in_out_dir )

                if gradebook:
                    final_matching_percentage = matching_ratio_all_inputs * 100.0 / len( self._99_inputs )
                    print final_matching_percentage, '%'
                    # print sorted( self._99_threshold_marks, reverse = True )

                    for m in sorted( self._99_threshold_marks, reverse = True ):
                        if final_matching_percentage >= m:
                            gradebook[AgGlobals.get_gradebook_heading( AgGlobals.RUBRIC_MARKS, self._01_prob_no )] = self._99_threshold_marks[m]
                            break


    '''
        Comared the differences between the student output and the reference output
        Based on the differences, provide a matching score for the student output
        Further, provides some html highlighting the differences between the two
        outputs so that the student can improve his or her program.
        student_out    : Studnent's output text
        reference_out  : Reference output text
        ignore_spaces  : If set to true, differences due to white spaces are ignored
    '''
    def grade_student_output( self, student_out, reference_out, ignore_spaces = False ):

        differences = SequenceMatcher( None, student_out, reference_out )

        html = []
        html.append( '<pre>' )

        space_mismatch = 0

        for op, ob, oe, nb, ne in differences.get_opcodes():

            so = student_out[ob:oe].replace( "&", "&amp;" ).replace( "<", "&lt;" ).replace( ">", "&gt;" ).replace( "\n", "&para;<br>" )
            ro = reference_out[nb:ne].replace( "&", "&amp;" ).replace( "<", "&lt;" ).replace( ">", "&gt;" ).replace( "\n", "&para;<br>" )

            if op == 'insert':
                if ( ro.strip() or not ignore_spaces ):
                    html.append( '<ins style=\"background:#e6ffe6;\">{}</ins>'.format( ro ) )
                else:
                    space_mismatch += len( ro )
            elif op == 'delete':
                if ( so.strip() or not ignore_spaces ):
                    html.append( '<del style=\"background:#ffe6e6;\">{}</del>'.format( so ) )
                else:
                    html.append( '<span>{}</span>'.format( so ) )
                    space_mismatch += len( so )
            elif op == 'replace':
                html.append( '<del style=\"background:#ffe6e6;\">{}</del>'.format( so ) )
                html.append( '<ins style=\"background:#e6ffe6;\">{}</ins>'.format( ro ) )
            elif op == 'equal':
                html.append( '<span>{}</span>'.format( so ) )

        html.append( '</pre>' )

        # Compute the matching ratio between the
        # student output and the reference output

        # Default matching ratio
        # This is calculated by:
        #    2.0*M / T
        #        T is the total number of elements in both sequences
        #        M is the number of matches
        matching_ratio = differences.ratio()

        if ignore_spaces:
            # Total lengths of student and reference outputs
            comb_len = len( student_out ) + len( reference_out )
            # print 'comb_len: ', comb_len

            # Reverse engineer the formula used in ratio() to
            # get the default matching elements
            def_match = matching_ratio * comb_len
            # def_match = matching_ratio * tot_elems

            # Add the elements mismatched due to spaces
            # in the the count of matching elements
            new_match = def_match + space_mismatch

            # Re-compute a new ratio using the new matching count
            matching_ratio = new_match / comb_len

        # print "space match : ", space_match
        # print "old ratio : ", def_ratio
        # print "Matching ratio : ", matching_ratio
        return matching_ratio, "".join( html )


    def get_gradebook_headers( self ):
        # problem_header = []
        marks_header = []
        print self._15_marks
        if self._03_prob_type == AgGlobals.PROBLEM_TYPE_PROG:
            if self._08_language in ['c', 'C', 'cpp', 'CPP']:
#                 problem_header = self._01_prob_no
#                 marks_header = 'compile, link, marks'
                rubric = self._15_marks.keys()

                if AgGlobals.RUBRIC_COMPILE in rubric:
                    marks_header.append( AgGlobals.get_gradebook_heading( AgGlobals.RUBRIC_COMPILE, self._01_prob_no ) )

                if AgGlobals.RUBRIC_COMPILE_WARNING in rubric:
                    marks_header.append( AgGlobals.get_gradebook_heading( AgGlobals.RUBRIC_COMPILE_WARNING, self._01_prob_no ) )

                if AgGlobals.RUBRIC_LINK in rubric:
                    marks_header.append( AgGlobals.get_gradebook_heading( AgGlobals.RUBRIC_LINK, self._01_prob_no ) )

                if AgGlobals.RUBRIC_LINK_WARNING in rubric:
                    marks_header.append( AgGlobals.get_gradebook_heading( AgGlobals.RUBRIC_LINK_WARNING, self._01_prob_no ) )

                if AgGlobals.RUBRIC_MEMLEAK in rubric:
                    marks_header.append( AgGlobals.get_gradebook_heading( AgGlobals.RUBRIC_MEMLEAK, self._01_prob_no ) )

                marks_header.append( AgGlobals.get_gradebook_heading( AgGlobals.RUBRIC_MARKS, self._01_prob_no ) )

                # problem_header.append( self._01_prob_no )

                # for r in range( len( marks_header ) - 1 ):
                #    problem_header.append( '' )

        # return ( ','.join( problem_header ), ','.join( marks_header ) )
        print marks_header
        return marks_header
