'''
Created on Jul 28, 2016
Encapsulates a single project / assignment / homework

@author: Manujinda Wathugala
'''

import ConfigParser
import datetime
import os
import sys

from AgGlobals import AgGlobals
from Input import Input
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
        # self._5_subdir = 'assignment1 ; This is the directory name where files for this assignment is stored'

        # IDs of problems that comprises this assignment
        self._6_problem_ids = '1:prog 2:code 3:ans 4:mcq ; insert the different problem names / numbers of this assignment followed by problem type separated by a :. Use spaces to separate problems'  # []

        # ID --> Problem mapping. Problem is an object of class Problem
        # Each Problem encapsulated the details of that problem.
        # self._8_problems = {}

        self._99_agg = AgGlobals()
        self._99_state = AgGlobals.INITIALIZED


    def __str__( self ):
        desc = ''
        for key in sorted( self.__dict__.keys() ):  # [:-1]:
            if key[0:4] != '_99_':
                desc += '{} > {} \n'.format( key[3:], self.__dict__[key] )
        return desc


    ''' Generate a new blank assignment.
        Creates the directory and the default assignment configuration file '''
    # @classmethod
    def new_assignment( self, grading_root, grading_master, assignment_name ):

        assignment_master_sub_dir = os.path.join( grading_root, grading_master, assignment_name )
        if not os.path.exists( assignment_master_sub_dir ):
            os.mkdir( assignment_master_sub_dir )

            assignment_config = ConfigParser.SafeConfigParser()
            assignment_config.add_section( assignment_name )

            for key in sorted( self.__dict__.keys() ):  # [:-1]:
                # Filter only the instances variables that are necessary for the configuration file
                if key[0:4] != '_99_':
                    assignment_config.set( assignment_name, key[3:], ' {}'.format( self.__dict__[key] ) )

            cfg_path = os.path.join( assignment_master_sub_dir, self._99_agg.get_asmt_cfg_name( assignment_name ) )
            with open( cfg_path, 'wb' ) as configfile:
                assignment_config.write( configfile )
            print 'Success: Blank assignment {} successfully created'.format( assignment_name )
            print 'Update the configuration file: {} as necessary to define the assignment'.format( cfg_path )
            print 'Then run python ... to generate problem skeleton file'
        else:
            print 'Error: Assignment {} already exists. Cannot overwrite'.format( assignment_name )



    '''
    Read the assignment configuration file and initialize the assignment
    instance variables.

    Before starting actual grading, this method can be used to generate
    Problem configuration file skeletons so that they can be filled with
    appropriate data to be used during the auto grading
    '''
    def setup_assignment( self, grading_root, grading_master, assignment_master_sub_dir ):

        # config_file = os.path.join( grading_root, grading_master, assignment_master_sub_dir, '+_1_{}.cfg'.format( assignment_master_sub_dir ) )
        config_file = os.path.join( grading_root, grading_master, assignment_master_sub_dir, self._99_agg.get_asmt_cfg_name( assignment_master_sub_dir ) )

        # Check whether the assignment configuration file exists.
        if not os.path.exists( config_file ):
            print '\nConfiguration file {} does not exist, exit...'.format( config_file )
            return False

        config = ConfigParser.SafeConfigParser()
        config.read( config_file )

        for key in sorted( self.__dict__.keys() ):  # [:-1]:
            if key[0:4] != '_99_':
                self.__dict__[key] = config.get( assignment_master_sub_dir, key[3:] ).strip()

        # self._1_asnmt_no = int( self._1_asnmt_no )
        self._3_duedate = datetime.datetime.strptime( self._3_duedate, '%m/%d/%Y' )

        self._4_gradingroot = grading_root
        self._5_subdir = assignment_master_sub_dir
        self._7_grading_master = grading_master

#         self._6_problem_ids = self._6_problem_ids.split()
#         temp_prob = {}
#         for p in self._6_problem_ids:
#             q = p.split( ':' )
#             temp_prob[q[0]] = q[1]
#         self._6_problem_ids = temp_prob

        problems = AgGlobals.parse_config_line( self._6_problem_ids )
        temp_prob = {}
        for p in problems:
            temp_prob[p[0]] = p[1]

        # This is a dictiory of the form:
        #    problem_id -> problem_type
        self._6_problem_ids = temp_prob

        print self
        self._99_state = AgGlobals.LOADED
        return True


    '''
    Set up the problems that constitutes this assignment
    '''
    def setup_problems( self ):
        if self._99_state == AgGlobals.LOADED:
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

            # Check problem dependencies
            prob_id_set = set( self._6_problem_ids )
            for p in sorted( self._6_problem_ids ):
                depend_set = self._8_problems[p].get_dependencies()
                if not depend_set.issubset( prob_id_set ):
                    print 'Error: Problem {} - {} is dependent on undefined problems {}.'.format( p, self._8_problems[p].get_name(), depend_set - prob_id_set )
                    return False

            self._99_state = AgGlobals.PROBLEMS_CREATED
            return True
        else:
            print 'Error: Need to load an assignment configuration before creating Problems'
            return False


    '''
    Generate problem configuration files
    '''
    def generate_problem_config( self ):
        if self._99_state == AgGlobals.LOADED:
            prob_cfg = self.get_prob_config_path()

            if os.path.exists( prob_cfg ):
                print 'Error: Problem configuration file {} already exisits. Cannot overwrite. Exit...'.format( prob_cfg )
                sys.exit()

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
                # section = '{}_problem_{}'.format( self._5_subdir, p )
                section = self._99_agg.get_problem_section( self._5_subdir, p )
                prob_config.add_section( section )
                for key in sorted( temp.__dict__.keys() ):
                    prob_config.set( section, key[4:], ' {}'.format( temp.__dict__[key] ) )

            with open( self.get_prob_config_path(), 'wb' ) as configfile:
                prob_config.write( configfile )

            print 'Setting up problem configuration file skeleton completed successfully'
            return True
        else:
            print 'Error: Need to load an assignment configuration before generating problem configurations'
            return False


    '''
    Generate the path to the configuration file that holds to configuration details of problems
    where this assignment is comprised of
    '''
    def get_prob_config_path( self ):
        # return os.path.join( self.get_masterdir(), '+_2_{}_problems.cfg'.format( self._5_subdir ) )
        return os.path.join( self.get_masterdir(), self._99_agg.get_prob_cfg_name( self._5_subdir ) )


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
    Create provided files in the assignment master sub directory.
    '''
    def generate_provided_files( self ):
        if self._99_state == AgGlobals.LOADED:
            self.setup_problems()

        if self._99_state == AgGlobals.PROBLEMS_CREATED:
            files = set()
            for p in self._6_problem_ids.keys():
                if self._8_problems[p].get_prob_type() == 'prog':
                    files.update( set( self._8_problems[p].get_files_provided() ) )
                    # print self._8_problems[p].get_files_provided()

            master = self.get_masterdir()
            for f in files:
                file_path = os.path.join( master, f )
                if not os.path.exists( file_path ):
                    print 'Provided file {} does not exist in the master directory. Creating...'.format( f )
                    fo = open( file_path, 'a' )
                    fo.close()

            return True
        else:
            print 'Error: Need to load an assignment configuration before checking "Provided" files for that assignment'
            return False

    '''
    Create submitted files in the assignment master sub directory.
    '''
    def generate_submitted_files( self ):
        if self._99_state == AgGlobals.LOADED:
            self.setup_problems()

        if self._99_state == AgGlobals.PROBLEMS_CREATED:
            files = set()
            for p in self._6_problem_ids.keys():
                files.update( set( self._8_problems[p].get_files_submitted() ) )

            master = self.get_masterdir()
            for f in files:
                file_path = os.path.join( master, f )
                if not os.path.exists( file_path ):
                    print 'Submitted file {} does not exist in the master directory. Creating...'.format( f )
                    fo = open( file_path, 'a' )
                    fo.close()

            return True
        else:
            print 'Error: Need to load an assignment configuration before checking "Submitted" files for that assignment'
            return False


    def generate_input_config( self ):
        if self._99_state == AgGlobals.LOADED:
            self.setup_problems()

        if self._99_state == AgGlobals.PROBLEMS_CREATED:

            # Create input output directory
            in_out_dir = os.path.join( self._4_gradingroot, self._7_grading_master, self._5_subdir, self._99_agg.get_input_output_directory() )
            if not os.path.exists( in_out_dir ):
                os.mkdir( in_out_dir )

            input_config = ConfigParser.SafeConfigParser()

            for p in sorted( self._6_problem_ids ):
                in_out = self._8_problems[p].get_inp_outps()

                for io in sorted( in_out ):
                    print io, in_out[io]
                    section = self._99_agg.get_input_section( self._5_subdir, p, io )
                    input_config.add_section( section )

                    temp_in = Input( in_out[io][0], in_out[io][1] )
                    for key in sorted( temp_in.__dict__.keys() ):
                        # Filter only the instances variables that are necessary for the configuration file
                        if key[0:4] != '_99_':
                            input_config.set( section, key[3:], ' {}'.format( temp_in.__dict__[key] ) )

                            if in_out[io][0] == AgGlobals.LONG:
                                input_file_path = os.path.join( in_out_dir, self._99_agg.get_input_file_name( self._5_subdir, p, io ) )
                                input_config.set( section, 'input_file', input_file_path )
                                fo = open( input_file_path, 'a' )
                                fo.close()

            cfg_path = os.path.join( in_out_dir, self._99_agg.get_input_cfg_name( self._5_subdir ) )
            with open( cfg_path, 'wb' ) as configfile:
                input_config.write( configfile )
            print 'Success: Input configuration file {} successfully created'.format( cfg_path )




# p = Assignment()
# p.test_meth()
