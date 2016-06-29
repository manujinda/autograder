#!/usr/bin/python 

import datetime
import os
import sys
import csv

from Problem import Problem

class Project(object):
    """
        A collection of problems that are bundled togetther as a project.
        Has a common due dayte.
    """
    def __init__(self):
        self.proj_no = 0
        self.name = ''
        self.duedate = datetime.date(2016, 6, 28)
        self.gradingroot = ''
        self.masterdir = ''
        self.subdir = 'assignment'
        self.problem_ids = []
        self.problems = {}
        
        #for i in range(3):
        #    self.problems.append(Problem.Problem(i))
        #    
        #print 'initialized'
        #for i in range(3):
        #    print self.problems[i].prob_no
            
        
    def setup_project(self, config_path):
        
        # Check whether the file exists.
        if not os.path.exists(config_path):
            print '\nConfiguration file {} does not exist, exit...'.format(config_path)
            sys.exit()

        #config_dict = {}
        with open(config_path) as config_file:
            reader = csv.DictReader(config_file)
            for row in reader:
                print row['Key'], row['Value']
                if row['Key'] ==  'proj_no':
                    self.proj_no = int(row['Value'])
                elif row['Key'] == 'name':
                    self.name = row['Value']
                elif row['Key'] == 'duedate':
                    self.duedate = datetime.datetime.strptime(row['Value'], '%m/%d/%Y')
                elif row['Key'] == 'gradingroot':
                    self.gradingroot = row['Value']
                elif row['Key'] == 'subdir':
                    self.subdir = row['Value']
                elif row['Key'] == 'problems':
                    self.problem_ids = row['Value'].split()
                #config_dict[row['Key']] = row['Value']
                
        for p in self.problem_ids:
            prob_conf = os.path.join(self.gradingroot, 'assignments', self.subdir, 'prob_' + p + '.csv')
            print prob_conf
            
            # Check whether the problem configuration file exisits.
            if not os.path.exists(prob_conf):
                print '\nProblem configuration file {} does not exist, exit...'.format(prob_conf)
                sys.exit()
            
            self.problems[p] = Problem(p)
            
            self.problems[p].setup_problem(prob_conf)
            
            #continue

            #prob_conf = 'C:\\Users\\manujinda\\Documents\\++grading\\assignments\\assignment1\\assignment1.csv'            
            #with open(prob_conf) as config_file:
            #    reader = csv.DictReader(config_file)
            #    for row in reader:
            #        print row['Key'], row['Value']
            #        if row['Key'] ==  'prob_no':
            #            self.problems[p].prob_no = int(row['Value'])
            #        elif row['Key'] == 'name':
            #            self.problems[p].name = row['Value']
            #    
            #    print self.problems[p]
                
        #print self.problems
        for p in self.problems.keys():
            print self.problems[p]
        
#p = Project()
#p.test_meth()