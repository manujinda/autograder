'''
Created on Aug 12, 2016

@author: Manujinda Wathugala

To encapsulate a test input to a program
'''
import ConfigParser
import os
import sys

from AgGlobals import AgGlobals


class Input( object ):
    '''
    classdocs
    '''

    def __init__( self, nature, output ):
        '''
        Constructor
        '''
        # The nature (how long and the stage at which the input is provided) of the input
        # short - Short input. Typically single line. Input is specified inline in the input configuration file itself.
        #         Multi-line inputs can be specified using '\n' to denote line breaks
        # long - Long inputs. Typically multi_lined. Input is specified in a seperate file.
        self._1_nature = nature  # 'short ; specify before the ;. values: short, long'

        self._2_cmd_line_input = AgGlobals.INPUT_INIT_CMD_LINE_INPUT

        # if nature of the input is cmdline or short, the actual input is specified
        # else the path the the file where this input is stored is specified.
        # if self._1_nature == AgGlobals.INPUT_NATURE_CMD or self._1_nature == AgGlobals.INPUT_NATURE_SHORT:
        if self._1_nature == AgGlobals.INPUT_NATURE_SHORT:
            self._3_input = AgGlobals.INPUT_INIT_INPUT
        else:
            self._3_input_file = AgGlobals.INPUT_INIT_INPUT_FILE

        # The place where the output is produced.
        # stdout - Standard output
        # file - Output is produced in a file.
        # both - Output to both stdout and files
        self._4_output = output  # 'stdout ; specify before the ;. values: stdout, file'

        # If output is produced in a file, the required file name is specified here
        if self._4_output != AgGlobals.OUTPUT_TO_STDOUT:
            self._5_out_file = AgGlobals.INPUT_INIT_OUTPUT_FILE

        # The percentage the student output should match the reference output and
        # the amount of marks granted if student output achieves that level.
        # Format: a list of matching_%:marks
        # 0 means no matching at all and 100 means perfect matching.
        self._6_marks = AgGlobals.INPUT_INIT_MARKS


    def __str__( self ):
        return AgGlobals.string_of( self, 3 )


    '''
    Read input configuration file and populate the instance variables
    '''
    def load_input( self, config_file, section ):

        # Check whether the problem configuration file exists.
        if not os.path.exists( config_file ):
            print '\Input configuration file {} does not exist, exit...'.format( config_file )
            sys.exit()

        input_nature_in_problem = self._1_nature
        output_location_in_problem = self._4_output

        config = ConfigParser.SafeConfigParser()
        config.read( config_file )
        print self

        try:
            for key in sorted( self.__dict__.keys() ):
                if key[0:4] != '_99_':
                    self.__dict__[key] = config.get( section, key[3:] ).strip()
        except ConfigParser.NoSectionError as no_sec_err:
            print 'Error: {} in input configuration file {}. Exiting...'.format( no_sec_err, config_file )
            sys.exit()
        except ConfigParser.NoOptionError as no_op_err:
            print 'Error: {} in input configuration file {}. Exiting...'.format( no_op_err, config_file )
            sys.exit()

        if self._1_nature != input_nature_in_problem:
            print 'Error:  Input nature mismatch for input'  # "{}" of type "{}"'.format( self._02_name, self._03_prob_type )
            print '\tInput nature in problem configuration : {}'.format( input_nature_in_problem )
            print '\tInput nature in input configuration    : {}'.format( self._1_nature )
            print '\tExiting...'
            sys.exit()

        if self._4_output != output_location_in_problem:
            print 'Error:  Output location mismatch for input'  # "{} - {}"'.format( self._01_prob_no, self._02_name )
            print '\tOutput location in problem configuration : {}'.format( output_location_in_problem )
            print '\tOutput location in input configuration    : {}'.format( self._4_output )
            print '\tExiting...'
            sys.exit()

        if self._1_nature == AgGlobals.INPUT_NATURE_LONG:
            # Check whether the file containing actual input exists
            if not os.path.exists( self._3_input_file ):
                print 'Error: File {} containing input does not exists. Exit...'.format( self._3_input_file )
                sys.exit()

            inp = open( self._3_input_file, 'r' )
            self._3_input = inp.read()
            inp.close()

        if self._4_output == AgGlobals.OUTPUT_TO_FILE or self._4_output == AgGlobals.OUTPUT_TO_BOTH:
        # if self._4_output != AgGlobals.OUTPUT_TO_STDOUT:
            self._5_out_file = self._5_out_file.split()

        temp_marks = AgGlobals.parse_config_line( self._6_marks )
        self._6_marks = {}
        for mark in temp_marks:
            self._6_marks[mark[0]] = mark[1]

        print self

        return True


    def get_cmd_line_input( self ):
        return self._2_cmd_line_input


    def get_inputs( self ):
        return self._3_input


    def get_output_files_generated( self ):
        if self._4_output == AgGlobals.OUTPUT_TO_FILE or self._4_output == AgGlobals.OUTPUT_TO_BOTH:
        # if self._4_output != AgGlobals.OUTPUT_TO_STDOUT:
            return self._5_out_file
        else:
            return []


    def outputs_to_stdout( self ):
        return self._4_output == AgGlobals.OUTPUT_TO_STDOUT or self._4_output == AgGlobals.OUTPUT_TO_BOTH
