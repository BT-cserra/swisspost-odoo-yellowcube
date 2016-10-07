# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (c) 2016 brain-tec AG (http://www.braintec-group.com)
#    All Right Reserved
#
#    See LICENSE file for full licensing details.
##############################################################################
import paramiko
import time
import tempfile
import logging
from StringIO import StringIO
from openerp.exceptions import UserError
from openerp.tools import ustr
_logger = logging.getLogger(__name__)
# _logger.setLevel(logging.DEBUG)


class SFTPTransport:

    transport = None
    connection = None

    def __init__(self, backend):
        self.backend = backend
        self.username = backend.transport_id.sftp_username or None
        self.password = backend.transport_id.sftp_password or None
        self.path = backend.transport_id.sftp_path or None
        self.rsa_key = backend.transport_id.sftp_rsa_key or None
        self.retries = 3

    def test_connection(self):
        with self:
            _logger.debug(self.list_dir())
        return True

    def send_file(self, connector_file):
        with tempfile.NamedTemporaryFile() as temp:
            temp.write(connector_file.content)
            temp.flush()
            # Requires version 1.7.7
            self.connection.put(temp.name, connector_file.name, confirm=False)
            connector_file.state = 'done'

    def get_file(self, filename):
        with tempfile.NamedTemporaryFile() as temp:
            self.connection.get(filename, temp.name)
            content = file(temp.name).read()
            self.backend.env['stock_connector.file'].create({
                'backend_id': self.backend.id,
                'name': filename,
                'transmit': 'in',
                'content': ustr(content),
            })

    def change_dir(self, path):
        self.connection.chdir(path)

    def list_dir(self):
        result = []
        for name in self.connection.listdir():
            lstat = str(self.connection.lstat(name))
            if lstat[0] == '-':
                result.append(name)
        return result

    def open(self):
        """
        Opens an SFTP connection.
        """
        # Gets the key.
        if self.rsa_key:
            rsa_key = paramiko.RSAKey.from_private_key(StringIO(self.rsa_key))
        else:
            rsa_key = None

        # Sets the parameters to use.
        path = self.path
        port = 22  # Default port for SFTP.
        retries = self.retries
        if path is None:
            raise UserError("Missing parameter 'path'")
        if ':' in path:
            t = path.split(':')
            path = t[0]
            port = int(t[1])

        while self.connection is None:
            try:
                # Opens the connection.
                transport = paramiko.Transport((path, port))
                transport.connect(username=self.username,
                                  password=self.password,
                                  pkey=rsa_key)
                ssh = paramiko.SFTPClient.from_transport(transport)
                self.transport = transport
                self.connection = ssh
            except:
                if retries <= 0:
                    raise
                else:
                    retries -= 1
                    time.sleep(1)

    def close(self):
        self.connection.close()
        self.transport.close()
        self.connection = None
        self.transport = None

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()