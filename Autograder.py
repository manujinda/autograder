"""
    autograder.py
    Combines everything and performs autograding of a single project / assignemnt
"""
import ConfigParser
from __builtin__ import True
import csv
from datetime import datetime
import os
import shutil
import sys

from AgGlobals import AgGlobals
from Assignment import Assignment
from Command import Command
from Problem import Problem  # Just to access its instance variables to generate a sample configuration file
from Repository import Repository
from Student import Student


class Autograder( object ):

    def __init__( self, config_file ):

        # self.ag_created = False

        '''
            Read the autograder configuration file and populate grading root
            and grading master directory names
        '''
        if not os.path.exists( config_file ):
            print 'Error: Autograder Configuration File {} does not exist. Exit...'.format( config_file )
            sys.exit( 0 )

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


        self.students = []

        self.asmnt = Assignment()

        self.students_directory = AgGlobals.STUDENTS_DIRECTORY  # self.agg.get_students_directory()
        self.grading_directory = AgGlobals.GRADING_DIRECTORY  # self.agg.get_grading_directory()
        # self.asmnt_loaded = False  # Keeps track of whether a valid assignment configuration file has been loaded

        # self.ag_created = True
        self.ag_state = AgGlobals.AG_STATE_CREATED



    def created( self ):
        # return self.ag_created
        return AgGlobals.is_flags_set( self.ag_state, AgGlobals.AG_STATE_CREATED )


    # @classmethod
    '''
        Setup an autograder directory tree for grading
        projects / assignments for a particular offering
        of a particular class
    '''
    def setup_grading_dir_tree( self ):
        if os.path.exists( self.grading_root ):
            print 'Error: Autograder grading root directory {} already exists. Exit...'.format( self.grading_root )
            sys.exit( 0 )

#         students_directory = 'students'
#         grading_directory = 'grading'

        os.mkdir( self.grading_root )
        os.mkdir( os.path.join( self.grading_root, self.grading_master ) )

        # All the student git repos are cloned in this directory
        os.mkdir( os.path.join( self.grading_root, self.students_directory ) )

        # All the compiling and grading of student submission happens here.
        # Foe each student there is a directory with the cloned student repo name in this directory.
        os.mkdir( os.path.join( self.grading_root, self.grading_directory ) )

        # Copy the autograder configuration file to autograder directory for later usage
        shutil.copy2( self.config_file, os.path.join( self.grading_root, AgGlobals.AUTOGRADER_CFG_NAME ) )

        # Create the skeleton of the student data csv file
        student_db = os.path.join( self.grading_root, self.students_directory, AgGlobals.STUDENT_DB )
        with open( student_db, 'wb' ) as students:
            writer = csv.writer( students, delimiter = ',', quotechar = '|', quoting = csv.QUOTE_MINIMAL )
            writer.writerow( AgGlobals.STUDENT_DB_FIEDLS )

        # Create an example assignment directory and configuration files
        assignment_name = '{}_{}'.format( self.grading_master[:-1], 1 )  # 'assignment1'
        assignment = self.new_assignment( assignment_name )

        # Populate the assignment with the just created assignment configuration file
        assignment.load_assignment( self.grading_root, self.grading_master, assignment_name )
        assignment.generate_problem_config()

        print 'Setting up autograder directory structure completed successfully'


    ''' Generate a new blank assignment.
        Creates the directory and the default assignment configuration file '''
    def new_assignment( self, assignment_name ):

        # Create an example assignment directory and configuration files
        assignment = Assignment()
        assignment.new_assignment( self.grading_root, self.grading_master, assignment_name )

        return assignment



    def load_assignment( self, assignment_name ):

        # print '\nEnter the assignment master sub-directory name : '
        # self.assignment_master_sub_dir = '{}_{}'.format( self.grading_master[:-1], 1 )  # 'assignment1'

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
            print '\nGrading root directory {} does not exist, exit...'.format( self.grading_root )
            return False
            # sys.exit()

        # self.asmnt.masterdir = os.path.join( self.asmnt.gradingroot, 'assignments', self.asmnt.subdir )

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

        self.students = []
        with open( students ) as student_db:
            reader = csv.DictReader( student_db )
            for row in reader:
                stud = Student( row )
                self.students.append( stud )
                # print '{}\n'.format( stud )
                # self.check_student_directory( stud )

        return len( self.students ) > 0

#     def clone_repos( self ):
#         # When student database is sorted in the ascending order of  student index numbers
#         # the length of the index number of the last student is the longest. Get the length
#         # of that index number and pass that to the cloning method so that when creating the
#         # local student repository directory name each directory have the index number of each
#         # student prefixed to student name in such a way prefixed index numbers have the same
#         # length with 0s padded in the left. e.g. 003_manujinda
#         index_len = len( '{}'.format( self.students[-1].get_index() ) )
#         for stud in self.students:
#             stud_dir = os.path.join( self.grading_root, self.students_directory, stud.get_dir( index_len ) )
#             if not os.path.exists( stud_dir ):
#                 stud.clone_student_repo( stud_dir )
#             else:
#                 print 'Repository path {} already exists'.format( stud_dir )

    def update_repos( self ):
        # When student database is sorted in the ascending order of  student index numbers
        # the length of the index number of the last student is the longest. Get the length
        # of that index number and pass that to the cloning method so that when creating the
        # local student repository directory name each directory have the index number of each
        # student prefixed to student name in such a way prefixed index numbers have the same
        # length with 0s padded in the left. e.g. 003_manujinda
        index_len = len( '{}'.format( self.students[-1].get_index() ) )
        for stud in self.students:
            stud_dir = os.path.join( self.grading_root, self.students_directory, stud.get_dir( index_len ) )
            if not os.path.exists( stud_dir ):
                # Student repository has not been cloned. Have to clone it first
                stud.clone_student_repo( stud_dir )
            else:
                stud.pull_student_repo( stud_dir )



    '''
    Copying files from cloned student repos to student grading folders.
    At the moment I'm making use of git itself to do the job. I clone the
    cloned student repo in students directory to the grading directory.
    If this has any bad implications I'd have to copy files using
    OS file copy utilities.
    '''
    def do_grading( self ):
        # If students are loaded and problems are loaded
        if len( self.students ) > 0 and AgGlobals.is_flags_set( self.ag_state, AgGlobals.AG_STATE_ASSIGNMENT_LOADED, AgGlobals.AG_STATE_PROBLEMS_LOADED, AgGlobals.AG_STATE_INPUTS_LOADED ) :

            # This is the path for the students directory
            source = os.path.join( self.grading_root, self.students_directory )

            # This is the path for the grading directory
            destination = os.path.join( self.grading_root, self.grading_directory )

            # Length of the longest student index. This is used to insert
            # leading 0's in the student directory name
            index_len = len( '{}'.format( self.students[-1].get_index() ) )

            # Get a dictionary of submitted file names and their aliases
            # submitted_file_name --> set(alias1, alias2, ...)
            file_aliases = self.asmnt.get_files_submitted_with_aliases()

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

            # Open grading log file for this student
            grading_log = open( os.path.join( asmnt_master_sub_dir, AgGlobals.AUTOGRADER_LOG_FILE_NAME ), 'a' )
            AgGlobals.write_to_log( grading_log, '\n{0}<< Grading Session on {1} : START >>{0}\n'.format( '-' * 20, datetime.now() ) )

            # For each student
            for stud in self.students:

                AgGlobals.write_to_log( grading_log, '\n{0} Student: {1} {0}\n'.format( '#' * 10, stud.get_name() ) )

                # Student's directory name
                stud_dir_name = stud.get_dir( index_len )

                # Path for the student's directory in the students directory
                stud_local_repo_path = os.path.join( source, stud_dir_name )

                # Path for the student's directory in the grading directory
                stud_dir_path = os.path.join( destination, stud_dir_name, self.asmnt.get_assignment_sub_dir() )

                # Update local student repository
                if not os.path.exists( stud_local_repo_path ):
                    # Student repository has not been cloned. Have to clone it first
                    stud.clone_student_repo( stud_local_repo_path, grading_log )
                else:
                    stud.pull_student_repo( stud_local_repo_path, grading_log )

                # Copy all the student submitted files from student directory in students directory
                # to a directory with the same name in the grading directory
                stud.copy_student_repo( source, destination, index_len )

                # Check whether student has created a directory with the proper name in his or her
                # repository to upload files for this assignment / project
                if not os.path.exists( stud_dir_path ):
                    print 'Error: Student {} does not have the assignment directory {} in the repository.'.format( stud.get_name(), stud_dir_path )
                    AgGlobals.write_to_log( grading_log, '\tError: {} directory does not exist in the repo\n'.format( self.asmnt.get_assignment_sub_dir() ) )
                    continue

                # For each file student is supposed to submit
                for file_submitted in file_aliases:

                    # The path for that file in the student's directory in the grading directory
                    file_path = os.path.join( stud_dir_path, file_submitted )

                    # If student has not submitted a file with the exact name
                    if not os.path.exists( file_path ):

                        # Check whether the student has submitted a file that matches an alias
                        # Alias could be a misspelled file name or a shorten file name
                        found = False
                        for file_alias in file_aliases[file_submitted]:
                            file_alias_path = os.path.join( stud_dir_path, file_alias )

                            # A file that matches an alias exists.
                            # Student might have submitted this file thinking he/she is submitting
                            # the file he/she is supposed to submit
                            if os.path.exists( file_alias_path ):
                                found = True
                                # Rename the file. Might want to do this only when we provide the make file
                                cmd = 'mv {} {}'.format( file_alias, file_submitted )
                                retcode, out, err = Command( cmd ).run( cwd = stud_dir_path )
                                AgGlobals.write_to_log( grading_log, '\tWarning: Renamed file - {} --> {}\n'.format( file_alias, file_submitted ) )
                                break

                        if not found:
                            print 'Error: Student {} has not submitted file {}'.format( stud.get_name(), file_submitted )
                            AgGlobals.write_to_log( grading_log, '\tError: File - {} - missing\n'.format( file_submitted ) )
                            continue

                # Copy the provided files into student's directory in the grading directory
                for pf_path in provided_file_paths:
                    cmd = 'cp {} .'.format( pf_path )
                    retcode, out, err = Command( cmd ).run( cwd = stud_dir_path )

                # Compile student submission
                self.asmnt.compile( stud_dir_path )

                # Link student submissions
                self.asmnt.link( stud_dir_path )

                # Run student program and generate output for test input
                output_dir = os.path.join( stud_dir_path, AgGlobals.INPUT_OUTPUT_DIRECTORY )
                self.asmnt.generate_output( output_dir )

                grading_log.flush()

            grading_log.close()

    # # !! Needs update.. student.get_dir() has been changed to get_dir(index_len)
#     def check_student_directory( self, student ):
#         try:
#             stud_dir = os.path.join( self.asmnt.gradingroot, student.get_dir() )
#             if not os.path.exists( stud_dir ):
#                 print '\nStudnt directory {} for {} does not exist, creating it...'.format( student.get_dir(), student.get_name() )
#                 os.mkdir( stud_dir )
#         except AttributeError:
#             print '\nInput parameter should be of type Student'


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

            # print self.asmnt.get_files_submitted_with_aliases()
            return result

        return False


    def generate_files( self ):
        if AgGlobals.is_flags_set( self.ag_state, AgGlobals.AG_STATE_ASSIGNMENT_LOADED ):
            self.asmnt.generate_provided_files()
            self.asmnt.generate_submitted_files()
            self.asmnt.generate_input_config()


    def load_input( self ):
        if AgGlobals.is_flags_set( self.ag_state, AgGlobals.AG_STATE_ASSIGNMENT_LOADED ):
        # if self.asmnt_loaded:
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


#     def correct_submitted_file_names( self ):
#         if len( self.students ) > 0:
#             index_len = len( '{}'.format( self.students[-1].get_index() ) )
#             for stud in self.students:
#                 directory = os.path.join( self.grading_root, self.grading_directory, stud.get_dir( index_len ), self.asmnt. )
#                 stud.copy_student_repo( source, destination,  )



if len( sys.argv ) > 2:
    if sys.argv[1] == 'setup':
        # Setup the initial directory tree for grading one instance of a class
        # Need to run once at the beginning of the semester / term / quater
        # Command:
        #    $ python Autograder.py setup <path to autograder configuration file>
        # Test Parameters
        #    setup /home/users/manu/Documents/manujinda/uo_classes/4_2016_summer/boyana/autograder_ws/autograder/autograder.cfg
        ag = Autograder( sys.argv[2] )
        if ag.created():
            ag.setup_grading_dir_tree()

    elif sys.argv[1] == 'newasmnt':
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
                                ag.do_grading()


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
