#
# The XBUILD configuration file.
#
# (c) 2012 The XTK Developers <dev@goXTK.com>
#

import os
import sys
import tempfile


# STRINGS
SOFTWARE = 'Fyborg'
SOFTWARE_SHORT = 'Fyborg'
SOFTWARE_DESCRIPTION = 'THE ULTIMATE SCALAR MAPPING FRAMEWORK FOR TRACKVIS (.TRK) FILES'
SOFTWARE_HOMEPAGE = 'http://fnndsc.github.com'

NAMESPACE = 'fyborg'

LICENSE_HEADER = '''# 
#   ___         __                        
# .'  _|.--.--.|  |--..-----..----..-----.
# |   _||  |  ||  _  ||  _  ||   _||  _  |
# |__|  |___  ||_____||_____||__|  |___  |
#       |_____|                    |_____|
#
# THE ULTIMATE SCALAR MAPPING FRAMEWORK FOR TRACKVIS (.TRK) FILES
#
#
#
# (c) 2012 FNNDSC, Children's Hospital Boston 
#
#'''


# PATHS
EXCLUDES_PATH = ['lib', 'testing', 'deps', 'utils']
INCLUDES_PATH = ['csg', 'JXG'] # force inclusion of sub folders in an excluded directory for dependency generation

REPOSITORY_URL = 'https://github.com/FNNDSC/fyborg/'

CDASH_SUBMIT_URL = 'http://x.babymri.org/cdash/submit.php?project=' + SOFTWARE_SHORT

XBUILD_PATH = os.path.abspath( os.path.dirname( sys.argv[0] ) )
SOFTWARE_PATH = os.path.normpath( XBUILD_PATH + os.sep + '..' + os.sep )

CLOSURELIBRARY_PATH = os.path.normpath( os.path.join( SOFTWARE_PATH, 'lib/closure-library/closure/' ) )
CLOSURELIBRARY_PYTHON_PATH = os.path.normpath( os.path.join( CLOSURELIBRARY_PATH, 'bin/build/' ) )
CLOSUREBUILDER_PATH = os.path.normpath( os.path.join( CLOSURELIBRARY_PYTHON_PATH, 'closurebuilder.py' ) )
CLOSUREDEPSWRITER_PATH = os.path.normpath( os.path.join( CLOSURELIBRARY_PYTHON_PATH, 'depswriter.py' ) )
CLOSURECOMPILER_PATH = os.path.normpath( os.path.join( SOFTWARE_PATH, 'lib/closure-library/compiler-latest/compiler.jar' ) )
CLOSUREGOOGBASE_PATH = os.path.normpath( os.path.join( CLOSURELIBRARY_PATH, 'goog/base.js' ) )

DOC_TEMPLATES_PATH = os.path.normpath( os.path.join( XBUILD_PATH, '_core', 'templates/' ) )

BUILD_OUTPUT_PATH = os.path.normpath( os.path.join( XBUILD_PATH , SOFTWARE_SHORT.lower() + '.js' ) )
DEPS_OUTPUT_PATH = os.path.normpath( os.path.join( SOFTWARE_PATH , SOFTWARE_SHORT.lower() + '-deps.js' ) )
DOC_OUTPUT_PATH = os.path.normpath( os.path.join( SOFTWARE_PATH , 'doc/' ) )

TEMP_PATH = tempfile.gettempdir()
