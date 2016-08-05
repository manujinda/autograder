'''
Created on Jul 28, 2016
Encapsulates a single project / assignment / homework

@author: Manujinda Wathugala
'''

import ConfigParser
import datetime
import os
import sys

from Problem import Problem


class Assignment( object ):
    """
        A collection of problems that are bundled together as an assignment.
        Has a common due date.
    """
    def __init__( self ):
        self._1_asnmt_no = '1 ; insert the assignment number before the ; sign'
        self._2_name = 'hello world ; insert the assignment name before the ; sign'
        self._3_duedate = '6/28/2016 ; insert the due date before the ; sign. Format mm/dd/yyyy'  # datetime.date( 2016, 6, 28 )
        # self._4_gradingroot = ''

        # This is the sub-directory in which each student submits his/her
        # solutions to the assignment. Each student creates a sub-directory
        # in his or her repo. When cloned each student directory will have
        # a sub-directory by this name. Further, the master director for a
        # particular assignment is also named with this.
        self._5_subdir = 'assignment1 ; This is the directory name where files for this assignment is stored'

        # IDs of problems that comprises this assignment
        self._6_problem_ids = '1:prog 2:code 3:ans 4:mcq ; insert the different problem names / numbers of this assignment followed by problem type separated by a :. Use spaces to separate problems'  # []

        # ID --> Problem mapping. Problem is an object of class Problem
        # Each Problem encapsulated the details of that problem.
        # self._8_problems = {}

        self._99_loaded = False


    def __str__( self ):
        desc = ''
        for f in sorted( self.__dict__.keys() )[:-1]:
            desc += '{} > {} \n'.format( f[3:], self.__dict__[f] )
        return desc


    '''
    Read the assignment configuration file and initialize the assignment
    instance variables.

    Before starting actual grading, this method can be used to generate
    Problem configuration file skeletons so that they can be filled with
    appropriate data to be used during the auto grading
    '''
    def setup_assignment( self, grading_root, grading_master, assignment_master_sub_dir ):

#        config_file = os.path.join( self._4_gradingroot, self._7_grading_master, self._5_subdir, '{}.cfg'.format( self._5_subdir ) )
        config_file = os.path.join( grading_root, grading_master, assignment_master_sub_dir, '+_1_{}.cfg'.format( assignment_master_sub_dir ) )

        # Check whether the assignment configuration file exists.
        if not os.path.exists( config_file ):
            print '\nConfiguration file {} does not exist, exit...'.format( config_file )
            sys.exit()

        config = ConfigParser.SafeConfigParser()
        config.read( config_file )

        for key in sorted( self.__dict__.keys() )[:-1]:
            self.__dict__[key] = config.get( assignment_master_sub_dir, key[3:] ).strip()

        self._1_asnmt_no = int( self._1_asnmt_no )
        self._3_duedate = datetime.datetime.strptime( self._3_duedate, '%m/%d/%Y' )
        self._6_problem_ids = self._6_problem_ids.split()

        self._4_gradingroot = grading_root
        self._5_subdir = assignment_master_sub_dir
        self._7_grading_master = grading_master

        temp_prob = {}
        for p in self._6_problem_ids:
            q = p.split( ':' )
            temp_prob[q[0]] = q[1]
        self._6_problem_ids = temp_prob

        print self
        self._99_loaded = True
        return True
#         generate = raw_input( '\nGenerate Assignment Skeleton ( y / n ) : ' )
#
#         if ( generate == 'y' ):
#             self.generate_problem_config()
#         else:
#             self.setup_problems()


    '''
    Set up the problems that constitutes this assignment
    '''
    def setup_problems( self ):
        if self._99_loaded:
            prob_conf = self.get_prob_config_path()
            section_prefix = '{}_problem_{}'.format( self._5_subdir, {} )
            # Check whether the problem configuration file exists.
            if not os.path.exists( prob_conf ):
                print '\nProblem configuration file {} does not exist, exit...'.format( prob_conf )
                sys.exit()

            # ID --> Problem mapping. Problem is an object of class Problem
            # Each Problem encapsulated the details of that problem.
            self._8_problems = {}

            for p in sorted( self._6_problem_ids ):
                self._8_problems[p] = Problem( p, self._6_problem_ids[p] )

                self._8_problems[p].setup_problem( prob_conf, section_prefix.format( p ) )

    #         for p in self._8_problems.keys():
    #             print self._8_problems[p]
            return True
        else:
            return False


    '''
    Generate problem configuration files
    '''
    def generate_problem_config( self ):
        if self._99_loaded:
            # asgnmt_root = os.path.join( self._4_gradingroot, 'assignments', self._5_subdir )
            assignment_path = self.get_masterdir()

            if not os.path.exists( assignment_path ):
                os.mkdir( assignment_path )

            prob_config = ConfigParser.SafeConfigParser()
            for p in sorted( self._6_problem_ids ):
                # create a temporary Problem object so that we can access
                # its instance variable names.
                # temp.__dict__ provides the instances variables of object
                # temp as instance variable name --> instance variable value
                temp = Problem( p, self._6_problem_ids[p] )
                section = '{}_problem_{}'.format( self._5_subdir, p )
                prob_config.add_section( section )
                for key in sorted( temp.__dict__.keys() ):
                    prob_config.set( section, key[4:], ' {}'.format( temp.__dict__[key] ) )

            # with open( os.path.join( assignment_path, '+_2_{}_problems.cfg'.format( self._5_subdir ) ), 'wb' ) as configfile:
            with open( self.get_prob_config_path(), 'wb' ) as configfile:
                prob_config.write( configfile )

            print 'Setting up problem configuration file skeleton completed successfully'
        else:
            print 'Error: Need to load an assignment configuration before generating problem configurations'


    '''
    Generate the path to the configuration file that holds to configuration details of problems
    where this assignment is comprised of
    '''
    def get_prob_config_path( self ):
        return os.path.join( self.get_masterdir(), '+_2_{}_problems.cfg'.format( self._5_subdir ) )


    '''
    This is the root directory where all the grading for a particular
    class is handled. The directory structure used is as follows:
        gradingroot\
              autograder.cfg
              assignments\
                  assignment1\
                  assignment2\
              grading\
                  stud1
                      assignment1\
                      assignment2\
                  stud2
                      assignment1\
                      assignment2\
              students\
                  students.csv
                  stud1
                      assignment1\
                      assignment2\
                  stud2
                      assignment1\
                      assignment2\
    '''
    def get_gradingroot( self ):
        return self._4_gradingroot


    '''
    masterdir is the directory where all the assignment related stuff that are
    supplied to students and grading related stuff are kept.
    These include supplied code, makefiles, assignment configuration file,
    problem configuration files, template answer files.
    '''
    def get_masterdir( self ):
        return os.path.join( self._4_gradingroot, self._7_grading_master, self._5_subdir )


    def get_problem_ids( self ):
        if self._99_loaded:
            return self._6_problem_ids
        else:
            return {}


    '''
    Check provided files in the master directory. If not found create those files
    '''
    def check_provided_files( self ):
        files = set()
        for p in self._7_problems.keys():
            files.update( set( self._7_problems[p].get_files_provided() ) )
            # print self._7_problems[p].get_files_provided()

        master = self.get_masterdir()
        for f in files:
            file_path = os.path.join( master, f )
            if not os.path.exists( file_path ):
                print 'Provided file {} does not exist in the master directory. Creating...'.format( f )

    '''
    Check submitted files in the master directory. If not create them
    '''
    def check_submitted_files( self ):
        files = set()
        for p in self._7_problems.keys():
            files.update( set( self._7_problems[p].get_files_submitted() ) )

        master = self.get_masterdir()
        for f in files:
            file_path = os.path.join( master, f )
            if not os.path.exists( file_path ):
                print 'Submitted file {} does not exist in the master directory. Creating...'.format( f )




# p = Assignment()
# p.test_meth()
