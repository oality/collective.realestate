# -*- coding: utf-8 -*-
from collective.realestate.testing import COLLECTIVE_REALESTATE_FUNCTIONAL_TESTING
from collective.realestate.testing import COLLECTIVE_REALESTATE_INTEGRATION_TESTING
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from zope.component import getMultiAdapter
from zope.component.interfaces import ComponentLookupError

import unittest


class ViewsIntegrationTest(unittest.TestCase):

    layer = COLLECTIVE_REALESTATE_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        api.content.create(self.portal, 'Folder', 'other-folder')
        api.content.create(self.portal, 'Collection', 'my-collection')

    def test_booking_view_is_registered(self):
        view = getMultiAdapter(
            (self.portal['other-folder'], self.portal.REQUEST),
            name='booking-view'
        )
        self.assertTrue(view(), 'booking-view is not found')
        self.assertTrue(
            'Sample View' in view(),
            'Sample View is not found in booking-view'
        )
        self.assertTrue(
            'Sample View' in view(),
            'A small message is not found in booking-view'
        )

    def test_booking_view_in_my_collection(self):
        with self.assertRaises(ComponentLookupError):
            getMultiAdapter(
                (self.portal['my-collection'], self.portal.REQUEST),
                name='booking-view'
            )


class ViewsFunctionalTest(unittest.TestCase):

    layer = COLLECTIVE_REALESTATE_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
