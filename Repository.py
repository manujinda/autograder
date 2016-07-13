'''
Created on Jul 6, 2016
A class to encapsulate a version control repository such as Git

@author: manujinda
'''
import os
import re
import subprocess


class Repository( object ):
    '''
    classdocs
    '''


    def __init__( self, repo ):
        '''
        Constructor
        '''
        # git_ssh = re.compile( '^(git@)([a-zA-Z0-9]*)\.(org|com):([a-zA-Z0-9_]*)/([a-zA-Z0-9_-]*)\.(git)$' )
        # git_https = re.compile( '^(https://)(?:[a-zA-Z0-9_]*@|)([a-zA-Z0-9_]*).(com|org)/([a-zA-Z0-9_]*)/([a-zA-Z0-9_-]*).(git)$' )
        git_ssh = re.compile( '^(git@)([a-zA-Z0-9]*)\.(?:org|com):([a-zA-Z0-9_]*)/([a-zA-Z0-9_-]*)\.(git)$' )
        git_https = re.compile( '^(https://)(?:[a-zA-Z0-9_]*@|)([a-zA-Z0-9_]*).(?:com|org)/([a-zA-Z0-9_]*)/([a-zA-Z0-9_-]*).(git)$' )

        self.uri = repo.strip()

        valid_rui = git_ssh.match( self.uri )

        if not valid_rui:
            valid_rui = git_https.match( self.uri )

        if valid_rui:
            self.protocol = 'https' if valid_rui.group( 1 ) == 'https://' else 'ssh'
            self.host = valid_rui.group( 2 )
            self.user_name = valid_rui.group( 3 )  # ( 4 )
            self.repo_name = valid_rui.group( 4 )  # ( 5 )
            self.repo_type = valid_rui.group( 5 )  # ( 6 )
            self.valid = True
        else:
            # self.uri = ''
            self.protocol = ''
            self.host = ''
            self.user_name = ''
            self.repo_name = ''
            self.repo_type = ''
            self.valid = False
            print 'Invalid git uri: {}'.format( self.uri )

#         if valid_rui:
#             self.repo_type = 'git'
#             self.protocol = 'ssh'
#             self.host = valid_rui.group( 2 )
#             self.user_name = valid_rui.group( 4 )
#             self.repo_name = valid_rui.group( 5 )
#         else:
#             valid_rui = git_https.match( self.uri )
#
#             if valid_rui:
#                 self.repo_type = 'git'
#                 self.protocol = 'https'
#                 self.host = valid_rui.group( 3 )
#                 self.user_name = valid_rui.group( 5 )
#                 self.repo_name = valid_rui.group( 6 )
#             else:
#                 self.repo_type = ''
#                 self.protocol = ''
#                 self.host = ''
#                 self.user_name = ''
#                 self.repo_name = ''
#                 print 'Invalid git uri'


    def __str__( self ):
        desc = ''
        for f in sorted( self.__dict__.keys() ):
            desc += '{} > {} \n'.format( f, self.__dict__[f] )
        return desc

    def clone( self, path = '' ):
        '''
        clone the git repo at the location provided.
        Checks whether already cloned beforehand.
        '''
        if self.valid:
            cmd = 'git clone {} {}'.format( self.uri, path )
            cloning = subprocess.Popen( cmd.split(), stdout = subprocess.PIPE, stderr = subprocess.PIPE )
            out, err = cloning.communicate()
            print 'output\n', out
            print 'error\n', err
        else:
            print 'Error: Invalid Git uri: {}'.format( self.uri )
