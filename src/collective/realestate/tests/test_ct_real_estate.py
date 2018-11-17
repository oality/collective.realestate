# -*- coding: utf-8 -*-
from collective.realestate.content.real_estate import IRealEstate  # NOQA E501
from collective.realestate.testing import COLLECTIVE_REALESTATE_INTEGRATION_TESTING  # noqa
from plone import api
from plone.api.exc import InvalidParameterError
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import createObject
from zope.component import queryUtility

import unittest




class RealEstateIntegrationTest(unittest.TestCase):

    layer = COLLECTIVE_REALESTATE_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def test_ct_real_estate_schema(self):
        fti = queryUtility(IDexterityFTI, name='Real estate')
        schema = fti.lookupSchema()
        self.assertEqual(IRealEstate, schema)

    def test_ct_real_estate_fti(self):
        fti = queryUtility(IDexterityFTI, name='Real estate')
        self.assertTrue(fti)

    def test_ct_real_estate_factory(self):
        fti = queryUtility(IDexterityFTI, name='Real estate')
        factory = fti.factory
        obj = createObject(factory)

        self.assertTrue(
            IRealEstate.providedBy(obj),
            u'IRealEstate not provided by {0}!'.format(
                obj,
            ),
        )

    def test_ct_real_estate_adding(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        obj = api.content.create(
            container=self.portal,
            type='Real estate',
            id='real_estate',
        )

        self.assertTrue(
            IRealEstate.providedBy(obj),
            u'IRealEstate not provided by {0}!'.format(
                obj.id,
            ),
        )

    def test_ct_real_estate_globally_addable(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        fti = queryUtility(IDexterityFTI, name='Real estate')
        self.assertTrue(
            fti.global_allow,
            u'{0} is not globally addable!'.format(fti.id)
        )

    def test_ct_real_estate_filter_content_type_true(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        fti = queryUtility(IDexterityFTI, name='Real estate')
        portal_types = self.portal.portal_types
        parent_id = portal_types.constructContent(
            fti.id,
            self.portal,
            'real_estate_id',
            title='Real estate container',
         )
        self.parent = self.portal[parent_id]
        with self.assertRaises(InvalidParameterError):
            api.content.create(
                container=self.parent,
                type='Document',
                title='My Content',
            )
