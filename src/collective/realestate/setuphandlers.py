# -*- coding: utf-8 -*-
from plone import api
from Products.CMFPlone.interfaces import INonInstallable
from Products.ZCatalog.Catalog import CatalogError
from zope.interface import implementer

import logging


indexed_fields = [
    "persons",
    "rooms",
    "bathrooms",
    "area",
    "parking",
    "pets",
    "type",
    "price",
    "sale_or_rent",
    "sold",
    "reference",
    "new",
]
logger = logging.getLogger("setuphandlers realestate")


@implementer(INonInstallable)
class HiddenProfiles(object):
    def getNonInstallableProfiles(self):
        """Hide uninstall profile from site-creation and quickinstaller."""
        return ["collective.realestate:uninstall"]


def post_install(context):
    """Post install script"""
    for indexed_field in indexed_fields:
        add_index(indexed_field)
    # api.portal.set_registry_record('plone.resources.development', True)
    api.portal.set_registry_record(
        "plone.allowed_sizes",
        [
            u"large 768:768",
            u"preview 400:400",
            u"mini 200:200",
            u"thumb 128:128",
            u"tile 64:64",
            u"icon 32:32",
            u"listing 16:16",
            u"banner 2000:600",
        ],
    )
    key = "collective.behavior.banner.browser.controlpanel.IBannerSettingsSchema.banner_scale"  # noqa
    api.portal.set_registry_record(key, "banner")
    # key = 'plone.default_language'
    # api.portal.set_registry_record(key, 'fr')
    # api.portal.set_registry_record('plone.available_languages', ['fr', 'es'])
    # api.content.create(type='LRF', id='fr', title=u'Français', container=api.portal.get())
    # api.content.create(type='LRF', id='es', title=u'Espagnol', container=api.portal.get())


def uninstall(context):
    """Uninstall script"""
    for indexed_field in indexed_fields:
        remove_index(indexed_field)


def add_index(field_name):
    catalog = api.portal.get_tool("portal_catalog")
    indexables = []
    try:
        catalog.addIndex(field_name, "FieldIndex")
        indexables.append(field_name)
    except CatalogError:
        logger.info(
            "Index {0} already exists, we hope it is proper configured".format(
                field_name
            )
        )
    if len(indexables) > 0:
        logger.info("Indexing new indexes {0}.".format(", ".join(indexables)))
        catalog.manage_reindexIndex(ids=indexables)


def remove_index(field_name):
    catalog = api.portal.get_tool("portal_catalog")
    try:
        catalog.delIndex(field_name)
    except CatalogError:
        logging.info(
            "Could not delete index {0} something is not right.".format(field_name)
        )
