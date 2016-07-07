"""
    autograder.py
    Combines everything and performs autograding of a single project / assignemnt
"""
import csv
import os
import sys

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


proj = Autograder()
