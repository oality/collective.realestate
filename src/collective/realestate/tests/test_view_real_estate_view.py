# -*- coding: utf-8 -*-
from collective.realestate.testing import COLLECTIVE_REALESTATE_FUNCTIONAL_TESTING  # noqa
from collective.realestate.testing import COLLECTIVE_REALESTATE_INTEGRATION_TESTING  # noqa
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
        api.content.create(self.portal, 'Real estate', 'my-realestate')

    def test_real_estate_view_is_registered(self):
        view = getMultiAdapter(
            (self.portal['my-realestate'], self.portal.REQUEST),
            name='real-estate-view'
        )
        self.assertTrue('<div class="figures' in view(),
                        'class figures row not found in real-estate-view')

    def test_real_estate_view_in_my_collection(self):
        with self.assertRaises(ComponentLookupError):
            getMultiAdapter(
                (self.portal['my-collection'], self.portal.REQUEST),
                name='real-estate-view'
            )


class ViewsFunctionalTest(unittest.TestCase):

    layer = COLLECTIVE_REALESTATE_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
