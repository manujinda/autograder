'''
Created on Aug 9, 2016

@author: Manujinda Wathugala

Global constants and formats that are used across classes of the autograder
'''

class AgGlobals( object ):

    def __init__( self ):
        self.ag_cfg = 'autograder.cfg'
        self.asnmt_cfg = '+_1_{}.cfg'
        self.prob_cfg = '+_2_{}_problems.cfg'
        self.students_directory = 'students'
        self.grading_directory = 'grading'
        self.students_db = 'students.csv'
        self.prob_section_format = '{}_problem_{}'


    def get_autograder_cfg_name( self ):
        return self.ag_cfg

    def get_asmt_cfg_name( self, assignment_name ):
        return self.asnmt_cfg.format( assignment_name )


    def get_prob_cfg_name( self, assignment_name ):
        return self.prob_cfg.format( assignment_name )


    def get_students_directory( self ):
        return self.students_directory


    def get_grading_directory( self ):
        return self.grading_directory


    def get_students_db_name( self ):
        return self.students_db


    def get_problem_section( self, assignment_name, problem_id ):
        return self.prob_section_format.format( assignment_name, problem_id )

    '''
        When a string of the form:
            111:aaa:xxx 22:bbbbb:yy 3:ccc
        is passed this returns a list of lists of the form:
            [ [111, aaa, xxx], [22, bbbbb, yy], [3, cc] ]
    '''
    @classmethod
    def parse_config_line( cls, line ):
        parts = line.split()
        ll = []
        for p in parts:
            ll.append( p.split( ':' ) )

        return ll

