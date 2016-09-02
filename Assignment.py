'''
Created on Jul 28, 2016
Encapsulates a single project / assignment / homework

@author: Manujinda Wathugala
'''

import ConfigParser
from __builtin__ import True
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
        self._1_asnmt_no = AgGlobals.ASSIGNMENT_INIT_NO
        self._2_name = AgGlobals.ASSIGNMENT_INIT_NAME
        self._3_duedate = AgGlobals.ASSIGNMENT_INIT_DUE_DATE
        # self._4_gradingroot = ''

        # This is the sub-directory in which each student submits his/her
        # solutions to the assignment. Each student creates a sub-directory
        # in his or her repo. When cloned each student directory will have
        # a sub-directory by this name. Further, the master director for a
        # particular assignment is also named with this.
        # self._5_subdir = 'assignment1 ; This is the directory name where files for this assignment is stored'

        # IDs of problems that comprises this assignment
        self._6_problem_ids = AgGlobals.ASSIGNMENT_INIT_PROBLEM_IDS

        # ID --> Problem mapping. Problem is an object of class Problem
        # Each Problem encapsulated the details of that problem.
        # self._8_problems = {}

        self._99_state = AgGlobals.ASSIGNMENT_STATE_INITIALIZED


    def __str__( self ):
#         desc = ''
#         for key in sorted( self.__dict__.keys() ):  # [:-1]:
#             if key[0:4] != '_99_':
#                 desc += '{} > {} \n'.format( key[3:], self.__dict__[key] )
#         return desc
        return AgGlobals.string_of( self, 3 )


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

            cfg_path = os.path.join( assignment_master_sub_dir, AgGlobals.get_asmt_cfg_name( assignment_name ) )
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
    def load_assignment( self, grading_root, grading_master, assignment_master_sub_dir ):

        # config_file = os.path.join( grading_root, grading_master, assignment_master_sub_dir, '+_1_{}.cfg'.format( assignment_master_sub_dir ) )
        config_file = os.path.join( grading_root, grading_master, assignment_master_sub_dir, AgGlobals.get_asmt_cfg_name( assignment_master_sub_dir ) )

        # Check whether the assignment configuration file exists.
        if not os.path.exists( config_file ):
            print '\nConfiguration file {} does not exist, exit...'.format( config_file )
            return False

        config = ConfigParser.SafeConfigParser()
        config.read( config_file )

        try:
            for key in sorted( self.__dict__.keys() ):  # [:-1]:
                if key[0:4] != '_99_':
                    self.__dict__[key] = config.get( assignment_master_sub_dir, key[3:] ).strip()
        except ConfigParser.NoSectionError as no_sec_err:
            print 'Error: {} in assignment configuration file {}. Exiting...'.format( no_sec_err, config_file )
            sys.exit()
        except ConfigParser.NoOptionError as no_op_err:
            print 'Error: {} in assignment configuration file {}. Exiting...'.format( no_op_err, config_file )
            sys.exit()

        # self._1_asnmt_no = int( self._1_asnmt_no )
        self._3_duedate = datetime.datetime.strptime( self._3_duedate, AgGlobals.ASSIGNMENT_CFG_DUE_DATE_FORMAT )

        self._4_gradingroot = grading_root
        self._5_subdir = assignment_master_sub_dir
        self._7_grading_master = grading_master

        problems = AgGlobals.parse_config_line( self._6_problem_ids )
        temp_prob = {}
        for p in problems:
            temp_prob[p[0]] = p[1]

        # This is a dictiory of the form:
        #    problem_id -> problem_type
        self._6_problem_ids = temp_prob

        # print self
        self._99_state = AgGlobals.set_flags( self._99_state, AgGlobals.ASSIGNMENT_STATE_LOADED )
        return True


    '''
    Set up the problems that constitutes this assignment
    '''
    def load_problems( self ):
        if AgGlobals.is_flags_set( self._99_state, AgGlobals.ASSIGNMENT_STATE_LOADED ):
            prob_conf = self.get_prob_config_path()
            # section_prefix = '{}_problem_{}'.format( self._5_subdir, '{}' )
            # Check whether the problem configuration file exists.
            if not os.path.exists( prob_conf ):
                print '\nProblem configuration file {} does not exist, exit...'.format( prob_conf )
                sys.exit()

            # ID --> Problem mapping. Problem is an object of class Problem
            # Each Problem encapsulated the details of that problem.
            self._8_problems = {}

            for p in sorted( self._6_problem_ids ):
                self._8_problems[p] = Problem( p, self._6_problem_ids[p] )

                self._8_problems[p].load_problem( prob_conf, AgGlobals.get_problem_section( self._5_subdir, p ) )

            # Check problem dependencies
            prob_id_set = set( self._6_problem_ids )
            for p in sorted( self._6_problem_ids ):
                depend_set = self._8_problems[p].get_dependencies()
                if not depend_set.issubset( prob_id_set ):
                    print 'Error: Problem {} - {} is dependent on undefined problems {}.'.format( p, self._8_problems[p].get_name(), depend_set - prob_id_set )
                    return False

            self._99_state = AgGlobals.set_flags( self._99_state, AgGlobals.ASSIGNMENT_STATE_PROBLEMS_LOADED )
            # print 'Loading success::::: {}'.format( self.get_masterdir() )
            return True
        else:
            print 'Error: Need to load an assignment configuration before loading Problems'
            return False


    '''
    Generate problem configuration files
    '''
    def generate_problem_config( self ):
        if AgGlobals.is_flags_set( self._99_state, AgGlobals.ASSIGNMENT_STATE_LOADED ):
            prob_cfg = self.get_prob_config_path()

            if os.path.exists( prob_cfg ):
                print 'Error: Problem configuration file {} already exists. Cannot overwrite. Exit...'.format( prob_cfg )
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
                section = AgGlobals.get_problem_section( self._5_subdir, p )
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
        return os.path.join( self.get_masterdir(), AgGlobals.get_prob_cfg_name( self._5_subdir ) )


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
        if AgGlobals.is_flags_set( self._99_state, AgGlobals.ASSIGNMENT_STATE_LOADED ):
            return os.path.join( self._4_gradingroot, self._7_grading_master, self._5_subdir )
        else:
            return ''


    def get_assignment_sub_dir( self ):
        if AgGlobals.is_flags_set( self._99_state, AgGlobals.ASSIGNMENT_STATE_LOADED ):
            return self._5_subdir
        else:
            return ''


    def get_problem_ids( self ):
        if AgGlobals.is_flags_set( self._99_state, AgGlobals.ASSIGNMENT_STATE_LOADED ):
            return self._6_problem_ids
        else:
            return {}


    def is_problems_loaded( self ):

        # Both the assignment and problems are loaded
        if AgGlobals.is_flags_set( self._99_state, AgGlobals.ASSIGNMENT_STATE_LOADED, AgGlobals.ASSIGNMENT_STATE_PROBLEMS_LOADED ):
            return True

        # Only the assignment is loaded
        if AgGlobals.is_flags_set( self._99_state, AgGlobals.ASSIGNMENT_STATE_LOADED ):
            # Try loading problems
            return self.load_problems()

        return False


    '''
        Accumulate all the file names student is supposed to submit and their possible aliases
        for each problem in this assignment / project into a dictionary of the form
        submitted_file_name --> set( [ alias1, alias2, ... ] )
        and return that dictionary
    '''
    def get_files_submitted_with_aliases( self ):
        # A dictionary of submitted file names and their aliases
        # submitted_file_name --> set(alias1, alias2, ...)
        glob_f_dict = {}

        # If problems are loaded
        if self.is_problems_loaded():
            # For each problem
            for p in self._6_problem_ids.keys():

                # Get the list of lists of file names and their aliases student should submit and
                # for the list of each file and its aliases - The 1st element is the file name and
                # the following names are the aliases
                for prob_f_list in self._8_problems[p].get_files_submitted_with_aliases():

                    # If this file has not been added to the list of all files student should
                    # submit for this assignment add that file and its aliases to the dictionary
                    if not prob_f_list[0] in glob_f_dict.keys():
                        glob_f_dict[prob_f_list[0]] = set( prob_f_list[1:] )

                    # If this file has already been added as part of another problem in this assignment
                    # add any additional aliases if present to the list of aliases of that file
                    else:
                        glob_f_dict[prob_f_list[0]].update( set( prob_f_list[1:] ) )

        return glob_f_dict



    '''
        Accumulate all the provided files for each problem in this assignment
        into a single set and return that set
    '''
    def get_provided_files_set( self ):

        # A set of provided file names
        provided_files = set()

        # If problems are loaded
        if self.is_problems_loaded():

            # For each problem
            for p in self._6_problem_ids.keys():

                # If this is a programming type project
                if self._8_problems[p].get_prob_type() == AgGlobals.PROBLEM_TYPE_PROG:

                    # Get the list of provided files for this problem and update the global
                    # set of provided files for this whole assignment / project
                    provided_files.update( set( self._8_problems[p].get_files_provided() ) )

        return provided_files


    '''
    Create provided files in the assignment master sub directory.
    '''
    def generate_provided_files( self ):
        # If problems are loaded
        if self.is_problems_loaded():
            files = set()
            for p in self._6_problem_ids.keys():
                if self._8_problems[p].get_prob_type() == AgGlobals.PROBLEM_TYPE_PROG:
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
        # If problems are loaded
        if self.is_problems_loaded():
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


    ''' Delete later '''
    def generate_input_config2( self ):
        # If problems are loaded
        if self.is_problems_loaded():

            # Create input output directory
            in_out_dir = os.path.join( self._4_gradingroot, self._7_grading_master, self._5_subdir, AgGlobals.INPUT_OUTPUT_DIRECTORY )
            if not os.path.exists( in_out_dir ):
                os.mkdir( in_out_dir )

            input_config = ConfigParser.SafeConfigParser()

            for p in sorted( self._6_problem_ids ):
                in_out = self._8_problems[p].get_inp_outps()

                for io in sorted( in_out ):
                    print io, in_out[io]
                    section = AgGlobals.get_input_section( self._5_subdir, p, io )
                    input_config.add_section( section )

                    temp_in = Input( in_out[io][0], in_out[io][1] )
                    for key in sorted( temp_in.__dict__.keys() ):
                        # Filter only the instances variables that are necessary for the configuration file
                        if key[0:4] != '_99_':
                            input_config.set( section, key[3:], ' {}'.format( temp_in.__dict__[key] ) )

                    if in_out[io][0] == AgGlobals.INPUT_NATURE_LONG:
                        input_file_path = os.path.join( in_out_dir, AgGlobals.get_input_file_name( self._5_subdir, p, io ) )
                        input_config.set( section, 'input_file', input_file_path )
                        fo = open( input_file_path, 'a' )
                        fo.close()

            cfg_path = os.path.join( in_out_dir, AgGlobals.get_input_cfg_name( self._5_subdir ) )
            with open( cfg_path, 'wb' ) as configfile:
                input_config.write( configfile )
            print 'Success: Input configuration file {} successfully created'.format( cfg_path )


    def generate_input_config( self ):
        # If problems are loaded
        if self.is_problems_loaded():

            # Create input output directory
            in_out_dir = os.path.join( self._4_gradingroot, self._7_grading_master, self._5_subdir, AgGlobals.INPUT_OUTPUT_DIRECTORY )
            if not os.path.exists( in_out_dir ):
                os.mkdir( in_out_dir )

            input_config = ConfigParser.SafeConfigParser()

            for p in sorted( self._6_problem_ids ):
                self._8_problems[p].generate_input_config( self._5_subdir, in_out_dir, input_config )

            cfg_path = os.path.join( in_out_dir, AgGlobals.get_input_cfg_name( self._5_subdir ) )
            with open( cfg_path, 'wb' ) as configfile:
                input_config.write( configfile )

            print 'Success: Input configuration file {} successfully created'.format( cfg_path )


    def load_input( self ):
        success = False
        # If problems are loaded
        if self.is_problems_loaded():

            cfg_path = os.path.join( self._4_gradingroot, self._7_grading_master, self._5_subdir, AgGlobals.INPUT_OUTPUT_DIRECTORY, AgGlobals.get_input_cfg_name( self._5_subdir ) )

            if not os.path.exists( cfg_path ):
                print '\Input configuration file {} does not exist, exit...'.format( cfg_path )
                sys.exit()

            success = True
            for p in sorted( self._6_problem_ids.keys() ):
                success = success and self._8_problems[p].load_input( self._5_subdir, cfg_path )

            if success:
                print 'Success: Loading inputs'

            return success


    '''
    Compile files.
    '''
    def compile( self, cwd = '' ):
        success = False
        # If problems are loaded
        if self.is_problems_loaded():
            # os.chdir( self.get_masterdir() )
            if not cwd:
                cwd = self.get_masterdir()
            success = True
            for p in sorted( self._6_problem_ids.keys() ):
                success = success and self._8_problems[p].compile( cwd )

        return success

    '''
    Link
    '''
    def link( self, cwd = '' ):
        success = False
        # If problems are loaded
        if self.is_problems_loaded():
            # os.chdir( self.get_masterdir() )
            if not cwd:
                cwd = self.get_masterdir()
            success = True
            for p in sorted( self._6_problem_ids.keys() ):
                success = success and self._8_problems[p].link( cwd )

        return success


    def generate_output( self, cwd = '' ):
        # If problems are loaded
        if self.is_problems_loaded():

            # Create input output directory
            if not cwd:
                cwd = os.path.join( self._4_gradingroot, self._7_grading_master, self._5_subdir, AgGlobals.INPUT_OUTPUT_DIRECTORY )
            if not os.path.exists( cwd ):
                os.mkdir( cwd )

            for p in sorted( self._6_problem_ids.keys() ):
                self._8_problems[p].generate_output( self._5_subdir, cwd )

            print 'Success: Generating Reference Outputs'


#     def load_inputs( self ):
#         if self._99_state == AgGlobals.ASSIGNMENT_STATE_LOADED:
#             self.load_problems()
#
#         if self._99_state == AgGlobals.ASSIGNMENT_STATE_PROBLEMS_LOADED:
#
#             in_out_dir = os.path.join( self._4_gradingroot, self._7_grading_master, self._5_subdir, AgGlobals.INPUT_OUTPUT_DIRECTORY )
#
#             input_conf = os.path.join( in_out_dir, AgGlobals.get_input_cfg_name( self._5_subdir ) )
#
#             if not os.path.exists( input_conf ):
#                 print '\nProblem configuration file {} does not exist, exit...'.format( input_conf )
#                 sys.exit()
#
#             for p in sorted( self._6_problem_ids ):
#                 in_out = self._8_problems[p].get_inp_outps()
#
#                 for io in sorted( in_out ):
#                     section = AgGlobals.get_input_section( self._5_subdir, p, io )
#
#                     temp_in = Input( in_out[io][0], in_out[io][1] )
#                     temp_in.load_input( input_conf, section )
#
#             print 'Success: Inputs successfully loaded'




# p = Assignment()
# p.test_meth()
