import sys
import traceback

from provision.context import Context
from provision.config import Action
from provision.output import error
from provision import server
from provision import cleanup

context = Context(sys.argv)
if context.config.action == Action.PROVISION:
    try:
        server.provision(context)
        cleanup.retire(context)
    except:
        error('provisioning error\n{}'.format(traceback.format_exc()))
        cleanup.rollback(context)
elif context.config.action == Action.DELETE:
    try:
        cleanup.retire(context)
    except:
        error('unable to delete resources\n{}'.format(traceback.format_exc()))
