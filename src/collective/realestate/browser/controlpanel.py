# -*- coding: utf-8 -*-
from collective.realestate import _
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper
from plone.app.registry.browser.controlpanel import RegistryEditForm
from plone.z3cform import layout
from zope import schema as zopeschema
from zope.interface import Interface


class IRealEstateSettings(Interface):
    """ Define settings data structure """

    owner_email = zopeschema.ASCIILine(
        title=_(u'Owner e-mail'),
        description=_(u'Default e-mail use to send request reservation.')
    )


class RealEstateSettingsEditForm(RegistryEditForm):
    """
    Define form logic
    """
    schema = IRealEstateSettings
    schema_prefix = 'collective.realestate'
    label = _(u'Real Estate settings')


RealEstateSettingsView = layout.wrap_form(
    RealEstateSettingsEditForm, ControlPanelFormWrapper)
