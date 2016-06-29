"""
    autograder.py
    Combines everything and peformes autograding of a single project / assignemnt
"""
import os
import sys
import csv
import datetime

#import Project
from Project import Project

class Autograder(object):
    
    def __init__(self):
        
        self.proj = Project()
        
        #self.read_config()
        self.setup_project()
        
        self.validate_config()


    def setup_project(self):
        
        #self.config_file = input('Enter the path to the project configuration csv file : ')
        print '\nEnter the path to the project configuration csv file : '
        #self.config_file = raw_input()
        self.config_file = 'C:\\Users\\manujinda\\Documents\\++grading\\assignments\\assignment1\\assignment1.csv'
        print self.config_file
        
        self.proj.setup_project(self.config_file)

    
    
#    def read_config(self):
#        
#        #self.config_file = input('Enter the path to the project configuration csv file : ')
#        print '\nEnter the path to the project configuration csv file : '
#        #self.config_file = raw_input()
#        self.config_file = 'C:\\Users\\manujinda\\Documents\\++grading\\assignments\\assignment1\\assignment1.csv'
#        print self.config_file
#
#        # Check whether the file exists.
#        if not os.path.exists(self.config_file):
#            print '\nConfiguration file {} does not exist, exit...'.format(self.config_file)
#            sys.exit()
#
#        #config_dict = {}
#        with open(self.config_file) as config_file:
#            reader = csv.DictReader(config_file)
#            for row in reader:
#                print row['Key'], row['Value']
#                if row['Key'] ==  'proj_no':
#                    self.proj.proj_no = int(row['Value'])
#                elif row['Key'] == 'name':
#                    self.proj.name = row['Value']
#                elif row['Key'] == 'duedate':
#                    self.proj.duedate = datetime.datetime.strptime(row['Value'], '%m/%d/%Y')
#                elif row['Key'] == 'gradingroot':
#                    self.proj.gradingroot = row['Value']
#                elif row['Key'] == 'subdir':
#                    self.proj.subdir = row['Value']
#                #config_dict[row['Key']] = row['Value']
#                
#        #print config_dict


    def validate_config(self):
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
        if not os.path.exists(self.proj.gradingroot):
            print '\nGrading root directory {} does not exist, exit...'.format(self.proj.gradingroot)
            sys.exit()

        self.proj.masterdir = os.path.join(self.proj.gradingroot, 'assignments', self.proj.subdir)
        
        # Check whether the project master directory exisits.
        # This is where all the solution and provided files are stored
        if not os.path.exists(self.proj.masterdir):
            print '\nMaster directory {} does not exist, exit...'.format(self.proj.masterdir)
            sys.exit()

                
proj = Autograder()
