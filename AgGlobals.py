'''
Created on Aug 9, 2016

@author: Manujinda Wathugala

Global constants and formats that are used across classes of the autograder
'''

class AgGlobals( object ):

    # Autograder Diectory Names
    STUDENTS_DIRECTORY = 'students'  # This is where student details database and all the cloned student repositories are kept
    GRADING_DIRECTORY = 'grading'  # This is where compiling of all the student code and testing happens. A copy of student submissions are made here.
    INPUT_OUTPUT_DIRECTORY = '+_4_in_out'  # This is where test inputs and their intended output are kept
    LOG_FILE_DIRECTORY = '+_5_logs'  # This is where the log file for an assignment / project are kept

    # Autograder Configuration file name and keywords
    AUTOGRADER_CFG_NAME = 'autograder.cfg'  # Name of the autograder configuration file
    AUTOGRADER_CFG_SECTION = 'Autograder Setup'  # Section name in the autograder configuration file to store configuration values
    AUTOGRADER_CFG_GRADING_ROOT = 'grading_root'  # The directory name for the autograder directory tree is stored under key in the config file. Everything autograder cares for gradeing is stored within a directory with this name
    AUTOGRADER_CFG_GRADING_MASTER = 'grading_master'  # The directory name for the directory where all the assignment / project details are stored is provided under this key in the config file. It is suggested to give this directory a meaningful name like 'Assignments' or 'Projects'
    AUTOGRADER_CFG_GRADING_ROOT_COMMENT = '  ; Enter the root directory for all the grading of this class'
    AUTOGRADER_CFG_GRADING_MASTER_COMMENT = 'assignments ; Enter the master directory where all assignment / project configurations are kept'
    AUTOGRADER_LOG_FILE_NAME = '+_6_grading_log.txt'
    AUTOGRADER_GRADEBOOK_NAME_FORMAT = '+_{}_gradebook_{}{}{}.csv'

    # Autograder States
    AG_STATE_CREATED = 1
    AG_STATE_CONFIGURATION_CHECKED = 2
    AG_STATE_ASSIGNMENT_LOADED = 4
    AG_STATE_PROBLEMS_LOADED = 8
    AG_STATE_INPUTS_LOADED = 16
    AG_STATE_COMPILED = 32
    AG_STATE_LINKED = 64
    AG_STATE_OUTPUTS_GENERATED = 128
    AG_STATE_FILE_NAMES_CORRECTED = 256

    # Assignment / project configuration file name and formats
    ASSIGNMENT_CFG_FORMAT = '+_1_{}.cfg'  # Format for the assignment / project configuration file name. E.g. +_1_Assignment_1.cfg
    ASSIGNMENT_CFG_DUE_DATE_FORMAT = '%m/%d/%Y'  # This should match the format provided in ASSIGNMENT_INIT_DUE_DATE

    # Different states of an assignment / project
    ASSIGNMENT_STATE_INITIALIZED = 10
    ASSIGNMENT_STATE_LOADED = 11
    ASSIGNMENT_STATE_PROBLEMS_LOADED = 12

    # Assignment object initial values.
    # These values are chosen this way to automatically generate a meaningful assignment / project configuration file with comments.
    ASSIGNMENT_INIT_NO = '1 ; insert the assignment number before the ; sign'
    ASSIGNMENT_INIT_NAME = 'hello world ; insert the assignment name before the ; sign'
    ASSIGNMENT_INIT_DUE_DATE = '6/28/2016 ; insert the due date before the ; sign. Format mm/dd/yyyy'
    ASSIGNMENT_INIT_PROBLEM_IDS = '1:prog 2:code 3:ans 4:mcq ; insert the different problem numbers of this assignment followed by problem type separated by a :. Use spaces to separate problems'

    # Problem configuration file name and keywords
    PROBLEM_CFG_FORMAT = '+_2_{}_problems.cfg'  # Format for problems of an assignment / project configuration file name. E.g. +_2_Assignment_1_problems.cfg
    PROBLEM_CFG_SECTION_FORMAT = '{}_problem_{}'  # Format for the section name in configuration file for a specific problem in the problem configuration file. E.g. Assignment_1_problem_2
    # Problem types
    PROBLEM_TYPE_PROG = 'prog'  # A programming problem. Student submits a program that can be compiled and run
    PROBLEM_TYPE_CODE = 'code'  # A coding segment problem. Student submits code segments. Not necessarily complete programs. Cannot compile and run as it is
    PROBLEM_TYPE_ANS = 'ans'  # A text answer type submission
    PROBLEM_TYPE_MCQ = 'mcq'  # Multiple choice question

    # Problem object initial values.
    # These values are chosen this way to automatically generate a meaningful problem configuration file with comments.
    PROBLEM_INIT_NAME = 'Problem name'
    PROBLEM_INIT_DESCRIPTION = 'Problem description'
    PROBLEM_INIT_FILES_PRVIDED = 'provided_1 provided_2 provided_3 ; List the names of the provided files before the ; separated by spaces'
    PROBLEM_INIT_FILES_SUBMITTED = 'file_1:alias_1_1:alias_1_2 file_2:alias_2_1 ; List the names of the files students are supposed to submit before the ; separated by spaces. To handle naming errors, for each file a student is supposed to submit you can give a : separated list of aliases'
    PROBLEM_INIT_INP_OUTPS = '1:short:stdout 2:long:file 3:long:both ; List the nature of inputs and outputs to test submissions for this programming problem. Format - Input_ID:Input_Lenght:Output_location'
    PROBLEM_INIT_COMMAND_LINE_OPTIONS = False
    PROBLEM_INIT_STUDENT_MAKE_FILE = False
    PROBLEM_INIT_MAKE_TARGET = '  ; Make target for this problem. This is the final executable generated for this problem'
    PROBLEM_INIT_TIMEOUT = -1  # Timeout interval to decide infinite loop. # -1 means do not timeout
    PROBLEM_INIT_LANGUAGE = ''
    PROBLEM_INIT_DEPENDS_ON = ''
    PROBLEM_INIT_MARKS = 'compile:10 compwarn:5 link:10 linkwarn:5 memleaks:10 0:0 50:80 100:100 ; Specify the different degrees to with the student output should match the reference output and the marks granted'

    # Different states of a problem
    PROBLEM_STATE_INITIALIZED = 1
    PROBLEM_STATE_LOADED = 2
    PROBLEM_STATE_COMPILED = 4
    PROBLEM_STATE_LINKED = 8
    PROBLEM_STATE_INPUTS_LOADED = 16

    # Marks components in the grading rubric
    RUBRIC_COMPILE = 'compile'
    RUBRIC_COMPILE_WARNING = 'compwarn'
    RUBRIC_LINK = 'link'
    RUBRIC_LINK_WARNING = 'linkwarn'
    RUBRIC_MEMLEAK = 'memleak'
    RUBRIC_MARKS = 'marks'
    RUBRIC_FILE_NAMING = 'filenames'

    # Input output configuration file names
    INPUT_CFG_FORMAT = '+_3_{}_inputs.cfg'  # Format for test inputs for a program assignment configuration file name. E.g. +_3_Assignment_1_inputs.cfg
    INPUT_CFG_SECTION_FORMAT = '{}_problem_{}_input_{}'  # Format for the section name in configuration file for a specific input to a problem. E.g. Assignment_1_problem_2_input_1
    # INPUT_FILE_NAME_FORMAT = '{}_input_problem_{}_{}.txt'  # Format for the file name that holds a single set of inputs for a single run of a program. Used when the input to be provided is lengthy. E.g. 2_input_problem_1_Assignment_1.txt
    INPUT_FILE_NAME_FORMAT = 'io_{}_problem_{}_{}_input.txt'  # Format for the file name that holds a single set of inputs for a single run of a program. Used when the input to be provided is lengthy. E.g. io_Assignment_1_problem_1_2_input.txt
    # Nature of inputs
    INPUT_NATURE_SHORT = 'short'  # Short single line inputs provided when the program prompts for them. These inputs are described in the input configuration file itself.
    INPUT_NATURE_LONG = 'long'  # Multi-line input that are fed into the program at a single prompt or several prompts. These inputs are described in separate files one for each set of inputs. The input configuration file only records the link to the file that holds the actual input.
    # INPUT_NATURE_CMD = 'cmd'  # Command-line input. Described in the input configuration file itself.
    # Output location
    OUTPUT_TO_STDOUT = 'stdout'  # Output is printed on standard output.
    OUTPUT_TO_FILE = 'file'  # Output is produced in a specific file.
    OUTPUT_TO_BOTH = 'both'  # Produce some output in stdout and some in file

    # OUTPUT_FILE_NAME_FORMAT = '{}_output_problem_{}_{}.txt'  # Format for the file name that holds the output for a single set of inputs for a single run of a program. E.g. 2_output_problem_1_Assignment_1.txt
    OUTPUT_FILE_NAME_FORMAT = 'io_{}_problem_{}_{}_output.txt'  # Format for the file name that holds the output for a single set of inputs for a single run of a program. E.g. io_Assignment_1_problem_1_2_output.txt

    # Input object initial values.
    # These values are chosen this way to automatically generate a meaningful problem configuration file with comments.
    INPUT_INIT_INPUT = ' ; Enter actual input before the ;. Keep a space between the actual input and the ;.'
    INPUT_INIT_CMD_LINE_INPUT = '  ; Enter command line input'
    INPUT_INIT_INPUT_FILE = ''
    INPUT_INIT_OUTPUT_FILE = ' ; Enter the required output file name before the ;. Keep a space between the actual input and the ;.'
    INPUT_INIT_MARKS = '0:0 50:80 100:100 ; Specify the different degrees to with the student output should match the reference output and the marks granted'

    # Student details database / table and its fields
    STUDENT_DB = 'students.csv'  # The file name for the student details. This is stored in the STUDENTS_DIRECTORY of the autograder dierctory tree.
    STUDENT_DB_FIED_NO = 'No'
    STUDENT_DB_FIED_UOID = 'UO ID'
    STUDENT_DB_FIED_DUCKID = 'Duck ID'
    STUDENT_DB_FIED_LNAME = 'Last Name'
    STUDENT_DB_FIED_FNAME = 'First Name'
    STUDENT_DB_FIED_EMAIL = 'Email'
    STUDENT_DB_FIED_DIR_NAME = 'Dir Name'
    STUDENT_DB_FIED_REPO = 'Repo'
    STUDENT_DB_FIEDLS = [ STUDENT_DB_FIED_NO, STUDENT_DB_FIED_UOID, STUDENT_DB_FIED_DUCKID, STUDENT_DB_FIED_LNAME, STUDENT_DB_FIED_FNAME, STUDENT_DB_FIED_EMAIL, STUDENT_DB_FIED_DIR_NAME, STUDENT_DB_FIED_REPO ]
    # STUDENT_DB_FIEDLS = ['No', 'UO ID', 'Duck ID', 'Last Name', 'First Name', 'Email', 'Dir Name', 'Repo']

    STUDENT_LOG_FILE_NAME_FORMAT = '+_log_file_{}_{}.txt'
    STUDENT_GRADES_FILE_NAME_FORMAT = '+_9_grades_{}_{}.csv'
    STUDENT_LOG_CSS_FILE_NAME = 'style.css'
    STUDENT_LOG_HTML_SKELETON_FILE_NAME = 'skeleton.html'

    # Repository last changed file names
    REPO_LAST_CHANGED_FILE = 'last_changed.txt'
    REPO_GIT_ALREADY_UP_TO_DATE = 'Already up-to-date.\n'


    @classmethod
    def get_asmt_cfg_name( cls, assignment_name ):
        return AgGlobals.ASSIGNMENT_CFG_FORMAT.format( assignment_name )


    @classmethod
    def get_prob_cfg_name( cls, assignment_name ):
        return AgGlobals.PROBLEM_CFG_FORMAT.format( assignment_name )


    @classmethod
    def get_input_cfg_name( cls, assignment_name ):
        return AgGlobals.INPUT_CFG_FORMAT.format( assignment_name )


    @classmethod
    def get_input_file_name( cls, assignment_name, problem_id, input_id ):
        return AgGlobals.INPUT_FILE_NAME_FORMAT.format( assignment_name, problem_id, input_id )


    '''
        This method returns a file name to store output of a test run
        for a particular problem, input pair.
        If the last parameter is None, this gives a file name to store
        output produced in the standard output.
        If the last parameter is a file name, this means that the problem
        generates a file with this name as output when run on this input.
        Since a problem could produce the same output file name for two
        or more different inputs, if we keep only the original name, the
        output file produced by the last set of inputs will only prevail
        overwriting all the others. To prevent this, this function provides
        a unique output file name prefixing the assignment, problem and input
        ids creating a namespace effect.
    '''
    @classmethod
    def get_output_file_name( cls, assignment_name, problem_id, input_id, if_files_produced_name = None ):

        if if_files_produced_name:
            return '{}_{}'.format( AgGlobals.OUTPUT_FILE_NAME_FORMAT.format( assignment_name, problem_id, input_id ), if_files_produced_name )
        else:
            return AgGlobals.OUTPUT_FILE_NAME_FORMAT.format( assignment_name, problem_id, input_id )


    @classmethod
    def get_problem_section( cls, assignment_name, problem_id ):
        return AgGlobals.PROBLEM_CFG_SECTION_FORMAT.format( assignment_name, problem_id )


    @classmethod
    def get_input_section( cls, assignment_name, problem_id, input_id ):
        return AgGlobals.INPUT_CFG_SECTION_FORMAT.format( assignment_name, problem_id, input_id )


    '''
        When a string of the form:
            111:aaa:xxx 22:bbbbb:yy 3:ccc
        is passed this returns a list of lists of the form:
            [ [111, aaa, xxx], [22, bbbbb, yy], [3, cc] ]
    '''
    @classmethod
    def parse_config_line( cls, line ):
        parts = line.split()
        ll = []
        for p in parts:
            ll.append( p.split( ':' ) )

        return ll

    @classmethod
    def get_student_dir_name( cls, index_len, no, name ):
        # If index_len = 3, this creates a string of the form:
        # {:0>3}_{}
        ret = '{}{}{}_{}'.format( '{:0>', index_len, '}', '{}' )

        # Use the format string created above to format the student
        # directory name appropriately
        return ret.format( no, name )

    @classmethod
    def string_of( cls, my_class, skip_chars = 0 ):
        desc = ''
        for key in sorted( my_class.__dict__.keys() ):
            if key[0:4] != '_99_':
                desc += '{} > {} \n'.format( key[skip_chars:], my_class.__dict__[key] )
        return desc


    '''
        Sets particular bits of an integer
    '''
    @classmethod
    def set_flags( cls, var, *flags ):

        # print '{:0>10b}'.format( var )

        for f in flags:
            var |= f

        # print '{:0>10b}'.format( var )

        return var


    '''
        Clears particular bits of an integer
    '''
    @classmethod
    def clear_flags( cls, var, *flags ):

        # print '{:0>10b}'.format( var )

        for f in flags:
            var &= ~f

        # print '{:0>10b}'.format( var )

        return var


    '''
        Checks whether particular bits of an integer is set.
        Returns true only if all the bits are set
    '''
    @classmethod
    def is_flags_set( cls, var, *flags ):
        if len( flags ):

            check_for = 0
            for f in flags:
                check_for |= f

            # print '{:0>10b}'.format( var )
            # print '{:0>10b}'.format( check_for )

            return var & check_for == check_for

        return False


    @classmethod
    def write_to_log( cls, log_file, message, tabs = 0 ):
        if log_file and message:
            if tabs > 0:
                for line in message.split( '\n' ):
                    log_file.write( '{}{}\n'.format( '\t' * tabs, line ) )
            else:
                log_file.write( message )


    @classmethod
    def get_stud_log_file_name( cls, student_dir_name, assignment_sub_dir_name ):
        return AgGlobals.STUDENT_LOG_FILE_NAME_FORMAT.format( assignment_sub_dir_name, student_dir_name )

    @classmethod
    def get_stud_grades_file_name( cls, student_dir_name, assignment_sub_dir_name ):
        return AgGlobals.STUDENT_GRADES_FILE_NAME_FORMAT.format( assignment_sub_dir_name, student_dir_name )


    @classmethod
    def get_gradebook_file_name( cls, assingment_name, prob_no = None ):
        if prob_no:
            return AgGlobals.AUTOGRADER_GRADEBOOK_NAME_FORMAT.format( 8, assingment_name, '_', prob_no )
        else:
            return AgGlobals.AUTOGRADER_GRADEBOOK_NAME_FORMAT.format( 7, assingment_name, '', '' )


    @classmethod
    def get_gradebook_heading( cls, heading_type, problem_no ):
        if heading_type == AgGlobals.RUBRIC_COMPILE:
            return '{}_Compile'.format( problem_no )

        if heading_type == AgGlobals.RUBRIC_COMPILE_WARNING:
            return '{}_No Warnings\nCompiling'.format( problem_no )

        if heading_type == AgGlobals.RUBRIC_LINK:
            return '{}_Link'.format( problem_no )

        if heading_type == AgGlobals.RUBRIC_LINK_WARNING:
            return '{}_No Warnings\nLinking'.format( problem_no )

        if heading_type == AgGlobals.RUBRIC_MEMLEAK:
            return '{}_No Memory Leaks'.format( problem_no )

        if heading_type == AgGlobals.RUBRIC_MARKS:
            return '{}_Marks'.format( problem_no )

    # Other constant gradebook headers
    GRADEBOOK_HEADER_STUDENT = 'Student'
    GRADEBOOK_HEADER_TOTAL = 'Total'
    GRADEBOOK_HEADER_COMMENT = 'Comment'
