#!/usr/bin/python 

import datetime

import Problem

class Project(object):
    """
        A collection of problems that are bundled togetther as a project.
        Has a common due dayte.
    """
    def __init__(self):
        self.proj_no = 0
        self.duedate = datetime.date(2016, 6, 28)
        self.subdir = 'assignment'
        self.problems = []
        
        for i in range(3):
            self.problems.append(Problem.Problem(i))
            
        print 'initialized'
        for i in range(3):
            print self.problems[i].prob_no
        
p = Project()