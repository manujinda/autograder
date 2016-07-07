'''
Created on Jul 28, 2016
Encapsulates a single project / assignment / homework

@author: manujinda
'''

import csv
import datetime
import os
import sys

from Problem import Problem


class Project( object ):
    """
        A collection of problems that are bundled together as a project.
        Has a common due date.
    """
    def __init__( self ):
        self.proj_no = 0
        self.name = ''
        self.duedate = datetime.date( 2016, 6, 28 )
        self.gradingroot = ''

        # This is the sub-directory in which each student submits his/her
        # solutions to the project. Each student creates a sub-directory
        # in his or her repo. When cloned each student directory will have
        # a sub-directory by this name. Further, the master director for a
        # particular project is also named with this.
        self.subdir = ''

        # IDs of problems that comprises this project
        self.problem_ids = []

        # ID --> Problem mapping. Problem is an object of class Problem
        # Each Problem encapsulated the details of that problem.
        self.problems = {}


    '''
    Read the project configuration file and initialize the project
    instance variables.

    Before starting actual grading, this method can be used to generate
    Problem configuration file skeletons so that they can be filled with
    appropriate data to be used during the auto grading
    '''
    def setup_project( self, config_path ):

        # Check whether the project configuration file exists.
        if not os.path.exists( config_path ):
            print '\nConfiguration file {} does not exist, exit...'.format( config_path )
            sys.exit()

        # config_dict = {}
        with open( config_path ) as config_file:
            reader = csv.DictReader( config_file )
            for row in reader:
                # self.__dict__[row['Key']] = row['Value']
                key = row['Key'].strip()
                value = row[' Value'].strip()
                if key == 'proj_no':
                    self.proj_no = int( value )
                elif key == 'name':
                    self.name = value
                elif key == 'duedate':
                    self.duedate = datetime.datetime.strptime( value, '%m/%d/%Y' )
                elif key == 'gradingroot':
                    self.gradingroot = value
                elif key == 'subdir':
                    self.subdir = value
                elif key == 'problems':
                    self.problem_ids = value.split()
                # config_dict[row['Key']] = row['Value']

        generate = raw_input( '\nGenerate Project Skeleton ( y / n ) : ' )

        if ( generate == 'y' ):
            self.generate_problem_config()
        else:
            self.setup_problem()


    '''
    Set up the problems that constitutes this project
    '''
    def setup_problem( self ):
        masterdir = self.get_masterdir()
        for p in self.problem_ids:
            prob_conf = os.path.join( masterdir, 'prob_' + p + '.csv' )
            # print prob_conf

            # Check whether the problem configuration file exists.
            if not os.path.exists( prob_conf ):
                print '\nProblem configuration file {} does not exist, exit...'.format( prob_conf )
                sys.exit()

            self.problems[p] = Problem( p )

            self.problems[p].setup_problem( prob_conf )

        for p in self.problems.keys():
            print self.problems[p]


    '''
    Generate problem configurtion files
    '''
    def generate_problem_config( self ):
        # asgnmt_root = os.path.join( self.gradingroot, 'assignments', self.subdir )
        masterdir = self.get_masterdir()

        if not os.path.exists( masterdir ):
            os.mkdir( masterdir )

        for p in self.problem_ids:
            prob_conf = os.path.join( masterdir, 'prob_' + p + '.csv' )
            with open( prob_conf, 'wb' ) as config_file:
                # writer = csv.DictWriter( config_file )
                writer = csv.writer( config_file, delimiter = ',', quotechar = '|', quoting = csv.QUOTE_MINIMAL )
                # writer.writerow( ['Key', '{} {}'.format( ' ', 'Value' )] )
                writer.writerow( ['Key', ' Value'] )

                # create a temporary Problem object so that we can access
                # its instance variable names.
                # temp.__dict__ provides the instances variables of object
                # temp as instance variable name --> instance variable value
                temp = Problem( p )
                for key in sorted( temp.__dict__.keys() ):
                    # writer.writerow( [key , '{} {}'.format( ' ', temp.__dict__[key] )] )
                    writer.writerow( [key , ' {}'.format( temp.__dict__[key] )] )


    '''
    This is the root directory where all the grading for a particular
    class is handled. The directory structure used is as follows:
        gradingroot\
              assignments\
                  assignment1\
                  assignment2\
              stud1
                  assignment1\
                  assignment2\
              stud2
                  assignment1\
                  assignment2\
    '''
    def get_gradingroot( self ):
        return self.gradingroot


    '''
    masterdir is the directory where all the project related stuff that are
    supplied to students and grading related stuff are kept.
    These include supplied code, makefiles, project configuration file,
    problem configuration files, template answer files.
    '''
    def get_masterdir( self ):
        return os.path.join( self.gradingroot, 'assignments', self.subdir )


    '''
    Check provided files in the master directory
    '''
    def check_provided_files( self ):
        files = set()
        for p in self.problems.keys():
            files.update( set( self.problems[p].get_files_provided() ) )
            # print self.problems[p].get_files_provided()

        master = self.get_masterdir()
        for f in files:
            file_path = os.path.join( master, f )
            if not os.path.exists( file_path ):
                print 'Provided file {} does not exist in the master directory. Creating...'.format( f )

    '''
    Check submitted files in the master directory
    '''
    def check_submitted_files( self ):
        files = set()
        for p in self.problems.keys():
            files.update( set( self.problems[p].get_files_submitted() ) )

        master = self.get_masterdir()
        for f in files:
            file_path = os.path.join( master, f )
            if not os.path.exists( file_path ):
                print 'Submitted file {} does not exist in the master directory. Creating...'.format( f )




# p = Project()
# p.test_meth()
