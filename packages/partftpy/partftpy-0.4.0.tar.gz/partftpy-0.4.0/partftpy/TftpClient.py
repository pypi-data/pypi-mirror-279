# coding: utf-8
# vim: ts=4 sw=4 et ai:
from __future__ import print_function, unicode_literals

"""This module implements the TFTP Client functionality. Instantiate an
instance of the client, and then use its upload or download method. Logging is
performed via a standard logging object set in TftpShared."""


import logging
import socket
import types

from .TftpContexts import TftpContextClientDownload, TftpContextClientUpload
from .TftpPacketTypes import *
from .TftpShared import *

log = logging.getLogger("partftpy.TftpClient")


class TftpClient(TftpSession):
    """This class is an implementation of a tftp client. Once instantiated, a
    download can be initiated via the download() method, or an upload via the
    upload() method."""

    def __init__(
        self, host, port=69, options=None, localip="", af_family=socket.AF_INET
    ):
        TftpSession.__init__(self)
        self.context = None
        self.host = host
        self.iport = port
        self.filename = None
        self.options = options or {}
        self.localip = localip
        self.af_family = af_family
        if "blksize" in self.options:
            size = self.options["blksize"]
            tftpassert(int == type(size), "blksize must be an int")
            if size < MIN_BLKSIZE or size > MAX_BLKSIZE:
                raise TftpException("Invalid blksize: %d" % size)
        else:
            self.options["blksize"] = DEF_BLKSIZE

    def download(
        self,
        filename,
        output,
        packethook=None,
        timeout=SOCK_TIMEOUT,
        retries=DEF_TIMEOUT_RETRIES,
        ports=None,
    ):
        """This method initiates a tftp download from the configured remote
        host, requesting the filename passed. It writes the file to output,
        which can be a file-like object or a path to a local file. If a
        packethook is provided, it must be a function that takes two
        parameters, the first being a copy of each packet received in the
        form of a TftpPacket object, and the second being the TftpContext
        for this transfer, which can be inspected for more accurate statistics,
        progress estimates and such. The timeout parameter may be used to
        override the default SOCK_TIMEOUT setting, which is the amount of time
        that the client will wait for a receive packet to arrive.
        The retires parameter may be used to override the default DEF_TIMEOUT_RETRIES
        settings, which is the amount of retransmission attempts the client will initiate
        after encountering a timeout.

        Note: If output is a hyphen, stdout is used."""
        # We're downloading.
        t = "DL-ctx: host = %s, port = %s, filename = %s, options = %s, packethook = %s, timeout = %s"
        log.debug(t, self.host, self.iport, filename, self.options, packethook, timeout)
        self.context = TftpContextClientDownload(
            self.host,
            self.iport,
            filename,
            output,
            self.options,
            packethook,
            timeout,
            retries=retries,
            localip=self.localip,
            af_family=self.af_family,
            ports=ports,
        )
        self.context.start()
        # Download happens here
        self.context.end()

        st = self.context.metrics
        spd = st.kbps / 8192.0

        t = "DL done: "
        if st.duration == 0:
            t += "Duration too short, rate undetermined"
        else:
            t += "%d byte, %.2f sec, %.4f MiB/s, " % (st.bytes, st.duration, spd)

        t += "%d bytes resent, %d dupe pkts" % (st.resent_bytes, st.dupcount)
        log.info(t)

    def upload(
        self,
        filename,
        input,
        packethook=None,
        timeout=SOCK_TIMEOUT,
        retries=DEF_TIMEOUT_RETRIES,
        ports=None,
    ):
        """This method initiates a tftp upload to the configured remote host,
        uploading the filename passed. It reads the file from input, which
        can be a file-like object or a path to a local file. If a packethook
        is provided, it must be a function that takes two parameters,
        the first being a copy of each packet received in the form of
        a TftpPacket object, and the second being the TftpContext for
        this transfer, which can be inspected for more accurate statistics,
        progress estimates, etc. The timeout parameter may be used to override
        the default SOCK_TIMEOUT setting, which is the amount of time that
        the client will wait for a DAT packet to be ACKd by the server.
        The retires parameter may be used to override the default DEF_TIMEOUT_RETRIES
        settings, which is the amount of retransmission attempts the client will initiate
        after encountering a timeout.

        Note: If input is a hyphen, stdin is used."""
        self.context = TftpContextClientUpload(
            self.host,
            self.iport,
            filename,
            input,
            self.options,
            packethook,
            timeout,
            retries=retries,
            localip=self.localip,
            ports=ports,
        )
        self.context.start()
        # Upload happens here
        self.context.end()

        st = self.context.metrics
        spd = st.kbps / 8192.0

        t = "Upload done: "
        if st.duration == 0:
            t += "Duration too short, rate undetermined; "
        else:
            t += "%d byte, %.2f sec, %.4f MiB/s, " % (st.bytes, st.duration, spd)

        t += "%d bytes resent, %d dupe pkts" % (st.resent_bytes, st.dupcount)
        log.info(t)
