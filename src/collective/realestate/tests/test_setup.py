# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from collective.realestate.testing import COLLECTIVE_REALESTATE_INTEGRATION_TESTING  # noqa

import unittest


class TestSetup(unittest.TestCase):
    """Test that collective.realestate is properly installed."""

    layer = COLLECTIVE_REALESTATE_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if collective.realestate is installed."""
        self.assertTrue(self.installer.isProductInstalled(
            'collective.realestate'))

    def test_browserlayer(self):
        """Test that ICollectiveRealestateLayer is registered."""
        from collective.realestate.interfaces import (
            ICollectiveRealestateLayer)
        from plone.browserlayer import utils
        self.assertIn(
            ICollectiveRealestateLayer,
            utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = COLLECTIVE_REALESTATE_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')
        roles_before = api.user.get_roles(TEST_USER_ID)
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.installer.uninstallProducts(['collective.realestate'])
        setRoles(self.portal, TEST_USER_ID, roles_before)

    def test_product_uninstalled(self):
        """Test if collective.realestate is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled(
            'collective.realestate'))

    def test_browserlayer_removed(self):
        """Test that ICollectiveRealestateLayer is removed."""
        from collective.realestate.interfaces import \
            ICollectiveRealestateLayer
        from plone.browserlayer import utils
        self.assertNotIn(
            ICollectiveRealestateLayer,
            utils.registered_layers())
