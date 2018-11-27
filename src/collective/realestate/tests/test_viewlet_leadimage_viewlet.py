# -*- coding: utf-8 -*-
from collective.realestate.interfaces import ICollectiveRealestateLayer
from collective.realestate.testing import COLLECTIVE_REALESTATE_FUNCTIONAL_TESTING
from collective.realestate.testing import COLLECTIVE_REALESTATE_INTEGRATION_TESTING
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from Products.Five.browser import BrowserView as View
from zope.component import queryMultiAdapter
from zope.interface import alsoProvides
from zope.viewlet.interfaces import IViewletManager

import unittest


class ViewletIntegrationTest(unittest.TestCase):

    layer = COLLECTIVE_REALESTATE_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.app = self.layer['app']
        self.request = self.app.REQUEST
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        api.content.create(self.portal, 'Document', 'other-document')
        api.content.create(self.portal, 'Collection', 'my-collection')

    def test_leadimage_viewlet_is_registered(self):
        view = View(self.portal['other-document'], self.request)
        manager_name = 'plone.abovecontenttitle'
        alsoProvides(self.request, ICollectiveRealestateLayer)
        manager = queryMultiAdapter(
            (self.portal['other-document'], self.request, view),
            IViewletManager,
            manager_name,
            default=None
        )
        self.assertIsNotNone(manager)
        manager.update()
        my_viewlet = [v for v in manager.viewlets if v.__name__ == 'contentleadimage']  # NOQA: E501
        self.assertEqual(len(my_viewlet), 1)

    def test_myviewlet_in_my_collection(self):
        view = View(self.portal['my-collection'], self.request)
        manager_name = 'plone.abovecontenttitle'
        alsoProvides(self.request, ICollectiveRealestateLayer)
        manager = queryMultiAdapter(
            (self.portal['my-collection'], self.request, view),
            IViewletManager,
            manager_name,
            default=None
        )
        self.assertIsNotNone(manager)
        manager.update()
        my_viewlet = [v for v in manager.viewlets if v.__name__ == 'contentleadimage']  # NOQA: E501
        self.assertEqual(len(my_viewlet), 0)


class ViewletFunctionalTest(unittest.TestCase):

    layer = COLLECTIVE_REALESTATE_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])