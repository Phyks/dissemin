# -*- encoding: utf-8 -*-

# Dissemin: open access policy enforcement tool
# Copyright (C) 2014 Antonin Delpeuch
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU Affero General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
#

from datetime import date
from io import BytesIO
import unittest
import django.test
import pytest
import os

from deposit.protocol import DepositResult
from deposit.protocol import RepositoryProtocol
from deposit.registry import protocol_registry
from django.contrib.auth.models import User
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.forms import Form
from django.test.utils import override_settings
from papers.models import OaiSource
from papers.models import Paper
from deposit.tasks import refresh_deposit_statuses

# 1x1 px image used as default logo for the repository
simple_png_image = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\tpHYs\x00\x00\x0b\x13\x00\x00\x0b\x13\x01\x00\x9a\x9c\x18\x00\x00\x00\x07tIME\x07\xdf\n\x12\x0c+\x19\x84\x1d/"\x00\x00\x00\x19tEXtComment\x00Created with GIMPW\x81\x0e\x17\x00\x00\x00\x0cIDAT\x08\xd7c\xa8\xa9\xa9\x01\x00\x02\xec\x01u\x90\x90\x1eL\x00\x00\x00\x00IEND\xaeB`\x82'

class DepositTest(django.test.TestCase):
    def test_refresh_deposit_statuses(self):
        # TODO: set up some DepositRecords + repository and protocol, to
        # so that this task actually does something
        refresh_deposit_statuses()

@pytest.mark.usefixtures("load_test_data")
class ProtocolTest(django.test.TestCase):
    """
    Set of generic tests that any protocol should pass.
    """

    def __init__(self, *args, **kwargs):
        super(ProtocolTest, self).__init__(*args, **kwargs)

    @override_settings(MEDIA_ROOT='mediatest/')
    def setUp(self):
        if type(self) is ProtocolTest:
            raise unittest.SkipTest("Base test")
        self.p1 = Paper.get_or_create(
                "This is a test paper",
                [self.r1.name, self.r2.name, self.r4.name],
                date(year=2014, month=2, day=15))

        self.username = 'mydepositinguser'
        self.password = 'supersecret'
        self.user = User.objects.create_user(username=self.username, email="my@email.com", password=self.password)
        self.testdir = os.path.dirname(os.path.abspath(__file__))
        self.pdfpath = os.path.join(self.testdir, 'data/blank.pdf')

    def setUpForProtocol(self, protocol_class, repository):

        self.oaisource, _ = OaiSource.objects.get_or_create(
            identifier='deposit_oaisource',
            name='Repository OAI source',
            default_pubtype='preprint')
        logo = InMemoryUploadedFile(
                BytesIO(simple_png_image),
                None, 'logo.png',
                'image/png', len(simple_png_image), None, None)
        self.repo = repository
        self.repo.oaisource = self.oaisource
        self.repo.logo = logo
        if not self.repo.description:
            self.repo.description = 'brsuatiercs'
        if not self.repo.name:
            self.repo.name = 'Test Repository'
        self.repo.protocol = protocol_class.__name__
        self.repo.save()
        protocol_registry.register(protocol_class)
        self.proto = protocol_class(self.repo)
        self.form = None


    def test_protocol_identifier(self):
        self.assertTrue(len(self.proto.protocol_identifier()) > 1)

    def test_init_deposit(self):
        retval = self.proto.init_deposit(self.p1, self.user)
        self.assertIs(type(retval), bool)

    def test_get_form_return_type(self):
        self.proto.init_deposit(self.p1, self.user)
        retval = self.proto.get_form()
        self.assertIsInstance(retval, Form)

    def test_deposit_page(self):
        self.assertEqual(self.user.username, self.username)
        self.assertTrue(self.client.login(username=self.username, password=self.password))
        r = self.getPage('upload_paper', kwargs={'pk': self.p1.pk})
        self.assertEqual(r.status_code, 200)

    def dry_deposit(self, paper, **form_fields):
        """
        This is not a test by itself - it's a method
        subclasses can call to create a fake deposit
        (if the protocol supports it!)
        """
        return self.deposit(paper, dry_run=True, **form_fields)

    def deposit(self, paper, dry_run=False, **form_fields):
        enabled = self.proto.init_deposit(paper, self.user)
        self.assertTrue(enabled)

        args = self.proto.get_form_initial_data()
        args.update(form_fields)

        form = self.proto.get_bound_form(args)
        if not form.is_valid():
            print(form.errors)
        self.assertTrue(form.is_valid())
        pdf = self.pdfpath
        deposit_result = self.proto.submit_deposit_wrapper(pdf,
                                                           form, dry_run=dry_run)
        self.assertIsInstance(deposit_result, DepositResult)
        self.assertIsInstance(deposit_result.additional_info, list)
        for i in deposit_result.additional_info:
            self.assertNotEqual(i.get('label'), None)
            self.assertNotEqual(i.get('value'), None)
        return deposit_result

    def assertEqualOrLog(self, a, b):
        """
        Same as assertEqual but prints logs before failing
        if the two quantities are not equal.
        """
        if a != b:
            print(self.proto._logs)
        self.assertEqual(a, b)

class ProtocolRegistryTest(django.test.TestCase):
    def test_get(self):
        c = protocol_registry.get('ZenodoProtocol')
        self.assertTrue(issubclass(c, RepositoryProtocol))

