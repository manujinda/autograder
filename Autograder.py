"""
    autograder.py
    Combines everything and peforms autograding of a single project / assignemnt
"""
import csv
import datetime
import os
import sys

from Project import Project


# import Project
class Autograder( object ):

    def __init__( self ):

        self.proj = Project()

        # self.read_config()
        self.setup_project()

        self.validate_config()


    def setup_project( self ):

        # self.config_file = input('Enter the path to the project configuration csv file : ')
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
        #       assignment\
        #           assignment1\
        #           assignment2\
        #       stud1
        #           assignment1\
        #           assignment2\
        #       stud2
        #           assignment1\
        #           assignment2\
        if not os.path.exists( self.proj.gradingroot ):
            print '\nGrading root directory {} does not exist, exit...'.format( self.proj.gradingroot )
            sys.exit()

        self.proj.masterdir = os.path.join( self.proj.gradingroot, 'assignments', self.proj.subdir )

        # Check whether the project master directory exisits.
        # This is where all the solution and provided files are stored
        if not os.path.exists( self.proj.masterdir ):
            print '\nMaster directory {} does not exist, exit...'.format( self.proj.masterdir )
            sys.exit()


proj = Autograder()
