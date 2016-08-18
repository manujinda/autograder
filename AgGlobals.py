'''
Created on Aug 9, 2016

@author: Manujinda Wathugala

Global constants and formats that are used across classes of the autograder
'''

class AgGlobals( object ):

    # Autograder Diectory Names
    STUDENTS_DIRECTORY = 'students'  # This is where student details database and all the cloned student repositories are kept
    GRADING_DIRECTORY = 'grading'  # This is where compiling of all the student code and testing happens. A copy of student submissions are made here.
    INPUT_OUTPUT_DIRECTORY = 'in_out'  # This is where test inputs and their intended output are kept

    # Autograder Configuration file name and keywords
    AUTOGRADER_CFG_NAME = 'autograder.cfg'  # Name of the autograder configuration file
    AUTOGRADER_CFG_SECTION = 'Autograder Setup'  # Section name in the autograder configuration file to store configuration values
    AUTOGRADER_CFG_GRADING_ROOT = 'grading_root'  # The directory name for the autograder directory tree is stored under key in the config file. Everything autograder cares for gradeing is stored within a directory with this name
    AUTOGRADER_CFG_GRADING_MASTER = 'grading_master'  # The directory name for the directory where all the assignment / project details are stored is provided under this key in the config file. It is suggested to give this directory a meaningful name like 'Assignments' or 'Projects'

    # Assignment / project configuration file name and formats
    ASSIGNMENT_CFG_FORMAT = '+_1_{}.cfg'  # Format for the assignment / project configuration file name. E.g. +_1_Assignment_1.cfg
    ASSIGNMENT_CFG_DUE_DATE_FORMAT = '%m/%d/%Y'  # This should match the format provided in ASSIGNMENT_INIT_DUE_DATE

    # Different states of an assignment / project
    INITIALIZED = 0
    LOADED = 1
    PROBLEMS_CREATED = 2

    # Assignment object initial values.
    # These values are chosen this way to automatically generate a meaningful assignment / project configuration file with comments.
    ASSIGNMENT_INIT_NO = '1 ; insert the assignment number before the ; sign'
    ASSIGNMENT_INIT_NAME = 'hello world ; insert the assignment name before the ; sign'
    ASSIGNMENT_INIT_DUE_DATE = '6/28/2016 ; insert the due date before the ; sign. Format mm/dd/yyyy'
    ASSIGNMENT_INIT_PROBLEM_IDS = '1:prog 2:code 3:ans 4:mcq ; insert the different problem names / numbers of this assignment followed by problem type separated by a :. Use spaces to separate problems'

    # Problem configuration file name and keywords
    PROBLEM_CFG_FORMAT = '+_2_{}_problems.cfg'  # Format for problems of an assignment / project configuration file name. E.g. +_2_Assignment_1_problems.cfg
    PROBLEM_CFG_SECTION_FORMAT = '{}_problem_{}'  # Format for the section name in configuration file for a specific problem in the problem configuration file. E.g. Assignment_1_problem_2
    # Problem types
    PROG = 'prog'  # A programming problem. Student submits a program that can be compiled and run
    CODE = 'code'  # A coding segment problem. Student submits code segments. Not necessarily complete programs. Cannot compile and run as it is
    ANS = 'ans'  # A text answer type submission
    MCQ = 'mcq'  # Multiple choice question

    # Problem object initial values.
    # These values are chosen this way to automatically generate a meaningful problem configuration file with comments.
    PROBLEM_INIT_NAME = 'Problem name'
    PROBLEM_INIT_DESCRIPTION = 'Problem description'
    PROBLEM_INIT_FILES_PRVIDED = 'provided_1 provided_2 provided_3 ; List the names of the provided files before the ; separated by spaces'
    PROBLEM_INIT_FILES_SUBMITTED = 'file_1:alias_1_1:alias_1_2 file_2:alias_2_1 ; List the names of the files students are supposed to submit before the ; separated by spaces. To handle naming errors, for each file a student is supposed to submit you can give a : separated list of aliases'
    PROBLEM_INIT_INP_OUTPS = '1:short:stdout 2:long:file 3:cmd:stdout ; List the nature of inputs and outputs to test submissions for this programming problem. Format - Input_ID:Input_Lenght:Output_location'
    PROBLEM_INIT_COMMAND_LINE_OPTIONS = False
    PROBLEM_INIT_STUDENT_MAKE_FILE = False
    PROBLEM_INIT_MAKE_TARGS = []
    PROBLEM_INIT_TIMEOUT = -1  # Timeout interval to decide infinite loop. # -1 means do not timeout
    PROBLEM_INIT_LANGUAGE = ''
    PROBLEM_INIT_DEPENDS_ON = ''

    # Input output configuration file names
    INPUT_CFG_FORMAT = '+_3_{}_inputs.cfg'  # Format for test inputs for a program assignment configuration file name. E.g. +_3_Assignment_1_inputs.cfg
    INPUT_CFG_SECTION_FORMAT = '{}_problem_{}_input_{}'  # Format for the section name in configuration file for a specific input to a problem. E.g. Assignment_1_problem_2_input_1
    INPUT_FILE_NAME_FORMAT = '{}_input_problem_{}_{}.txt'  # Format for the file name that holds a single set of inputs for a single run of a program. Used when the input to be provided is lengthy. E.g. 2_input_problem_1_Assignment_1.txt
    # Nature of inputs
    SHORT = 'short'  # Short single line inputs provided when the program prompts for them. These inputs are described in the input configuration file itself.
    LONG = 'long'  # Multi-line input that are fed into the program at a single prompt or several prompts. These inputs are described in separate files one for each set of inputs. The input configuration file only records the link to the file that holds the actual input.
    CMD = 'cmd'  # Command-line input. Described in the input configuration file itself.
    # Output location
    STDOUT = 'stdout'  # Output is printed on standard output.
    FILE = 'file'  # Output is produced in a specific file.

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
        return AgGlobals.INPUT_FILE_NAME_FORMAT.format( input_id, problem_id, assignment_name )


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

