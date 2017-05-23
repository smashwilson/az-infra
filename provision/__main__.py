import sys
import traceback

from provision.context import Context
from provision.output import error
from provision import server
from provision import cleanup

context = Context(sys.argv)
try:
    server.provision(context)
    cleanup.retire(context)
except:
    error('provisioning error\n{}'.format(traceback.format_exc()))
    cleanup.rollback(context)
