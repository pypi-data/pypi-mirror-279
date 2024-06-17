#!/usr/bin/env python
# vim: ts=4 sw=4 et ai:
# -*- coding: utf8 -*-

import logging
import socket
import sys
from optparse import OptionParser

from partftpy.TftpServer import TftpServer
from partftpy.TftpShared import TftpException

log = logging.getLogger("partftpy")
log.setLevel(logging.INFO)

# console handler
handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
default_formatter = logging.Formatter("[%(asctime)s] %(message)s")
handler.setFormatter(default_formatter)
log.addHandler(handler)


def main():
    usage = ""
    parser = OptionParser(usage=usage)
    parser.add_option(
        "-i",
        "--ip",
        type="string",
        help="ip address to bind to (default: INADDR_ANY)",
        default="",
    )
    parser.add_option(
        "-p",
        "--port",
        type="int",
        help="local port to use (default: 69)",
        default=69,
    )
    parser.add_option(
        "-r",
        "--root",
        type="string",
        help="path to serve from",
        default=None,
    )
    parser.add_option(
        "-q",
        "--quiet",
        action="store_true",
        default=False,
        help="Do not log unless it is critical",
    )
    parser.add_option(
        "-d",
        "--debug",
        action="store_true",
        default=False,
        help="upgrade logging from info to debug",
    )
    options, args = parser.parse_args()

    if options.debug:
        log.setLevel(logging.DEBUG)
        # increase the verbosity of the formatter
        debug_formatter = logging.Formatter(
            "[%(asctime)s%(msecs)03d] %(levelname)s [%(name)s:%(lineno)s] %(message)s"
        )
        handler.setFormatter(debug_formatter)
    elif options.quiet:
        log.setLevel(logging.WARNING)

    if not options.root:
        parser.print_help()
        sys.exit(1)

    fam = socket.AF_INET6 if ":" in options.ip else socket.AF_INET

    server = TftpServer(options.root)
    try:
        server.listen(options.ip, options.port, af_family=fam)
    except TftpException as err:
        sys.stderr.write("%s\n" % str(err))
        sys.exit(1)
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
