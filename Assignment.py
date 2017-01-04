'''
Created on Jul 28, 2016
Encapsulates a single project / assignment / homework

@author: Manujinda Wathugala
'''

import ConfigParser
from __builtin__ import True
import datetime
import os
import shutil
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

        # IDs of problems that comprises this assignment
        self._6_problem_ids = AgGlobals.ASSIGNMENT_INIT_PROBLEM_IDS

        self._99_state = AgGlobals.ASSIGNMENT_STATE_INITIALIZED


    def __str__( self ):
        return AgGlobals.string_of( self, 3 )


    '''
        Generate a new blank assignment.
        Creates the directory and the default assignment configuration file
    '''
    def new_assignment( self, grading_root, grading_master, assignment_name ):

        assignment_master_sub_dir = os.path.join( grading_root, grading_master, assignment_name )
        if not os.path.exists( assignment_master_sub_dir ):
            os.mkdir( assignment_master_sub_dir )
            os.mkdir( os.path.join( assignment_master_sub_dir, AgGlobals.LOG_FILE_DIRECTORY ) )

            assignment_config = ConfigParser.SafeConfigParser()
            assignment_config.add_section( assignment_name )

            for key in sorted( self.__dict__.keys() ):
                # Filter only the instances variables that are necessary for the configuration file
                if key[0:4] != '_99_':
                    assignment_config.set( assignment_name, key[3:], ' {}'.format( self.__dict__[key] ) )

            cfg_path = os.path.join( assignment_master_sub_dir, AgGlobals.get_asmt_cfg_name( assignment_name ) )
            with open( cfg_path, 'wb' ) as configfile:
                assignment_config.write( configfile )
            print 'Success: Blank assignment {} successfully created'.format( assignment_name )
            # print 'Update the configuration file: {} as necessary to define the assignment'.format( cfg_path )
            # print 'Then run python ... to generate problem skeleton file'
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

        config_file = os.path.join( grading_root, grading_master, assignment_master_sub_dir, AgGlobals.get_asmt_cfg_name( assignment_master_sub_dir ) )

        # Check whether the assignment configuration file exists.
        if not os.path.exists( config_file ):
            print '\nConfiguration file {} does not exist, exit...'.format( config_file )
            return False

        config = ConfigParser.SafeConfigParser()
        config.read( config_file )

        try:
            for key in sorted( self.__dict__.keys() ):
                if key[0:4] != '_99_':
                    self.__dict__[key] = config.get( assignment_master_sub_dir, key[3:] ).strip()
        except ConfigParser.NoSectionError as no_sec_err:
            print 'Error: {} in assignment configuration file {}. Exiting...'.format( no_sec_err, config_file )
            sys.exit()
        except ConfigParser.NoOptionError as no_op_err:
            print 'Error: {} in assignment configuration file {}. Exiting...'.format( no_op_err, config_file )
            sys.exit()

        try:
            self._3_duedate = datetime.datetime.strptime( self._3_duedate, AgGlobals.ASSIGNMENT_CFG_DUE_DATE_FORMAT )
        except ValueError:
            print 'Error: Invalid date time format for duedate. Exiting...'
            sys.exit()

        self._4_gradingroot = grading_root

        # This is the sub-directory in which each student submits his/her
        # solutions to the assignment. Each student creates a sub-directory
        # in his or her repo. When cloned each student directory will have
        # a sub-directory by this name. Further, the master director for a
        # particular assignment is also named with this.
        self._5_subdir = assignment_master_sub_dir

        self._7_grading_master = grading_master

        problems = AgGlobals.parse_config_line( self._6_problem_ids )
        temp_prob = {}
        for p in problems:
            try:
                temp_prob[int( p[0] )] = p[1]
            except ValueError:
                print 'Error: Problem number "{}" of problem type "{}" must be an integer. Exiting...'.format( p[0], p[1] )
                sys.exit()


        # This is a dictionary of the form:
        #    problem_id -> problem_type
        self._6_problem_ids = temp_prob

        self._99_state = AgGlobals.set_flags( self._99_state, AgGlobals.ASSIGNMENT_STATE_LOADED )
        return True


    '''
    Set up the problems that constitutes this assignment
    '''
    def load_problems( self ):
        if AgGlobals.is_flags_set( self._99_state, AgGlobals.ASSIGNMENT_STATE_LOADED ):
            prob_conf = self.get_prob_config_path()

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
                section = AgGlobals.get_problem_section( self._5_subdir, p )
                prob_config.add_section( section )
                for key in sorted( temp.__dict__.keys() ):
                    if key[0:4] != '_99_':
                        prob_config.set( section, key[4:], ' {}'.format( temp.__dict__[key] ) )

            with open( self.get_prob_config_path(), 'wb' ) as configfile:
                prob_config.write( configfile )

            print 'Success: Setting up problem configuration file skeleton'
            print 'File at: {}'.format( self.get_prob_config_path() )
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


    def get_deadline( self ):
        if AgGlobals.is_flags_set( self._99_state, AgGlobals.ASSIGNMENT_STATE_LOADED ):
            return self._3_duedate
        else:
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

            master = self.get_masterdir()
            print 'Creating provided files:'
            for f in files:
                file_path = os.path.join( master, f )
                if not os.path.exists( file_path ):
                    fo = open( file_path, 'a' )
                    fo.close()
                    print '\tCreated \t\t{}'.format( f )
                else:
                    print '\t\tAlready exists \t\t{}'.format( f )
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
            print 'Creating submitted files'
            for f in files:
                file_path = os.path.join( master, f )
                if not os.path.exists( file_path ):
                    fo = open( file_path, 'a' )
                    fo.close()
                    print '\tCreated \t\t{}'.format( f )
                else:
                    print '\t\tAlready exists \t\t{}'.format( f )

            return True
        else:
            print 'Error: Need to load an assignment configuration before checking "Submitted" files for that assignment'
            return False


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

            print 'Success: Generating input configuration file\n\t {}'.format( cfg_path )


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
    # def compile( self, cwd = '', grading_log_file = None, student_log_file = None, gradebook = None ):
    def compile( self ):
        success = False
        # If problems are loaded
        if self.is_problems_loaded():
            # if not cwd:
            cwd = self.get_masterdir()
            success = True
            for p in sorted( self._6_problem_ids.keys() ):
                success = success and self._8_problems[p].compile( cwd )

        return success

    '''
    Link
    '''
    # def link( self, cwd = '', grading_log_file = None, student_log_file = None, gradebook = None ):
    def link( self ):
        success = False
        # If problems are loaded
        if self.is_problems_loaded():
            # if not cwd:
            cwd = self.get_masterdir()
            success = True
            for p in sorted( self._6_problem_ids.keys() ):
                success = success and self._8_problems[p].link( cwd )

        return success


    # def generate_output( self, cwd = '' ):
    def generate_output( self ):
        # If problems are loaded
        if self.is_problems_loaded():

            # Create input output directory
            # if not cwd:
            cwd = os.path.join( self._4_gradingroot, self._7_grading_master, self._5_subdir, AgGlobals.INPUT_OUTPUT_DIRECTORY )
            if not os.path.exists( cwd ):
                os.mkdir( cwd )

            for p in sorted( self._6_problem_ids.keys() ):
                self._8_problems[p].generate_output( self._5_subdir, cwd, self.get_masterdir() )

            print 'Success: Generating Reference Outputs'



    '''
        Autograder do_grade2 calls this.
    '''
    def grade2( self, cwd, grading_log_file = None, student_log_file = None, gradebook = None, prob_no = None ):

        def rename_bad_file_names_back( name_tuple_list ):
            # Rename the files back to what student has originally submitted.
            # This renaming is necessary to properly update the student submission
            # in the grading directory in subsequent copying and compiling.
            for bad_file_name in name_tuple_list:
                shutil.move( bad_file_name[0], bad_file_name[1] )


        depend_success = { p:False for p in self._6_problem_ids.keys() }

        success = False
        # If problems are loaded
        if self.is_problems_loaded():

            if prob_no:
                problems = self.get_dependent_problme_nos( prob_no )
            else:
                problems = sorted( self._6_problem_ids.keys() )

            success = True

            for p in problems:
                AgGlobals.write_to_log( student_log_file, '<h3 class=problem_heading>Grading problem: {}) {}</h3>'.format( p, self._8_problems[p].get_name() ), 1 )

                success = True

                # Check whether the student has submitted all the files
                # required for this problem. If not we cannot grade this problem
                skip_problem = False

                # Get the list of lists of file names and their aliases student should submit and
                # for the list of each file and its aliases - The 1st element is the file name and
                # the following names are the aliases
                # [ [fn1, a11, a12], [fn2, a21, a22, a23], [fn3] ]
                file_aliases = self._8_problems[p].get_files_submitted_with_aliases()

                # Use this list to rename the files back to the original file name
                # student submitted after the compilation is over.
                # This renaming is necessary to properly update the student submission
                # in the grading directory in subsequent copying and compiling.
                rename_back_list = []

                # For each file student is supposed to submit
                for file_submitted in file_aliases:

                    # The path for that file in the student's directory in the grading directory
                    file_path = os.path.join( cwd, file_submitted[0] )

                    # If student has not submitted a file with the exact name
                    if not os.path.exists( file_path ):

                        # Check whether the student has submitted a file that matches an alias
                        # Alias could be a misspelled file name or a shorten file name
                        found = False
                        for file_alias in file_submitted[1:]:
                            file_alias_path = os.path.join( cwd, file_alias )

                            # A file that matches an alias exists.
                            # Student might have submitted this file thinking he/she is submitting
                            # the file he/she is supposed to submit
                            if os.path.exists( file_alias_path ):
                                found = True
                                # Rename the file. Might want to do this only when we provide the make file
                                shutil.move( file_alias_path, file_path )
                                rename_back_list.append( ( file_path, file_alias_path ) )
                                AgGlobals.write_to_log( grading_log_file, 'Warning: Renamed file - {} --> {}\n'.format( file_alias, file_submitted[0] ), 1 )
                                AgGlobals.write_to_log( student_log_file, '<div class=warning>Warning: Renamed file - {} --> {}</div>'.format( file_alias, file_submitted[0] ), 1 )
                                gradebook[AgGlobals.GRADEBOOK_HEADER_COMMENT] += 'Renamed file - {} --> {}\n'.format( file_alias, file_submitted[0] )
                                break

                        if not found:
                            # print 'Error: Student {} has not submitted file {}'.format( stud.get_name(), file_submitted[0] )
                            AgGlobals.write_to_log( grading_log_file, 'Error: File - {} - missing\n'.format( file_submitted[0] ), 1 )
                            AgGlobals.write_to_log( student_log_file, '<div class=error>Error: File - {} - missing</div>'.format( file_submitted[0] ), 1 )
                            gradebook[AgGlobals.GRADEBOOK_HEADER_COMMENT] += 'File - {} - missing. Cannot grade problem {}\n'.format( file_submitted[0], p )
                            # We cannot proceed with grading this problem.
                            skip_problem = True

                # Check whether all the problems that this problem depends on
                # succeeded before moving forward with this problem
                for depend in self._8_problems[p].get_dependencies():
                    if not depend_success[depend]:
                        AgGlobals.write_to_log( grading_log_file, 'Error: Depends on problem - {}) {} - that did not succeed'.format( depend, self._8_problems[depend].get_name() ), 1 )
                        AgGlobals.write_to_log( student_log_file, '<div class=error>Error:  Depends on problem - {}) {} - that did not suceed</div>'.format( depend, self._8_problems[depend].get_name() ), 1 )
                        gradebook[AgGlobals.GRADEBOOK_HEADER_COMMENT] += 'Depends on problem {}. Cannot grade problem {}\n'.format( depend, p )
                        skip_problem = True

                if skip_problem:
                    # Rename the files back to what student has originally submitted.
                    # This renaming is necessary to properly update the student submission
                    # in the grading directory in subsequent copying and compiling.
                    rename_bad_file_names_back( rename_back_list )
                    continue

                # Compiling
                success = success and self._8_problems[p].compile( cwd, grading_log_file, student_log_file, gradebook )

                # Linking
                if success:
                    # Compiled successfully. Try to link
                    success = success and self._8_problems[p].link( cwd, grading_log_file, student_log_file, gradebook )
                else:
                    # Compilation failed. Cannot link. Grade next problem
                    success = True
                    # Rename the files back to what student has originally submitted.
                    # This renaming is necessary to properly update the student submission
                    # in the grading directory in subsequent copying and compiling.
                    rename_bad_file_names_back( rename_back_list )
                    continue

                # Keep track of whether problem p linked successfully
                depend_success[p] = success

                # Running
                if success:
                    # Linked successfully. Try to run and produce output
                    output_dir = os.path.join( cwd, AgGlobals.INPUT_OUTPUT_DIRECTORY )
                    if not os.path.exists( output_dir ):
                        os.mkdir( output_dir )

                    self._8_problems[p].generate_output( self._5_subdir, output_dir, self.get_masterdir(), grading_log_file, student_log_file, gradebook )


                # Rename the files back to what student has originally submitted.
                # This renaming is necessary to properly update the student submission
                # in the grading directory in subsequent copying and compiling.
                for bad_file_name in rename_back_list:
                    shutil.move( bad_file_name[0], bad_file_name[1] )

        return success


    def generate_gradebook_headers( self, prob_no = None ):
        marks_header = [AgGlobals.GRADEBOOK_HEADER_STUDENT]
        if self.is_problems_loaded():

            if prob_no:
                problems = self.get_dependent_problme_nos( prob_no )
            else:
                problems = sorted( self._6_problem_ids.keys() )

            for p in problems:
                headers = self._8_problems[p].get_gradebook_headers()
                marks_header += headers

        return marks_header


    '''
        Find all the problem numbers the provided problem prob_no
        is directly or inderectly dependent upon.
    '''
    def get_dependent_problme_nos( self, prob_no ):

        # Problems numbers yet to search for dependencies
        search_dependencis = set( [prob_no] )

        # Already found dependencies
        dept_probs = []

        # While there are more problems to search for dependencies
        while search_dependencis:

            # Consider one such problem
            p = search_dependencis.pop()

            # If that problem is not already in the
            # dependencies found so far.
            # This could happen due to indirect dependencies
            if p not in dept_probs:

                # Add this problem to the set of dependencies
                dept_probs.append( p )

                # Get all the problems that this problem is dependent upon
                deps = self._8_problems[p].get_dependencies()

                # For each problem that this problem is dependent upon
                for d in deps:

                    # If that problem is not already in the list of dependent
                    # problems found so far.
                    if d not in dept_probs:

                        # We have to find all the problems that this problem
                        # is dependent upon.
                        search_dependencis.add( d )

        return sorted( dept_probs )


    def is_valid_problem_id( self, prob_no ):
        return prob_no in self._6_problem_ids.keys()
