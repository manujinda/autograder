#!/usr/bin/env python

"""
    autograder.py
    Combines everything and performs autograding of a single project / assignemnt
"""
import ConfigParser
from collections import OrderedDict
import csv
from datetime import datetime
import os
import shutil
import sys

from AgGlobals import AgGlobals
from Assignment import Assignment
from Student import Student


class Autograder( object ):

    def __init__( self, config_file ):
        '''
            Read the autograder configuration file and populate grading root
            and grading master directory names
        '''
        if not os.path.exists( config_file ):
            local_config_file = os.path.join( os.getcwd(), config_file )
            if not os.path.exists( local_config_file ):
                print 'Error: Autograder Configuration File {} does not exist. Exit...'.format( config_file )
                sys.exit( 0 )
            else:
                config_file = local_config_file

        self.config_file = config_file

        config = ConfigParser.SafeConfigParser()
        config.read( self.config_file )

        try:
            # All the grading for a particular offering of a particular class happens under this director
            self.grading_root = config.get( AgGlobals.AUTOGRADER_CFG_SECTION, AgGlobals.AUTOGRADER_CFG_GRADING_ROOT )

            # This is where all the supplied files / solutions etc are kept for each project / assignment.
            # For each project / assignment, there is a separate directory in this directory
            self.grading_master = config.get( AgGlobals.AUTOGRADER_CFG_SECTION, AgGlobals.AUTOGRADER_CFG_GRADING_MASTER )
        except ConfigParser.NoSectionError as no_sec_err:
            print 'Error: {} in autograder configuration file {}. Exiting...'.format( no_sec_err, self.config_file )
            sys.exit()
        except ConfigParser.NoOptionError as no_op_err:
            print 'Error: {} in autograder configuration file {}. Exiting...'.format( no_op_err, self.config_file )
            sys.exit()

        if not self.grading_root:
            print 'Error: Empty grading root. Exit...'
            sys.exit()

        if not self.grading_master:
            print 'Error: Empty grading master. Exit...'
            sys.exit()

        self.students_dict = OrderedDict()

        self.asmnt = Assignment()

        self.students_directory = AgGlobals.STUDENTS_DIRECTORY  # self.agg.get_students_directory()
        self.grading_directory = AgGlobals.GRADING_DIRECTORY  # self.agg.get_grading_directory()

        self.ag_state = AgGlobals.AG_STATE_CREATED


    '''
        Generate a blank autograder configuration file
    '''
    @classmethod
    def generage_autograder_config_skel( self, config_file_name ):
        cfg_file_path = os.path.join( os.getcwd(), config_file_name )
        if os.path.exists( cfg_file_path ):
            print 'Error: The configuration file {} already exists. Exit...'.format( cfg_file_path )
            return False

        assignment_config = ConfigParser.SafeConfigParser()
        assignment_config.add_section( AgGlobals.AUTOGRADER_CFG_SECTION )

        assignment_config.set( AgGlobals.AUTOGRADER_CFG_SECTION, AgGlobals.AUTOGRADER_CFG_GRADING_ROOT, AgGlobals.AUTOGRADER_CFG_GRADING_ROOT_COMMENT )
        assignment_config.set( AgGlobals.AUTOGRADER_CFG_SECTION, AgGlobals.AUTOGRADER_CFG_GRADING_MASTER, AgGlobals.AUTOGRADER_CFG_GRADING_MASTER_COMMENT )

        with open( config_file_name, 'wb' ) as configfile:
            assignment_config.write( configfile )

        print 'Success: Blank autograder configuration file {} successfully created'.format( config_file_name )



    def created( self ):
        return AgGlobals.is_flags_set( self.ag_state, AgGlobals.AG_STATE_CREATED )


    '''
        Setup an autograder directory tree for grading
        projects / assignments for a particular offering
        of a particular class
    '''
    def setup_grading_dir_tree( self ):
        if os.path.exists( self.grading_root ):
            print 'Error: Autograder grading root directory {} already exists. Exit...'.format( self.grading_root )
            sys.exit( 0 )

        os.mkdir( self.grading_root )
        os.mkdir( os.path.join( self.grading_root, self.grading_master ) )

        # All the student git repos are cloned in this directory
        os.mkdir( os.path.join( self.grading_root, self.students_directory ) )

        # All the compiling and grading of student submission happens here.
        # For each student there is a directory with the cloned student repo name in this directory.
        os.mkdir( os.path.join( self.grading_root, self.grading_directory ) )

        # Copy the autograder configuration file to autograder directory for later usage
        shutil.copy2( self.config_file, os.path.join( self.grading_root, AgGlobals.AUTOGRADER_CFG_NAME ) )

        # Get the directory where Autograder.py module is stored
        autograder_module_dir = os.path.dirname( os.path.realpath( __file__ ) )
        # Copy the student comments style sheet to the grading root directory
        shutil.copy2( os.path.join( autograder_module_dir, AgGlobals.STUDENT_LOG_CSS_FILE_NAME ), self.grading_root )


        # Create the skeleton of the student data csv file
        student_db = os.path.join( self.grading_root, self.students_directory, AgGlobals.STUDENT_DB )
        with open( student_db, 'wb' ) as students:
            writer = csv.writer( students, delimiter = ',', quotechar = '|', quoting = csv.QUOTE_MINIMAL )
            writer.writerow( AgGlobals.STUDENT_DB_FIEDLS )

        # Create an example assignment directory and configuration files
        assignment_name = '{}_{}'.format( self.grading_master[:-1], 1 )  # 'assignment1'
        self.new_assignment( assignment_name )

        print 'Success: Setting up autograder directory structure'
        print 'Grading root: {}'.format( self.grading_root )


    ''' Generate a new blank assignment.
        Creates the directory and the default assignment configuration file '''
    def new_assignment( self, assignment_name ):

        # Create an example assignment directory and configuration files
        assignment = Assignment()
        assignment.new_assignment( self.grading_root, self.grading_master, assignment_name )

        return assignment


    def load_assignment( self, assignment_name ):
        if self.asmnt.load_assignment( self.grading_root, self.grading_master, assignment_name ):
            self.ag_state = AgGlobals.set_flags( self.ag_state, AgGlobals.AG_STATE_ASSIGNMENT_LOADED )
            return True

        return False


    def validate_config( self ):
        # Check whether the grading root directory exists.
        # All the student submissions and assignment definitions are stored
        # under this directory.
        # gradingroot\
        #       autograder.cfg
        #       assignments\
        #           assignment1\
        #           assignment2\
        #       grading\
        #           stud1
        #               assignment1\
        #               assignment2\
        #           stud2
        #               assignment1\
        #               assignment2\
        #       students\
        #           students.csv
        #           stud1
        #               assignment1\
        #               assignment2\
        #           stud2
        #               assignment1\
        #               assignment2\
        if not os.path.exists( self.grading_root ):
            print '\nGrading root directory {} does not exist, Exit...'.format( self.grading_root )
            return False
            # sys.exit()

        # Check whether the assignment master directory exists.
        # This is where all the solution and provided files are stored
        master = os.path.join( self.grading_root, self.grading_master )
        if not os.path.exists( master ):
            print '\nMaster directory {} does not exist, exit...'.format( master )
            return False
            # sys.exit()

        # Check whether the student directory exists.
        # This is where all the cloned student repos are stored
        students = os.path.join( self.grading_root, self.students_directory )
        if not os.path.exists( students ):
            print '\nStudent directory {} does not exist, exit...'.format( students )
            return False
            # sys.exit()

        # Check whether the grading directory exists.
        # This is where all grading happens.
        grading = os.path.join( self.grading_root, self.grading_directory )
        if not os.path.exists( grading ):
            print '\nGrading directory {} does not exist, exit...'.format( grading )
            return False
            # sys.exit()

        self.ag_state = AgGlobals.set_flags( self.ag_state, AgGlobals.AG_STATE_CONFIGURATION_CHECKED )
        return True


    def read_students( self ):
        if not self.validate_config():
            sys.exit()

        students = os.path.join( self.grading_root, self.students_directory, AgGlobals.STUDENT_DB )

        if not os.path.exists( students ):
            print '\nStudnt data file {} does not exist, exit...'.format( students )
            sys.exit()

        # self.students = []
        self.students_dict = OrderedDict()
        with open( students ) as student_db:
            reader = csv.DictReader( student_db )
            for row in reader:
                stud = Student( row )
                # self.students.append( stud )
                self.students_dict[stud.get_index()] = stud

        return len( self.students_dict ) > 0


    def update_repos( self ):
        # When student database is sorted in the ascending order of  student index numbers
        # the length of the index number of the last student is the longest. Get the length
        # of that index number and pass that to the cloning method so that when creating the
        # local student repository directory name each directory have the index number of each
        # student prefixed to student name in such a way prefixed index numbers have the same
        # length with 0s padded in the left. e.g. 003_manujinda
        index_len = len( '{}'.format( self.students_dict[next( reversed( self.students_dict ) )].get_index() ) )
        for stud_no in self.students_dict.keys():
            stud = self.students_dict[stud_no]
            stud_dir = os.path.join( self.grading_root, self.students_directory, stud.get_dir( index_len ) )
            if not os.path.exists( stud_dir ):
                # Student repository has not been cloned. Have to clone it first
                stud.clone_student_repo( stud_dir )
            else:
                stud.pull_student_repo( stud_dir )


    '''
        Grading of student submissions
    '''
    def do_grading2( self, stud_no = None, prob_no = None ):

        print 'Grading',

        # A specific problem number is provided for grading
        if prob_no:
            try:
                prob_no = int( prob_no )
            except ValueError:
                print '\nError: Problem number "{}" must be an integer. Exiting...'.format( prob_no )
                exit()

            if not self.asmnt.is_valid_problem_id( prob_no ):
                print '\nError: Invalid problem number {}'.format( prob_no )
                exit()

            print 'problem number {}'.format( prob_no ),

        # Grade a specific student
        if stud_no:
            # Check whether this is a valid student number
            if stud_no in self.students_dict.keys():
                students = [stud_no]
                print 'of student {}'.format( stud_no ),
            else:
                print '\nError: Invalid student number for grading {}. Exiting...'.format( stud_no )
                exit()
        else:
            # Grade all the students
            students = self.students_dict.keys()

        print 'of {}'.format( self.asmnt.get_assignment_sub_dir() )

        # If students are loaded and problems are loaded
        if len( students ) > 0 and AgGlobals.is_flags_set( self.ag_state, AgGlobals.AG_STATE_ASSIGNMENT_LOADED, AgGlobals.AG_STATE_PROBLEMS_LOADED, AgGlobals.AG_STATE_INPUTS_LOADED ) :

            # This is the path for the students directory
            source = os.path.join( self.grading_root, self.students_directory )

            # This is the path for the grading directory
            destination = os.path.join( self.grading_root, self.grading_directory )

            # Length of the longest student index. This is used to insert
            # leading 0's in the student directory name
            index_len = len( '{}'.format( self.students_dict[next( reversed( self.students_dict ) )].get_index() ) )

            # Get the assignment / project master sub directory
            asmnt_master_sub_dir = self.asmnt.get_masterdir()

            # Get a set of all the provided file names for this assignment / project
            provided_files = self.asmnt.get_provided_files_set()

            # Create a list of paths to all the provided files in the assignment master sub directory
            provided_file_paths = []
            for pf in provided_files:

                # Generate the file path for this provided file
                pf_path = os.path.join( asmnt_master_sub_dir, pf )

                # Check whether this file exists in the assignment master sub directory
                if os.path.exists( pf_path ):
                    provided_file_paths.append( pf_path )

                # If this file does not exists, we cannot proceed with the grading
                else:
                    print 'Error: Provided file {} does not exist. Cannot proceed with grading. Exit...'.format( pf_path )
                    sys.exit( 1 )

            now_time = datetime.now()
            deadline = self.asmnt.get_deadline()

            if not deadline:
                print 'Error: Assignment deadline not properly set or assignment not properly loaded. Exiting...'
                sys.exit()

            update_repos = False
            if now_time > deadline:
                print '\nWarning: Assignment deadline has passed!'
                print 'Now     : {}'.format( now_time.strftime( '%x :: %X' ) )
                print 'Deadline: {}'.format( deadline.strftime( '%x :: %X' ) )
                lateness = now_time - deadline
                print 'Lateness: {}\n'.format( str( lateness ).split( '.', 2 )[0] )
                # print 'Lateness: {}'.format( lateness - timedelta( microseconds = lateness.microseconds ) )
                choice = raw_input( 'Do you want to update repos (Y | n)? ' )

                if choice.lower() == 'y':
                    update_repos = True

            # Open grading log file for this student
            log_directory_path = os.path.join( asmnt_master_sub_dir, AgGlobals.LOG_FILE_DIRECTORY )
            grading_log = open( os.path.join( log_directory_path, AgGlobals.AUTOGRADER_LOG_FILE_NAME ), 'a' )
            AgGlobals.write_to_log( grading_log, '\n{0}<< Grading Session on {1} : START >>{0}\n'.format( '-' * 20, now_time.strftime( '%x :: %X' ) ) )

            # Create the gradebook
            gradebook_headers = self.asmnt.generate_gradebook_headers( prob_no )
            if stud_no:
                grades_file_stud_path = os.path.join( log_directory_path, self.students_dict[stud_no].get_stud_grades_file_name( index_len, self.asmnt.get_assignment_sub_dir() ) )
                gradebook = open( grades_file_stud_path, 'wb' )
            else:
                gradebook = open( os.path.join( log_directory_path, AgGlobals.get_gradebook_file_name( self.asmnt.get_assignment_sub_dir(), prob_no ) ), 'wb' )
            gradebook_headers += [ AgGlobals.GRADEBOOK_HEADER_TOTAL, AgGlobals.GRADEBOOK_HEADER_COMMENT ]
            gb = csv.DictWriter( gradebook, gradebook_headers )
            gb.writeheader()

            # Get the directory where Autograder.py module is stored
            autograder_module_dir = os.path.dirname( os.path.realpath( __file__ ) )
            # Open and read grading output skeleton html
            html_file = open( os.path.join( autograder_module_dir, AgGlobals.STUDENT_LOG_HTML_SKELETON_FILE_NAME ), 'r' )
            html_skeleton = html_file.read()

            # For each student
            for stud_no in students:
                stud = self.students_dict[stud_no]

                print '\nStudent: {}) {}'.format( stud.get_index(), stud.get_name() )

                grading_log_stud_path = os.path.join( log_directory_path, stud.get_stud_log_file_name( index_len, self.asmnt.get_assignment_sub_dir() ) )
                grading_log_stud = open( grading_log_stud_path, 'a' )
                # AgGlobals.write_to_log( grading_log_stud, '\n{0}<< Grading Session on {1} : START >>{0}\n'.format( '-' * 20, datetime.now() ) )
                # AgGlobals.write_to_log( grading_log_stud, '\n{0} Student: {1} {0}\n'.format( '#' * 10, stud.get_name() ) )
                AgGlobals.write_to_log( grading_log_stud, '\n<h2 class=grading_session>Grading Session on {}</h2>'.format( datetime.now().strftime( '%x :: %X' ) ), 1 )

                AgGlobals.write_to_log( grading_log, '\n{0} Student: {1} {0}\n'.format( '#' * 10, stud.get_name() ) )

                marks_dict = {}
                for h in gradebook_headers:
                    marks_dict[h] = 0.0
                marks_dict[AgGlobals.GRADEBOOK_HEADER_STUDENT] = stud.get_index()
                marks_dict[AgGlobals.GRADEBOOK_HEADER_COMMENT] = ''

                # Student's directory name
                stud_dir_name = stud.get_dir( index_len )

                # Path for the student's directory in the students directory
                stud_local_repo_path = os.path.join( source, stud_dir_name )

                # Path for the student's directory in the grading directory
                stud_dir_path = os.path.join( destination, stud_dir_name, self.asmnt.get_assignment_sub_dir() )

                # Update student repos only if this is before the deadline
                if now_time <= deadline or update_repos:
                    # Update local student repository
                    if not os.path.exists( stud_local_repo_path ):
                        # Student repository has not been cloned. Have to clone it first
                        stud.clone_student_repo( stud_local_repo_path, grading_log, grading_log_stud )
                    else:
                        stud.pull_student_repo( stud_local_repo_path, grading_log, grading_log_stud )

                # Copy all the student submitted files from student directory in students directory
                # to a directory with the same name in the grading directory
                stud.copy_student_repo( source, destination, index_len )

                # Check whether student has created a directory with the proper name in his or her
                # repository to upload files for this assignment / project
                if not os.path.exists( stud_dir_path ):
                    print '\tError: Student {} does not have the assignment directory {} in the repository.'.format( stud.get_name(), stud_dir_path )
                    AgGlobals.write_to_log( grading_log, '\tError: {} directory does not exist in the repo\n'.format( self.asmnt.get_assignment_sub_dir() ) )
                    AgGlobals.write_to_log( grading_log_stud, '<p class=error>Error: {} directory does not exist in the repo</p>'.format( self.asmnt.get_assignment_sub_dir() ), 1 )
                    marks_dict[AgGlobals.GRADEBOOK_HEADER_COMMENT] = '{} directory does not exist in the repo'.format( self.asmnt.get_assignment_sub_dir() )
                    self.write_stud_marks( marks_dict, gb, grading_log_stud_path, html_skeleton )
                    grading_log_stud.close()
                    continue

                # Copy the provided files into student's directory in the grading directory
                for pf_path in provided_file_paths:
                    shutil.copy2( pf_path, stud_dir_path )

                self.asmnt.grade2( stud_dir_path, grading_log, grading_log_stud, marks_dict )

                grading_log_stud.close()
                grading_log.flush()
                os.fsync( grading_log )

                self.write_stud_marks( marks_dict, gb, grading_log_stud_path, html_skeleton )

                gradebook.flush()
                os.fsync( gradebook )

            grading_log.close()
            gradebook.close()


    def write_stud_marks( self, marks_dict, gb_csv, grading_log_stud_path, html_skeleton ):
        tot = 0
        for h in marks_dict:
            if h != AgGlobals.GRADEBOOK_HEADER_STUDENT and h != AgGlobals.GRADEBOOK_HEADER_COMMENT:
                tot += marks_dict[h]

        marks_dict[AgGlobals.GRADEBOOK_HEADER_TOTAL] = tot

        gb_csv.writerow( marks_dict )

        grading_log_stud_html = open( AgGlobals.get_stud_html_log_file_path( grading_log_stud_path ), 'wb' )
        grading_log_stud = open( grading_log_stud_path, 'r' )
        stud_log_entries = grading_log_stud.read()
        AgGlobals.write_to_log( grading_log_stud_html, html_skeleton )
        AgGlobals.write_to_log( grading_log_stud_html, stud_log_entries )
        AgGlobals.write_to_log( grading_log_stud_html, '</body>\n</html>' )
        grading_log_stud.close()
        grading_log_stud_html.close()


    '''
    If a valid assignment configuration file has been loaded, this will generate necessary problem configuration file
    '''
    def gen_prob_config_skel( self ):
        if AgGlobals.is_flags_set( self.ag_state, AgGlobals.AG_STATE_ASSIGNMENT_LOADED ):
            self.asmnt.generate_problem_config()


    def load_problems( self ):
        if AgGlobals.is_flags_set( self.ag_state, AgGlobals.AG_STATE_ASSIGNMENT_LOADED ):
            result = self.asmnt.load_problems()
            if result:
                self.ag_state = AgGlobals.set_flags( self.ag_state, AgGlobals.AG_STATE_PROBLEMS_LOADED )

            return result
        return False


    def generate_files( self ):
        if AgGlobals.is_flags_set( self.ag_state, AgGlobals.AG_STATE_ASSIGNMENT_LOADED ):
            self.asmnt.generate_provided_files()
            self.asmnt.generate_submitted_files()
            self.asmnt.generate_input_config()


    def load_input( self ):
        if AgGlobals.is_flags_set( self.ag_state, AgGlobals.AG_STATE_ASSIGNMENT_LOADED ):
            if self.asmnt.load_input():
                self.ag_state = AgGlobals.set_flags( self.ag_state, AgGlobals.AG_STATE_INPUTS_LOADED )

                return True
        return False


    def compile( self ):
        if AgGlobals.is_flags_set( self.ag_state, AgGlobals.AG_STATE_ASSIGNMENT_LOADED ):
            if self.asmnt.compile():
                self.ag_state = AgGlobals.set_flags( self.ag_state, AgGlobals.AG_STATE_COMPILED )

                return True
        return False


    def link( self ):
        if AgGlobals.is_flags_set( self.ag_state, AgGlobals.AG_STATE_ASSIGNMENT_LOADED ):
            if self.asmnt.compile():
                if self.asmnt.link():
                    self.ag_state = AgGlobals.set_flags( self.ag_state, AgGlobals.AG_STATE_LINKED )

                    return True
        return False


    def generate_output( self ):
        if AgGlobals.is_flags_set( self.ag_state, AgGlobals.AG_STATE_ASSIGNMENT_LOADED ):
            if self.asmnt.compile():
                if self.asmnt.link() and self.asmnt.load_input():
                    if self.asmnt.generate_output():
                        self.ag_state = AgGlobals.set_flags( self.ag_state, AgGlobals.AG_STATE_OUTPUTS_GENERATED )

                        return True
        return False


if len( sys.argv ) > 1:
    if sys.argv[1] == 'gencfg' or sys.argv[1] == '-cfg':
        Autograder.generage_autograder_config_skel( sys.argv[2] )
        exit()

    if sys.argv[1] == 'setup' or sys.argv[1] == '-s':
        # Setup the initial directory tree for grading one instance of a class
        # Need to run once at the beginning of the semester / term / quarter
        # Command:
        #    $ python Autograder.py setup <path to autograder configuration file>
        # Test Parameters
        #    setup /home/users/manu/Documents/manujinda/uo_classes/4_2016_summer/boyana/autograder_ws/autograder/autograder.cfg
        if len( sys.argv ) > 2:
            ag = Autograder( sys.argv[2] )
            # if ag.created():
            ag.setup_grading_dir_tree()
        else:
            print 'USAGE: Autograder.py setup <path to autograder configuration file>'
        exit()

    if len( sys.argv ) == 7 or len( sys.argv ) == 4:
        ag_cfg = os.path.join( sys.argv[2], AgGlobals.AUTOGRADER_CFG_NAME )
        next_para = 3
    elif len( sys.argv ) == 6 or len( sys.argv ) == 3:
        ag_cfg = os.path.join( os.getcwd(), AgGlobals.AUTOGRADER_CFG_NAME )
        next_para = 2
    else:
        print 'Error: Invalid autograder command line. Exiting...'
        sys.exit()
#     elif len( sys.argv ) > 3:
#         ag_cfg = os.path.join( sys.argv[2], AgGlobals.AUTOGRADER_CFG_NAME )
#         next_para = 3
#     elif len( sys.argv ) > 2:
#         ag_cfg = os.path.join( os.getcwd(), AgGlobals.AUTOGRADER_CFG_NAME )
#         next_para = 2

    ag = Autograder( ag_cfg )

    if not ag.created():
        print 'Error: Autograder not properly created. Exiting...'
        sys.exit()

    if not ag.validate_config():
        print 'Error: Invalid Autograder directory configuration. Exiting... '
        sys.exit()

    if sys.argv[1] == 'newasmnt' or sys.argv[1] == '-n':
        # Create a sub directory for a new assignment / project and provide
        # skeleton configuration file as a start
        # Command:
        #    $ python Autograder.py newasmnt <path to autograder root directory> <assignment / project name>
        # Test Parameters
        #    newasmnt /home/users/manu/Documents/manujinda/uo_classes/4_2016_summer/boyana/grading assignment_2
        ag.new_assignment( sys.argv[next_para] )
        sys.exit()

    if not ag.load_assignment( sys.argv[next_para] ):
        print 'Error: Loading assignment {}. Exiting...'.format( sys.argv[next_para] )
        sys.exit()

    next_para += 1

    if sys.argv[1] == 'genprob' or sys.argv[1] == '-p':
        # Generate blank problem configuration file based on a filled assignment / project configuration file
        # Command:
        #     $ python Autograder.py genprob <path to autograder root directory> <assignment / project name>
        # Test Parameters
        #    genprob /home/users/manu/Documents/manujinda/uo_classes/4_2016_summer/boyana/grading assignment_2
        ag.gen_prob_config_skel()
        sys.exit()

    if not ag.load_problems():
        print 'Error: Loading problems. Exiting...'
        sys.exit()

    if sys.argv[1] == 'genfiles' or sys.argv[1] == '-f':
        # Generate blank files described in the Assignment / Project. The configuration files for the
        # Assignment and its problems must be complete before running this command
        # Command:
        #     $ python Autograder.py genfiles <path to autograder root directory> <assignment / project name>
        # Test Parameters
        #    genfiles /home/users/manu/Documents/manujinda/uo_classes/4_2016_summer/boyana/grading assignment_2
        ag.generate_files()

    elif sys.argv[1] == 'compile' or sys.argv[1] == '-c':
        # Compile program files belonging to this assignment / project
        # Assignment and its problems must be complete before running this command
        # Command:
        #     $ python Autograder.py compile <path to autograder root directory> <assignment / project name>
        # Test Parameters
        #    compile /home/users/manu/Documents/manujinda/uo_classes/4_2016_summer/boyana/grading assignment_2
        ag.compile()

    elif sys.argv[1] == 'link' or sys.argv[1] == '-l':
        # Link object files belonging to this assignment / project
        # Assignment and its problems must be compiled before running this command
        # Command:
        #     $ python Autograder.py link <path to autograder root directory> <assignment / project name>
        # Test Parameters
        #    link /home/users/manu/Documents/manujinda/uo_classes/4_2016_summer/boyana/grading assignment_2
        ag.link()

    elif sys.argv[1] == 'genout' or sys.argv[1] == '-o':
        # Generate reference outputs for test input
        # Assignment and its problems must be compiled before running this command
        # Command:
        #     $ python Autograder.py genout <path to autograder root directory> <assignment / project name>
        # Test Parameters
        #    genout /home/users/manu/Documents/manujinda/uo_classes/4_2016_summer/boyana/grading assignment_2
        ag.generate_output()

    elif sys.argv[1] == 'grading' or sys.argv[1] == '-g':
        # Perform grading
        # Students, Assignment and its problems must be loaded before running this command
        # Command:
        #     $ python Autograder.py grading <path to autograder root directory> <assignment / project name>
        # Test Parameters
        #    grading /home/users/manu/Documents/manujinda/uo_classes/4_2016_summer/boyana/grading assignment_2
        if ag.read_students():
            if ag.load_input():
                if len( sys.argv ) > 5:
                    if sys.argv[next_para] == '-s':
                        ag.do_grading2( stud_no = sys.argv[next_para + 1] )
                    elif sys.argv[next_para] == '-p':
                        ag.do_grading2( prob_no = sys.argv[next_para + 1] )
                    elif sys.argv[next_para] == '-sp' and len( sys.argv ) > 6:
                        ag.do_grading2( stud_no = sys.argv[next_para + 1], prob_no = sys.argv[next_para + 2] )
                else:
                    ag.do_grading2()
            else:
                print 'Error: Inputs not loaded. Exiting...'
        else:
            print 'Error: Students not loaded. Exiting...'

else:
    print 'USAGE: Autograder.py <flag>'

exit()


####################


if len( sys.argv ) > 2:
    if sys.argv[1] == 'gencfg':
        Autograder.generage_autograder_config_skel( sys.argv[2] )
        exit()
    elif sys.argv[1] == 'setup':
        # Setup the initial directory tree for grading one instance of a class
        # Need to run once at the beginning of the semester / term / quarter
        # Command:
        #    $ python Autograder.py setup <path to autograder configuration file>
        # Test Parameters
        #    setup /home/users/manu/Documents/manujinda/uo_classes/4_2016_summer/boyana/autograder_ws/autograder/autograder.cfg
        ag = Autograder( sys.argv[2] )
        # if ag.created():
        ag.setup_grading_dir_tree()

        exit()

else:
    print 'Error: Invalid command'
    exit()

if len( sys.argv ) > 3:
    if sys.argv[1] == 'newasmnt':
        # Create a sub directory for a new assignment / project and provide
        # skeleton configuration file as a start
        # Command:
        #    $ python Autograder.py newasmnt <path to autograder root directory> <assignment / project name>
        # Test Parameters
        #    newasmnt /home/users/manu/Documents/manujinda/uo_classes/4_2016_summer/boyana/grading assignment_2
        ag_cfg = os.path.join( sys.argv[2], AgGlobals.AUTOGRADER_CFG_NAME )
        ag = Autograder( ag_cfg )
        if ag.created():
            if ag.validate_config():
                ag.new_assignment( sys.argv[3] )

    elif sys.argv[1] == 'genprob':
        # Generate blank problem configuration file based on a filled assignment / project configuration file
        # Command:
        #     $ python Autograder.py genprob <path to autograder root directory> <assignment / project name>
        # Test Parameters
        #    genprob /home/users/manu/Documents/manujinda/uo_classes/4_2016_summer/boyana/grading assignment_2
        ag_cfg = os.path.join( sys.argv[2], AgGlobals.AUTOGRADER_CFG_NAME )
        ag = Autograder( ag_cfg )
        if ag.created():
            if ag.validate_config():
                if ag.load_assignment( sys.argv[3] ):
                    ag.gen_prob_config_skel()
                # ag.load_problems()

    elif sys.argv[1] == 'genfiles':
        # Generate blank files described in the Assignment / Project. The configuration files for the
        # Assignment and its problems must be complete before running this command
        # Command:
        #     $ python Autograder.py genfiles <path to autograder root directory> <assignment / project name>
        # Test Parameters
        #    genfiles /home/users/manu/Documents/manujinda/uo_classes/4_2016_summer/boyana/grading assignment_2
        ag_cfg = os.path.join( sys.argv[2], AgGlobals.AUTOGRADER_CFG_NAME )
        ag = Autograder( ag_cfg )
        if ag.created():
            if ag.validate_config():
                if ag.load_assignment( sys.argv[3] ):
                    if ag.load_problems():
                        ag.generate_files()

    elif sys.argv[1] == 'lodinp':
        # Load test inputs to each of the programming problems
        # Assignment and its problems must be complete before running this command
        # Command:
        #     $ python Autograder.py lodinp <path to autograder root directory> <assignment / project name>
        # Test Parameters
        #    lodinp /home/users/manu/Documents/manujinda/uo_classes/4_2016_summer/boyana/grading assignment_2
        ag_cfg = os.path.join( sys.argv[2], AgGlobals.AUTOGRADER_CFG_NAME )
        ag = Autograder( ag_cfg )
        if ag.created():
            if ag.validate_config():
                if ag.load_assignment( sys.argv[3] ):
                    if ag.load_problems():
                        ag.load_input()

    elif sys.argv[1] == 'compile':
        # Compile program files belonging to this assignment / project
        # Assignment and its problems must be complete before running this command
        # Command:
        #     $ python Autograder.py compile <path to autograder root directory> <assignment / project name>
        # Test Parameters
        #    compile /home/users/manu/Documents/manujinda/uo_classes/4_2016_summer/boyana/grading assignment_2
        ag_cfg = os.path.join( sys.argv[2], AgGlobals.AUTOGRADER_CFG_NAME )
        ag = Autograder( ag_cfg )
        if ag.created():
            if ag.validate_config():
                if ag.load_assignment( sys.argv[3] ):
                    if ag.load_problems():
                        ag.compile()

    elif sys.argv[1] == 'link':
        # Link object files belonging to this assignment / project
        # Assignment and its problems must be compiled before running this command
        # Command:
        #     $ python Autograder.py link <path to autograder root directory> <assignment / project name>
        # Test Parameters
        #    link /home/users/manu/Documents/manujinda/uo_classes/4_2016_summer/boyana/grading assignment_2
        ag_cfg = os.path.join( sys.argv[2], AgGlobals.AUTOGRADER_CFG_NAME )
        ag = Autograder( ag_cfg )
        if ag.created():
            if ag.validate_config():
                if ag.load_assignment( sys.argv[3] ):
                    if ag.load_problems():
                        ag.link()


    elif sys.argv[1] == 'genout':
        # Generate reference outputs for test input
        # Assignment and its problems must be compiled before running this command
        # Command:
        #     $ python Autograder.py genout <path to autograder root directory> <assignment / project name>
        # Test Parameters
        #    genout /home/users/manu/Documents/manujinda/uo_classes/4_2016_summer/boyana/grading assignment_2
        ag_cfg = os.path.join( sys.argv[2], AgGlobals.AUTOGRADER_CFG_NAME )
        ag = Autograder( ag_cfg )
        if ag.created():
            if ag.validate_config():
                if ag.load_assignment( sys.argv[3] ):
                    if ag.load_problems():
                        ag.generate_output()


    elif sys.argv[1] == 'grading':
        # Perform grading
        # Students, Assignment and its problems must be loaded before running this command
        # Command:
        #     $ python Autograder.py grading <path to autograder root directory> <assignment / project name>
        # Test Parameters
        #    grading /home/users/manu/Documents/manujinda/uo_classes/4_2016_summer/boyana/grading assignment_2
        ag_cfg = os.path.join( sys.argv[2], AgGlobals.AUTOGRADER_CFG_NAME )
        ag = Autograder( ag_cfg )
        if ag.created():
            if ag.validate_config():
                if ag.load_assignment( sys.argv[3] ):
                    if ag.load_problems():
                        if ag.read_students():
                            if ag.load_input():
                                if len( sys.argv ) > 5:
                                    if sys.argv[4] == '-s':
                                        ag.do_grading2( stud_no = sys.argv[5] )
                                    elif sys.argv[4] == '-p':
                                        ag.do_grading2( prob_no = sys.argv[5] )
                                    elif sys.argv[4] == '-sp' and len( sys.argv ) > 6:
                                        ag.do_grading2( stud_no = sys.argv[5], prob_no = sys.argv[6] )
                                else:
                                    ag.do_grading2()
                            else:
                                print 'Error: Inputs not loaded. Exiting...'
                        else:
                            print 'Error: Students not loaded. Exiting...'
                    else:
                        print 'Error: Problems not loaded. Exiting...'
                else:
                    print 'Error: Assignment not loaded. Exiting...'
            else:
                print 'Error: Invalid autograder directory configuration. Exiting...'
        else:
            print 'Error: Autograder not properly created. Exiting...'


    elif sys.argv[1] == 'setasmnt':
        ag = Autograder( sys.argv[2] )
        if ag.validate_config():
            ag.read_students()
            ag.load_assignment()
    elif sys.argv[1] == 'update':
        # Clone / update student repositories into local hard disk
        # Prior to this a grading root directory structure should be in place
        # Command:
        #    $ python Autograder.py update <path to autograder root directory>
        # Test Parameters
        #    update /home/users/manu/Documents/manujinda/uo_classes/4_2016_summer/boyana/grading
        ag_cfg = os.path.join( sys.argv[2], AgGlobals.AUTOGRADER_CFG_NAME )
        ag = Autograder( ag_cfg )
        if ag.validate_config():
            ag.read_students()
            ag.update_repos()
    elif sys.argv[1] == 'copy':
        ag_cfg = os.path.join( sys.argv[2], AgGlobals.AUTOGRADER_CFG_NAME )
        ag = Autograder( ag_cfg )
        if ag.validate_config():
            ag.read_students()
            ag.update_repos()
            ag.copy_files_for_grading()
else:
    print 'Error: Invalid Command'
    print '\t{}'.format( ' '.join( sys.argv ) )
    exit()
