#!/usr/bin/python

import csv
import datetime
import os
import sys

from Problem import Problem


class Project( object ):
    """
        A collection of problems that are bundled togetther as a project.
        Has a common due dayte.
    """
    def __init__( self ):
        self.proj_no = 0
        self.name = ''
        self.duedate = datetime.date( 2016, 6, 28 )
        self.gradingroot = ''
        self.masterdir = ''
        self.subdir = 'assignment'
        self.problem_ids = []
        self.problems = {}

        # for i in range(3):
        #    self.problems.append(Problem.Problem(i))
        #
        # print 'initialized'
        # for i in range(3):
        #    print self.problems[i].prob_no


    def setup_project( self, config_path ):

        # Check whether the file exists.
        if not os.path.exists( config_path ):
            print '\nConfiguration file {} does not exist, exit...'.format( config_path )
            sys.exit()

        # config_dict = {}
        with open( config_path ) as config_file:
            reader = csv.DictReader( config_file )
            for row in reader:
                # self.__dict__[row['Key']] = row['Value']
                key = row['Key'].strip()
                value = row[' Value'].strip()
                if key == 'proj_no':
                    self.proj_no = int( value )
                elif key == 'name':
                    self.name = value
                elif key == 'duedate':
                    self.duedate = datetime.datetime.strptime( value, '%m/%d/%Y' )
                elif key == 'gradingroot':
                    self.gradingroot = value
                elif key == 'subdir':
                    self.subdir = value
                elif key == 'problems':
                    self.problem_ids = value.split()
                # config_dict[row['Key']] = row['Value']

        generate = raw_input( '\nGenerate Project Skeleton ( y / n ) : ' )

        if ( generate == 'y' ):
            self.generate_problem_config()
        else:
            self.read_problem_config()
        print generate

    def read_problem_config( self ):
        for p in self.problem_ids:
            prob_conf = os.path.join( self.gradingroot, 'assignments', self.subdir, 'prob_' + p + '.csv' )
            print prob_conf

            # Check whether the problem configuration file exisits.
            if not os.path.exists( prob_conf ):
                print '\nProblem configuration file {} does not exist, exit...'.format( prob_conf )
                sys.exit()

            self.problems[p] = Problem( p )

            self.problems[p].setup_problem( prob_conf )

        for p in self.problems.keys():
            print self.problems[p]


    def generate_problem_config( self ):
        asgnmt_root = os.path.join( self.gradingroot, 'assignments', self.subdir )

        if not os.path.exists( asgnmt_root ):
            os.mkdir( asgnmt_root )

        for p in self.problem_ids:
            prob_conf = os.path.join( asgnmt_root, 'prob_' + p + '.csv' )
            with open( prob_conf, 'wb' ) as config_file:
                # writer = csv.DictWriter( config_file )
                writer = csv.writer( config_file, delimiter = ',', quotechar = '|', quoting = csv.QUOTE_MINIMAL )
                writer.writerow( ['Key', '{} {}'.format( ' ', 'Value' )] )

                temp = Problem( p )
                print temp.__dict__
                for key in sorted( temp.__dict__.keys() ):
                    writer.writerow( [key , '{} {}'.format( ' ', temp.__dict__[key] )] )

# p = Project()
# p.test_meth()
