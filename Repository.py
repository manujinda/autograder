'''
Created on Jul 6, 2016
A class to encapsulate a version control repository such as Git

@author: Manujinda Wathugala
'''
from datetime import datetime
import os
import re
import subprocess

from AgGlobals import AgGlobals
from Command import Command


class Repository( object ):
    '''
    classdocs
    '''


    def __init__( self, repo ):
        '''
        Constructor
        '''
        # git_ssh = re.compile( '^(git@)([a-zA-Z0-9]+)\.(org|com):([a-zA-Z0-9_]+)/([a-zA-Z0-9_-]+)\.(git)$' )
        # git_https = re.compile( '^(https://)(?:[a-zA-Z0-9_]+@|)([a-zA-Z0-9_]+).(com|org)/([a-zA-Z0-9_]+)/([a-zA-Z0-9_-]+).(git)$' )
        git_ssh = re.compile( '^(git@)([a-zA-Z0-9]+)\.(?:org|com):([a-zA-Z0-9]+-{0,1}[a-zA-Z0-9]+)/([a-zA-Z0-9_-]+)\.(git)$' )
        git_https = re.compile( '^(https://)(?:[a-zA-Z0-9_]+@|)([a-zA-Z0-9_]+).(?:com|org)/([a-zA-Z0-9]+-{0,1}[a-zA-Z0-9]+)/([a-zA-Z0-9_-]+).(git)$' )

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


    def __str__( self ):
#         desc = ''
#         for f in sorted( self.__dict__.keys() ):
#             desc += '{} > {} \n'.format( f, self.__dict__[f] )
#         return desc
        return AgGlobals.string_of( self )

    def clone( self, path = '', log_file = '' ):
        '''
        clone the git repo at the location provided.
        Checks whether already cloned beforehand.
        '''
        if self.valid:
            if self.repo_type == 'git':
                # This is a git repository
                cmd = 'git clone {} {}'.format( self.uri, path )
                # cloning = subprocess.Popen( cmd.split(), stdout = subprocess.PIPE, stderr = subprocess.PIPE )
                # out, err = cloning.communicate()

                retcode, out, err = Command( cmd ).run()
                print out
                print err
                print retcode  # cloning.returncode

                if retcode == 0:
                    fo = open( os.path.join( path, AgGlobals.REPO_LAST_CHANGED_FILE ) , 'w' )
                    fo.write( str( datetime.now() ) )
                    fo.close()
                    AgGlobals.write_to_log( log_file, 'Success: Cloning\n' )
                    return True
                else:
                    AgGlobals.write_to_log( log_file, '\tError: Cloning\n' )
                    AgGlobals.write_to_log( log_file, '\t{} {} {}'.format( retcode, out, err ) )
                    return False

        else:
            print 'Error: Invalid repository uri: {}'.format( self.uri )
            AgGlobals.write_to_log( log_file, '\tError: Invalid git uri' )
            return False

        return False


    def pull( self, path = '', log_file = '' ):
        if path:
            # cwd = os.getcwd()
            if os.path.exists( path ):
                # os.chdir( path )
                if self.repo_type == 'git':
                    if os.path.exists( '.git' ):
                        # pulling = subprocess.Popen( ['git', 'pull'], stdout = subprocess.PIPE, stderr = subprocess.PIPE )
                        # out, err = pulling.communicate()

                        retcode, out, err = Command( 'git pull' ).run( cwd = path )
                        print out
                        # print err
                        # print retcode  # pulling.returncode

                        # If git pull is successful
                        if retcode == 0:
                            now_time = datetime.now()
                            fo = open( os.path.join( path, AgGlobals.REPO_LAST_CHANGED_FILE ) , 'r' )
                            prev_update = datetime.strptime( fo.readline(), '%Y-%m-%d %H:%M:%S.%f' )
                            fo.close()
                            # If the repo has been updated
                            if out != AgGlobals.REPO_GIT_ALREADY_UP_TO_DATE:
                                fo = open( os.path.join( path, AgGlobals.REPO_LAST_CHANGED_FILE ) , 'w' )
                                fo.write( str( datetime.now() ) )
                                fo.close()
                                AgGlobals.write_to_log( log_file, 'Success: Pull' )
                                return True
                            else:
                                diff_time = now_time - prev_update
                                # print 'Difference: {}'.format( now_time - prev_update )
                                # print diff_time
                                # print now_time
                                # print prev_update
                                print 'There has been no change in the repo for {} days {} hours {} minutes'.format( diff_time.days, diff_time.seconds // 3600, ( diff_time.seconds // 60 ) % 60 )
                                AgGlobals.write_to_log( log_file, '\tNothing updated since {}\n'.format( prev_update ) )
                                AgGlobals.write_to_log( log_file, '\tNo activity for: {} days {} hours {} minutes\n'.format( diff_time.days, diff_time.seconds // 3600, ( diff_time.seconds // 60 ) % 60 ) )
                                return False
                        else:
                            AgGlobals.write_to_log( log_file, '\tError: pull\n' )
                            AgGlobals.write_to_log( log_file, '\t{} {} {}'.format( retcode, out, err ) )
                            return False
                    else:
                        print 'this is not a git repo'
                        AgGlobals.write_to_log( log_file, '\tError: Not a valid git repo\n' )
                        return False
                # os.chdir( cwd )
        else:
            print 'empty path'
            return False


    '''
    Copy a local repository to another local folder
    '''
    def copy( self, source, destination, student ):
        src = os.path.join( source, student )
        cwd = ''
        if self.repo_type == 'git':
            if os.path.exists( os.path.join( src, '.git' ) ):
                root = 'git {}{}'
                # cwd = os.getcwd()
                repo_copy = os.path.join( destination, student )
                if os.path.exists( os.path.join( repo_copy, '.git' ) ):
                    # os.chdir( repo_copy )
                    cwd = repo_copy
                    cmd = root.format( 'pull', '' )
                elif not os.path.exists( repo_copy ):
                    # os.chdir( destination )
                    cwd = destination
                    cmd = root.format( 'clone file://', src )
                    # print repo_copy
                else:
                    cmd = ''
                    print 'Error: Destination directory already exists but not a repository'

                if cmd:
                    # copying = subprocess.Popen( cmd.split(), stdout = subprocess.PIPE, stderr = subprocess.PIPE )
                    # out, err = copying.communicate()

                    retcode, out, err = Command( cmd ).run( cwd = cwd )
                    print out
                    print err
                    print retcode  # copying.returncode

                # os.chdir( cwd )

