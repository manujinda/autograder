import os
import sys
import csv

class Problem(object):
    """
        A class to represent a single problem or a Homework
    """
    
    def __init__(self, no):
        self.prob_no = no
        self.name = ''
        self.proj_desc = 'Problem description'
        self.files_provided = []
        self.files_submitted = []
        self.inp_outps = {} # A dictionalry that maps test inputs to anticipated outputs
        self.language = 'Programming language used'
        self.command_line_options = False
        self.student_make_file = False
        self.make_targs = []
        self.scores = []

    def __str__(self):
        return '{} {}'.format(self.prob_no, self.name)
        
    def setup_problem(self, config_path):
        # Check whether the problem configuration file exisits.
        if not os.path.exists(config_path):
            print '\nProblem configuration file {} does not exist, exit...'.format(config_path)
            sys.exit()
        
        with open(config_path) as config_file:
            reader = csv.DictReader(config_file)
            for row in reader:
                print row['Key'], row['Value']
                if row['Key'] ==  'prob_no':
                    self.prob_no = int(row['Value'])
                elif row['Key'] == 'name':
                    self.name = row['Value']
            
        