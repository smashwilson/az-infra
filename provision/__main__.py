import sys
import traceback

from provision.context import Context
from provision.config import Action
from provision.output import error
from provision import server
from provision import cleanup
from provision import notify

context = Context(sys.argv)
if context.config.action == Action.PROVISION:
    try:
        server.provision(context)
        cleanup.retire(context)
        notify.success(context)
    except:
        formatted_tb = traceback.format_exc()
        error('provisioning error\n{}'.format(formatted_tb))
        cleanup.rollback(context)
        notify.failure(context, formatted_tb)
elif context.config.action == Action.DELETE:
    try:
        cleanup.retire(context)
    except:
        error('unable to delete resources\n{}'.format(traceback.format_exc()))
