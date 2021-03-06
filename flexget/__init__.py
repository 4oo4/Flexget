#!/usr/bin/python
import logging
import os
import sys

# __version__ import need to be first in order to avoid circular import within logger
from ._version import __version__  # noqa
from flexget import logger
from flexget.manager import Manager


log = logging.getLogger('main')


def main(args=None):
    """Main entry point for Command Line Interface"""

    try:
        logger.initialize()

        try:
            manager = Manager(args)
        except (IOError, ValueError) as e:
            if _is_debug():
                import traceback

                traceback.print_exc()
            else:
                print('Could not instantiate manager: %s' % e, file=sys.stderr)
            sys.exit(1)

        try:
            if manager.options.profile:
                try:
                    import cProfile as profile
                except ImportError:
                    import profile
                profile.runctx(
                    'manager.start()',
                    globals(),
                    locals(),
                    os.path.join(manager.config_base, manager.options.profile),
                )
            else:
                manager.start()
        except (IOError, ValueError) as e:
            if _is_debug():
                import traceback

                traceback.print_exc()
            else:
                print('Could not start manager: %s' % e, file=sys.stderr)

            sys.exit(1)
    except KeyboardInterrupt:
        if _is_debug():
            import traceback

            traceback.print_exc()

        print('Killed with keyboard interrupt.', file=sys.stderr)
        sys.exit(1)


def _is_debug():
    return any(
        arg in ['debug', '--debug', '--loglevel=trace', '--loglevel=debug']
        for arg in [a.lower() for a in sys.argv]
    )
