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
        # cmd - Command line input
        # short - Short input. Typically single line. Input is specified inline in the input configuration file itself.
        #         Multi-line inputs can be specified using '\n' to denote line breaks
        # long - Long inputs. Typically multi_lined. Input is specified in a seperate file.
        self._1_nature = nature  # 'short ; specify before the ;. values: cmdline, short, long'

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
        self._4_output = output  # 'stdout ; specify before the ;. values: stdout, file'

        # If output is produced in a file, the required file name is specified here
        if self._4_output != AgGlobals.OUTPUT_TO_STDOUT:
            self._5_out_file = AgGlobals.INPUT_INIT_OUTPUT_FILE

        # The percentage the student output should match the reference output and
        # the amount of marks granted if student output achieves that level.
        # Format: a list of matching_%:marks
        # 0 means no matching at all and 100 means perfect matching.
        self._6_marks = AgGlobals.INPUT_INIT_MARKS


    '''
    Read input configuration file and populate the instance variables
    '''
    def load_input( self, config_file, section ):

        # Check whether the problem configuration file exists.
        if not os.path.exists( config_file ):
            print '\Input configuration file {} does not exist, exit...'.format( config_file )
            sys.exit()

        config = ConfigParser.SafeConfigParser()
        config.read( config_file )

        for key in sorted( self.__dict__.keys() ):
            if key[0:4] != '_99_':
                self.__dict__[key] = config.get( section, key[3:] ).strip()

        return True

