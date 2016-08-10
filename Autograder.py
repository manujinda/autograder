"""
    autograder.py
    Combines everything and performs autograding of a single project / assignemnt
"""
import ConfigParser
import csv
import os
import shutil
import sys

from AgGlobals import AgGlobals
from Assignment import Assignment
from Problem import Problem  # Just to access its instance variables to generate a sample configuration file
from Repository import Repository
from Student import Student


class Autograder( object ):

    def __init__( self, config_file ):

        self.ag_created = False

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

        # All the grading for a particular offering of a particular class happens under this director
        self.grading_root = config.get( 'Autograder Setup', 'grading_root' )

        # This is where all the supplied files / solutions etc are kept for each project / assignment.
        # For each project / assignment, there is a separate directory in this directory
        self.grading_master = config.get( 'Autograder Setup', 'grading_master' )

        self.students = []

        self.asmnt = Assignment()

        # To get access to autograder global standards such as
        # file naming conventions
        self.agg = AgGlobals()
        self.students_directory = self.agg.get_students_directory()
        self.grading_directory = self.agg.get_grading_directory()
        self.asmnt_loaded = False  # Keeps track of whether a valid assignment configuration file has been loaded

        self.ag_created = True



    def created( self ):
        return self.ag_created


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
        shutil.copy2( self.config_file, os.path.join( self.grading_root, self.agg.get_autograder_cfg_name() ) )

        # Create the skeleton of the student data csv file
        student_db = os.path.join( self.grading_root, self.students_directory, self.agg.get_students_db_name() )
        with open( student_db, 'wb' ) as students:
            writer = csv.writer( students, delimiter = ',', quotechar = '|', quoting = csv.QUOTE_MINIMAL )
            writer.writerow( ['No', 'UO ID', 'Duck ID', 'Last Name', 'First Name', 'Email', 'Dir Name', 'Repo'] )

        # Create an example assignment directory and configuration files
        # assignment = Assignment()
        assignment_name = '{}_{}'.format( self.grading_master[:-1], 1 )  # 'assignment1'
        assignment = self.new_assignment( assignment_name )
        # assignment.new_assignment( self.grading_root, self.grading_master, assignment_name )

        # Populate the assignment with the just created assignment configuration file
        assignment.setup_assignment( self.grading_root, self.grading_master, assignment_name )
        assignment.generate_problem_config()

        print 'Setting up autograder directory structure completed successfully'


    ''' Generate a new blank assignment.
        Creates the directory and the default assignment configuration file '''
    def new_assignment( self, assignment_name ):

        # Create an example assignment directory and configuration files
        assignment = Assignment()
        assignment.new_assignment( self.grading_root, self.grading_master, assignment_name )

        return assignment



    def setup_assignment( self, assignment_name ):

        # print '\nEnter the assignment master sub-directory name : '
        # self.assignment_master_sub_dir = '{}_{}'.format( self.grading_master[:-1], 1 )  # 'assignment1'

        self.asmnt_loaded = self.asmnt.setup_assignment( self.grading_root, self.grading_master, assignment_name )

        return self.asmnt_loaded


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

        return True


    def read_students( self ):
        if not self.validate_config():
            sys.exit()

        students = os.path.join( self.grading_root, self.students_directory, 'students.csv' )

        if not os.path.exists( students ):
            print '\nStudnt data file {} does not exist, exit...'.format( students )
            sys.exit()

        with open( students ) as student_db:
            reader = csv.DictReader( student_db )
            for row in reader:
                stud = Student( row )
                self.students.append( stud )
                # print '{}\n'.format( stud )
                # self.check_student_directory( stud )


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
    def copy_files_to_grading( self ):
        index_len = len( '{}'.format( self.students[-1].get_index() ) )
        source = os.path.join( self.grading_root, self.students_directory )
        destination = os.path.join( self.grading_root, self.grading_directory )
        for stud in self.students:
            stud.copy_student_repo( source, destination, stud.get_dir( index_len ) )


    def check_student_directory( self, student ):
        try:
            stud_dir = os.path.join( self.asmnt.gradingroot, student.get_dir() )
            if not os.path.exists( stud_dir ):
                print '\nStudnt directory {} for {} does not exist, creating it...'.format( student.get_dir(), student.get_name() )
                os.mkdir( stud_dir )
        except AttributeError:
            print '\nInput parameter should be of type Student'


    '''
    If a valid assignment configuration file has been loaded, this will generate necessary problem configuration file
    '''
    def gen_prob_config_skel( self ):
        if self.asmnt_loaded:
            self.asmnt.generate_problem_config()


    def setup_problems( self ):
        if self.asmnt_loaded:
            self.asmnt.setup_problems()



agg = AgGlobals()

if len( sys.argv ) > 2:
    if sys.argv[1] == 'setup':
        # Setup the initial directory tree for grading one instance of a class
        # Need to run once at the begining of the semester / term / quater
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
        ag_cfg = os.path.join( sys.argv[2], agg.get_autograder_cfg_name() )
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
        ag_cfg = os.path.join( sys.argv[2], agg.get_autograder_cfg_name() )
        ag = Autograder( ag_cfg )
        if ag.created():
            if ag.validate_config():
                if ag.setup_assignment( sys.argv[3] ):
                    ag.gen_prob_config_skel()
                # ag.setup_problems()

    elif sys.argv[1] == 'setasmnt':
        ag = Autograder( sys.argv[2] )
        if ag.validate_config():
            ag.read_students()
            ag.setup_assignment()
    elif sys.argv[1] == 'update':
        ag = Autograder( sys.argv[2] )
        if ag.validate_config():
            ag.read_students()
            ag.update_repos()
    elif sys.argv[1] == 'copy':
        ag = Autograder( sys.argv[2] )
        if ag.validate_config():
            ag.read_students()
            ag.update_repos()
            ag.copy_files_to_grading()
