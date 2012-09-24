import sys
from _colors import Colors

class Logger( object ):

  def __init__( self, filename="fyborg_log.txt", debug_mode=False ):
    '''
    Initialize this logger with a log file and a verbose flag.
    '''
    self.__debug_mode = debug_mode
    self.terminal = sys.__stdout__
    self.log = open( filename, "a" )

  def write( self, message ):
    '''
    Write both to the terminal and to the logfile.
    '''
    self.terminal.write( message )
    self.log.write( Colors.strip( message ) ) # strip color codes here

  def flush( self ):
    '''
    Flush both the terminal and the log file.
    '''
    self.terminal.flush()
    self.log.flush()

  def fileno( self ):
    '''
    Return the identifier of the log file. This is required for use in connection with
    the subprocess module.
    '''
    return self.log.fileno()

  def debug( self, txt ):
    '''
    Print a debug message which always go to the log file but only appears on the terminal if
    debug mode is active. 
    '''
    if self.__debug_mode:
      self.terminal.write( 'DEBUG: ' + txt + '\n' )
    self.log.write( Colors.strip( txt ) + '\n' ) # strip color codes here
