import logging
import signal
import sys
import inspect

import odoo
from odoo.tools import config
from odoo.cli.shell import raise_keyboard_interrupt

_logger = logging.getLogger(__name__)


class OdooRunner():
    def __init__(self, args, entrypoint):
        assert callable(entrypoint), "entrypoint is not a function"
        self.entrypoint = entrypoint

        assert isinstance(args, list), "args has to be a list of strings"
        args.append('--no-http')
        config.parse_config(args)
        assert config['db_name'], "db_name is missing"

        odoo.cli.server.report_configuration()
        odoo.service.server.start(preload=[], stop=True)
        signal.signal(signal.SIGINT, raise_keyboard_interrupt)

    def run(self, *args, **kwargs):
        caller = inspect.getframeinfo(sys._getframe(1)).filename
        registry = odoo.registry(config['db_name'])
        with registry.cursor() as cr:
            uid = odoo.SUPERUSER_ID
            ctx = odoo.api.Environment(cr, uid, {})['res.users'].context_get()
            env = odoo.api.Environment(cr, uid, ctx)

            _logger.info(f"Running script '{caller}'")
            result = self.entrypoint(env, *args, **kwargs)
            cr.rollback()

        return result
