"""
    autograder.py
    Combines everything and performs autograding of a single project / assignemnt
"""
import ConfigParser
import csv
import os
import shutil
import sys

from Problem import Problem  # Just to access its instance variables to generate a sample configuratin file
from Project import Project
from Student import Student


# import Project
class Autograder( object ):

    def __init__( self ):

        self.proj = Project()

        # self.read_config()
        self.setup_project()

        if not self.validate_config():
            sys.exit()

        self.read_students()

        self.proj.check_provided_files()


    @classmethod
    def setup( self, config_file ):
        '''
            Read the autograder configuration file and setup an autograder directory tree for grading
            projects / assignments for a particular offering of a particular class
        '''
        if not os.path.exists( config_file ):
            print 'Error: Autograder Configuration File {} does not exist. Exit...'.format( config_file )
            sys.exit( 0 )

        config = ConfigParser.SafeConfigParser()
        config.read( config_file )

        # All the grading for a particular offering of a particular class happens under this director
        self.grading_root = config.get( 'Autograder Setup', 'grading_root' )

        # This is where all the supplied files / solutions etc are kept for each project / assignment.
        # For each project / assignment, there is a separate directory in this directory
        self.grading_master = config.get( 'Autograder Setup', 'grading_master' )

        if os.path.exists( self.grading_root ):
            print 'Error: Autograder grading root directory {} already exists. Exit...'.format( self.grading_root )
            sys.exit( 0 )

        students_directory = 'students'
        grading_directory = 'grading'

        os.mkdir( self.grading_root )
        os.mkdir( os.path.join( self.grading_root, self.grading_master ) )

        # All the student git repos are cloned in this directory
        os.mkdir( os.path.join( self.grading_root, students_directory ) )

        # All the compiling and grading of student submission happens here.
        # Foe each student there is a directory with the cloned student repo name in this directory.
        os.mkdir( os.path.join( self.grading_root, grading_directory ) )

        # Copy the autograder configuration file to autograder directory for later usage
        shutil.copy2( config_file, os.path.join( self.grading_root, 'autograder.cfg' ) )

        # Create the skeleton of the student data csv file
        student_db = os.path.join( self.grading_root, students_directory, 'students.csv' )
        with open( student_db, 'wb' ) as students:
            writer = csv.writer( students, delimiter = ',', quotechar = '|', quoting = csv.QUOTE_MINIMAL )
            writer.writerow( ['No', ' UO ID', ' Duck ID', ' Last Name', ' First Name', ' Email', ' Dir Name', ' Repo'] )

        # Create an example assignment directory and configuration files
        assignment1_config = ConfigParser.SafeConfigParser()
        assignment1_config.add_section( 'Assignment1' )
#         assignment1_config.set( 'Assignment1', 'no', '1 # insert the assignment number before the # sign' )
#         assignment1_config.set( 'Assignment1', 'name', 'hello world # insert the assignment name before the # sign' )
#         assignment1_config.set( 'Assignment1', 'duedate', '6/28/2016 # insert the due date before the # sign. Format mm/dd/yyyy' )
#         assignment1_config.set( 'Assignment1', 'subdir', 'assignment1 # This is the directory name where files for this assignment is stored' )
#         assignment1_config.set( 'Assignment1', 'problems', '1 2 # insert the different problem names / numbers of this assignment. Use spaces to separate problems' )

        assignemnt = Project()
        for key in sorted( assignemnt.__dict__.keys() ):
            assignment1_config.set( 'Assignment1', key, ' {}'.format( assignemnt.__dict__[key] ) )
        assignment1_config.set( 'Assignment1', '_4_gradingroot', self.grading_root )


        assignment1 = os.path.join( self.grading_root, self.grading_master, 'assignment1' )
        os.mkdir( assignment1 )

        with open( os.path.join( assignment1, 'assignment1.cfg' ), 'wb' ) as configfile:
            assignment1_config.write( configfile )

        # create a temporary Problem object so that we can access
        # its instance variable names.
        # temp.__dict__ provides the instances variables of object
        # temp as instance variable name --> instance variable value
        for p in range( 1, 3 ):
            temp = Problem( p )
            prob_config = ConfigParser.SafeConfigParser()
            section = 'problem_{}'.format( p )
            prob_config.add_section( section )
            for key in sorted( temp.__dict__.keys() ):
                prob_config.set( section, key, ' {}'.format( temp.__dict__[key] ) )

            with open( os.path.join( assignment1, section + '.cfg' ), 'wb' ) as configfile:
                prob_config.write( configfile )

        print 'Setting up autograder directory structure completed successfully'


    def setup_project( self ):

        # # self.config_file = input('Enter the path to the project configuration csv file : ')
        # self.config_file = raw_input('\nEnter the path to the project configuration csv file : ')
        print '\nEnter the path to the project configuration csv file : '
        self.config_file = 'C:\\Users\\manujinda\\Documents\\++grading\\assignments\\assignment1\\assignment1.csv'
        print self.config_file

        self.proj.setup_project( self.config_file )


    def validate_config( self ):
        # Check whether the grading root directory exisits.
        # All the student submissions and project definitions are stored
        # under this directory.
        # gradingroot\
        #       assignments\
        #           assignment1\
        #           assignment2\
        #       stud1
        #           assignment1\
        #           assignment2\
        #       stud2
        #           assignment1\
        #           assignment2\
        if not os.path.exists( self.proj.get_gradingroot() ):
            print '\nGrading root directory {} does not exist, exit...'.format( self.proj.gradingroot )
            return False
            # sys.exit()

        # self.proj.masterdir = os.path.join( self.proj.gradingroot, 'assignments', self.proj.subdir )

        # Check whether the project master directory exisits.
        # This is where all the solution and provided files are stored
        if not os.path.exists( self.proj.get_masterdir() ):
            print '\nMaster directory {} does not exist, exit...'.format( self.proj.masterdir )
            return False
            # sys.exit()

        return True

    def read_students( self ):
        if not self.validate_config():
            sys.exit()

        students = os.path.join( self.proj.get_gradingroot(), 'students.csv' )

        if not os.path.exists( students ):
            print '\nStudnt data file {} does not exist, exit...'.format( students )
            sys.exit()

        with open( students ) as student_db:
            reader = csv.DictReader( student_db )
            for row in reader:
                stud = Student( row )
                print '{}\n'.format( stud )
                self.check_student_directory( stud )


    def check_student_directory( self, student ):
        try:
            stud_dir = os.path.join( self.proj.gradingroot, student.get_dir() )
            if not os.path.exists( stud_dir ):
                print '\nStudnt directory {} for {} does not exist, creating it...'.format( student.get_dir(), student.get_name() )
                os.mkdir( stud_dir )
        except AttributeError:
            print '\nInput parameter should be of type Student'


if len( sys.argv ) > 2:
    if sys.argv[1] == 'setup':
        if os.path.exists( sys.argv[2] ):
            prog = Autograder.setup( os.path.join( os.getcwd(), 'autograder.cfg' ) )
