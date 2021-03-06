#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

'''
Faraday Penetration Test IDE
Copyright (C) 2013  Infobyte LLC (http://www.infobytesec.com/)
See the file 'doc/LICENSE' for the license information

'''

import unittest
import sys
import os
sys.path.append(os.path.abspath(os.getcwd()))
from plugins.repo.acunetix.plugin import AcunetixPlugin
from model.common import factory
from persistence.server.models import (
    Vuln,
    Credential,
    VulnWeb,
    Note,
    Host,
    Service,
    Interface
)
from plugins.modelactions import modelactions


class AcunetixParserTest(unittest.TestCase):

    cd = os.path.dirname(os.path.realpath(__file__))

    def setUp(self):
        self.plugin = AcunetixPlugin()
        factory.register(Host)
        factory.register(Interface)
        factory.register(Service)
        factory.register(Vuln)
        factory.register(VulnWeb)
        factory.register(Note)
        factory.register(Credential)

    def test_Plugin_creates_apropiate_objects(self):
        self.plugin.processReport(self.cd + '/acunetix_xml')
        action = self.plugin._pending_actions.get(block=True)
        self.assertEqual(action[0], modelactions.ADDHOST)
        self.assertEqual(action[1].name, "5.175.17.140")
        action = self.plugin._pending_actions.get(block=True)
        self.assertEqual(action[0], modelactions.ADDINTERFACE)
        self.assertEqual(action[2].name, "5.175.17.140")
        action = self.plugin._pending_actions.get(block=True)
        self.assertEqual(action[0], modelactions.ADDSERVICEINT)
        self.assertEqual(action[3].ports, [80])
        self.assertEqual(action[3].name, 'http')
        self.assertEqual(action[3].protocol, 'tcp')
        action = self.plugin._pending_actions.get(block=True)
        self.assertEqual(action[0], modelactions.ADDNOTESRV)
        action = self.plugin._pending_actions.get(block=True)
        action = self.plugin._pending_actions.get(block=True)
        self.assertEqual(action[0], modelactions.ADDVULNWEBSRV)
        self.assertEqual(action[3].name, "ASP.NET error message")


if __name__ == '__main__':
    unittest.main()
