"""
    autograder.py
    Combines everything and performs autograding of a single project / assignemnt
"""
import ConfigParser
import csv
import os
import shutil
import sys

from Problem import Problem  # Just to access its instance variables to generate a sample configuration file
from Project import Project
from Repository import Repository
from Student import Student


class Autograder( object ):

    def __init__( self, config_file ):

        self.students_directory = 'students'
        self.grading_directory = 'grading'
        self.config_file = config_file
        self.proj_loaded = False  # Keeps track of whether a valid project configuration file has been loaded

        '''
            Read the autograder configuration file and populate grading root
            and grading master directory names
        '''
        if not os.path.exists( self.config_file ):
            print 'Error: Autograder Configuration File {} does not exist. Exit...'.format( config_file )
            sys.exit( 0 )

        config = ConfigParser.SafeConfigParser()
        config.read( self.config_file )

        # All the grading for a particular offering of a particular class happens under this director
        self.grading_root = config.get( 'Autograder Setup', 'grading_root' )

        # This is where all the supplied files / solutions etc are kept for each project / assignment.
        # For each project / assignment, there is a separate directory in this directory
        self.grading_master = config.get( 'Autograder Setup', 'grading_master' )

        self.students = []

        self.proj = Project()
#
#         # self.read_config()
#         self.setup_project()
#
#         if not self.validate_config():
#             sys.exit()
#
#         self.read_students()
#
#         self.proj.check_provided_files()


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
        shutil.copy2( self.config_file, os.path.join( self.grading_root, 'autograder.cfg' ) )

        # Create the skeleton of the student data csv file
        student_db = os.path.join( self.grading_root, self.students_directory, 'students.csv' )
        with open( student_db, 'wb' ) as students:
            writer = csv.writer( students, delimiter = ',', quotechar = '|', quoting = csv.QUOTE_MINIMAL )
            writer.writerow( ['No', 'UO ID', 'Duck ID', 'Last Name', 'First Name', 'Email', 'Dir Name', 'Repo'] )

        # Create an example assignment directory and configuration files
        assignment_name = 'assignment1'
        assignment_config = ConfigParser.SafeConfigParser()
        assignment_config.add_section( assignment_name )
#         assignment1_config.set( 'Assignment1', 'no', '1 # insert the assignment number before the # sign' )
#         assignment1_config.set( 'Assignment1', 'name', 'hello world # insert the assignment name before the # sign' )
#         assignment1_config.set( 'Assignment1', 'duedate', '6/28/2016 # insert the due date before the # sign. Format mm/dd/yyyy' )
#         assignment1_config.set( 'Assignment1', 'subdir', 'assignment1 # This is the directory name where files for this assignment is stored' )
#         assignment1_config.set( 'Assignment1', 'problems', '1 2 # insert the different problem names / numbers of this assignment. Use spaces to separate problems' )

        assignemnt = Project()
        for key in sorted( assignemnt.__dict__.keys() ):
            assignment_config.set( assignment_name, key, ' {}'.format( assignemnt.__dict__[key] ) )
        # assignment1_config.set( 'assignment1', '_4_gradingroot', self.grading_root )


        assignment_path = os.path.join( self.grading_root, self.grading_master, assignment_name )
        os.mkdir( assignment_path )

        with open( os.path.join( assignment_path, '+_1_{}.cfg'.format( assignment_name ) ), 'wb' ) as configfile:
            assignment_config.write( configfile )

        # create a temporary Problem object so that we can access
        # its instance variable names.
        # temp.__dict__ provides the instances variables of object
        # temp as instance variable name --> instance variable value
        prob_config = ConfigParser.SafeConfigParser()
        for p in range( 1, 3 ):
            temp = Problem( p )
#            prob_config = ConfigParser.SafeConfigParser()
            section = '{}_problem_{}'.format( assignment_name, p )
            prob_config.add_section( section )
            for key in sorted( temp.__dict__.keys() ):
                prob_config.set( section, key, ' {}'.format( temp.__dict__[key] ) )

        with open( os.path.join( assignment_path, '+_2_{}_problems.cfg'.format( assignment_name ) ), 'wb' ) as configfile:
            prob_config.write( configfile )

        print 'Setting up autograder directory structure completed successfully'


    def setup_project( self ):

        # # self.config_file = input('Enter the assignment master sub-directory name ')
        # self.config_file = raw_input('\nEnter the assignment master sub-directory name ')
        print '\nEnter the assignment master sub-directory name : '
        self.assignment_master_sub_dir = 'assignment1'

        self.proj_loaded = self.proj.setup_project( self.grading_root, self.grading_master, self.assignment_master_sub_dir )


    def validate_config( self ):
        # Check whether the grading root directory exists.
        # All the student submissions and project definitions are stored
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

        # self.proj.masterdir = os.path.join( self.proj.gradingroot, 'assignments', self.proj.subdir )

        # Check whether the project master directory exists.
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
            print '\nMaster directory {} does not exist, exit...'.format( students )
            return False
            # sys.exit()

        # Check whether the grading directory exists.
        # This is where all grading happens.
        grading = os.path.join( self.grading_root, self.grading_directory )
        if not os.path.exists( grading ):
            print '\nMaster directory {} does not exist, exit...'.format( grading )
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
            stud_dir = os.path.join( self.proj.gradingroot, student.get_dir() )
            if not os.path.exists( stud_dir ):
                print '\nStudnt directory {} for {} does not exist, creating it...'.format( student.get_dir(), student.get_name() )
                os.mkdir( stud_dir )
        except AttributeError:
            print '\nInput parameter should be of type Student'


    '''
    If a valid project configuration file has been loaded, this will generate necessary problem configuration file
    '''
    def gen_prob_config_skel( self ):
        if self.proj_loaded:
            self.proj.generate_problem_config()


    def setup_problems( self ):
        if self.proj_loaded:
            self.proj.setup_problems()



if len( sys.argv ) > 2:
    ag = Autograder( sys.argv[2] )
    if sys.argv[1] == 'setup':
        if os.path.exists( sys.argv[2] ):
            ag.setup_grading_dir_tree()
    elif sys.argv[1] == 'setproj':
        if ag.validate_config():
            ag.read_students()
            ag.setup_project()
    elif sys.argv[1] == 'update':
        if ag.validate_config():
            ag.read_students()
            ag.update_repos()
    elif sys.argv[1] == 'copy':
        if ag.validate_config():
            ag.read_students()
            ag.update_repos()
            ag.copy_files_to_grading()
    elif sys.argv[1] == 'genprob':
        if ag.validate_config():
            ag.setup_project()
            ag.gen_prob_config_skel()
            ag.setup_problems()
