'''
Created on Jul 6, 2016
A class to encapsulate a version control repository such as Git

@author: Manujinda Wathugala
'''
from datetime import datetime
import os
import re
# import subprocess

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
            self.user_name = valid_rui.group( 3 )
            self.repo_name = valid_rui.group( 4 )
            self.repo_type = valid_rui.group( 5 )
            self.valid = True
        else:
            self.protocol = ''
            self.host = ''
            self.user_name = ''
            self.repo_name = ''
            self.repo_type = ''
            self.valid = False
            print 'Invalid git uri: {}'.format( self.uri )


    def __str__( self ):
        return AgGlobals.string_of( self )

    def clone( self, path = '', grading_log_file = None, student_log_file = None ):
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
                    AgGlobals.write_to_log( grading_log_file, 'Success: Cloning\n' )
                    # AgGlobals.write_to_log( student_log_file, 'Success: Cloning\n' )
                    AgGlobals.write_to_log( student_log_file, '<h3 class=success>Success: Cloning Repo</h3>', 1 )
                    return True
                else:
                    AgGlobals.write_to_log( grading_log_file, 'Error: Cloning\n', 1 )
                    AgGlobals.write_to_log( grading_log_file, '{} {} {}'.format( retcode, out, err ), 1 )
                    # AgGlobals.write_to_log( student_log_file, '\tError: Cloning\n' )
                    # AgGlobals.write_to_log( student_log_file, '\t{} {} {}'.format( retcode, out, err ) )
                    AgGlobals.write_to_log( student_log_file, '<div class=error>Error: Cloning Repo - {}</div>'.format( self.uri ), 1 )

                    AgGlobals.write_to_log( student_log_file, '<div class=error_out><pre>', 1 )
                    err = err.replace( "&", "&amp;" ).replace( "<", "&lt;" ).replace( ">", "&gt;" )
                    out = out.replace( "&", "&amp;" ).replace( "<", "&lt;" ).replace( ">", "&gt;" )
                    AgGlobals.write_to_log( student_log_file, 'Return code: {}'.format( retcode ), 2 )
                    AgGlobals.write_to_log( student_log_file, out, 2 )
                    AgGlobals.write_to_log( student_log_file, err, 2 )
                    AgGlobals.write_to_log( student_log_file, '</pre></div>', 1 )

                    # AgGlobals.write_to_log( student_log_file, '{} {} {}'.format( retcode, out, err ), 1 )
                    return False

        else:
            print 'Error: Invalid repository uri: {}'.format( self.uri )
            AgGlobals.write_to_log( student_log_file, '<div class=error>Error: Invalid git URI - {}</div>'.format( self.uri ), 1 )
            # AgGlobals.write_to_log( student_log_file, '\tError: Invalid git uri' )
            return False

        return False


    def pull( self, path = '', grading_log_file = None, student_log_file = None ):
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
                                AgGlobals.write_to_log( grading_log_file, 'Success: Pull', 1 )
                                AgGlobals.write_to_log( student_log_file, '<h3 class=success>Success: Pull Repo</h3>', 1 )
                                # AgGlobals.write_to_log( student_log_file, 'Success: Pull' )
                                return True
                            else:
                                diff_time = now_time - prev_update
                                # print 'Difference: {}'.format( now_time - prev_update )
                                # print diff_time
                                # print now_time
                                # print prev_update
                                print 'There has been no change in the repo for {} days {} hours {} minutes'.format( diff_time.days, diff_time.seconds // 3600, ( diff_time.seconds // 60 ) % 60 )
                                AgGlobals.write_to_log( grading_log_file, 'Nothing updated since {}\n'.format( prev_update.strftime( '%x :: %X' ) ), 1 )
                                AgGlobals.write_to_log( grading_log_file, 'No activity for: {} days {} hours {} minutes\n'.format( diff_time.days, diff_time.seconds // 3600, ( diff_time.seconds // 60 ) % 60 ), 1 )


                                AgGlobals.write_to_log( student_log_file, '<div class=warning>Warning: Nothing updated since {}</div>'.format( prev_update.strftime( '%x :: %X' ) ), 1 )
                                AgGlobals.write_to_log( student_log_file, '<div class=warning>No activity for: {} days {} hours {} minutes</div>'.format( diff_time.days, diff_time.seconds // 3600, ( diff_time.seconds // 60 ) % 60 ), 1 )
                                # AgGlobals.write_to_log( student_log_file, 'Nothing updated since {}\n'.format( prev_update.strftime( '%x :: %X' ) ), 1 )
                                # AgGlobals.write_to_log( student_log_file, 'No activity for: {} days {} hours {} minutes\n'.format( diff_time.days, diff_time.seconds // 3600, ( diff_time.seconds // 60 ) % 60 ), 1 )
                                return False
                        else:
                            AgGlobals.write_to_log( grading_log_file, 'Error: pull\n', 1 )
                            AgGlobals.write_to_log( grading_log_file, '{} {} {}'.format( retcode, out, err ), 1 )

                            AgGlobals.write_to_log( student_log_file, '<div class=error>Error: Pulling Repo - {}</div>'.format( self.uri ), 1 )

                            AgGlobals.write_to_log( student_log_file, '<div class=error_out><pre>', 1 )
                            err = err.replace( "&", "&amp;" ).replace( "<", "&lt;" ).replace( ">", "&gt;" )
                            out = out.replace( "&", "&amp;" ).replace( "<", "&lt;" ).replace( ">", "&gt;" )
                            AgGlobals.write_to_log( student_log_file, 'Return code: {}'.format( retcode ), 2 )
                            AgGlobals.write_to_log( student_log_file, out, 2 )
                            AgGlobals.write_to_log( student_log_file, err, 2 )
                            AgGlobals.write_to_log( student_log_file, '</pre></div>', 1 )

                            # AgGlobals.write_to_log( student_log_file, '\tError: pull\n' )
                            # AgGlobals.write_to_log( student_log_file, '\t{} {} {}'.format( retcode, out, err ) )
                            return False
                    else:
                        print 'this is not a git repo'
                        AgGlobals.write_to_log( grading_log_file, '\tError: Not a valid git repo\n' )
                        AgGlobals.write_to_log( student_log_file, '<div class=error>Error: Invalid git URI - {}</div>'.format( self.uri ), 1 )
                        # AgGlobals.write_to_log( student_log_file, '\tError: Not a valid git repo\n' )
                        return False
                # os.chdir( cwd )
        else:
            print 'empty path'
            return False


    '''
    Copy a local repository to another local folder
    At the moment I'm making use of git itself to do the job. I clone the
    cloned student repo in students directory to the grading directory.
    If this has any bad implications I'd have to copy files using
    OS file copy utilities.
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

