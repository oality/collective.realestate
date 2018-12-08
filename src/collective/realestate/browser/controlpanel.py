# -*- coding: utf-8 -*-
from collective.realestate import _
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper
from plone.app.registry.browser.controlpanel import RegistryEditForm
from plone.app.z3cform.wysiwyg import WysiwygFieldWidget
from plone.autoform import directives
from plone.formwidget.geolocation.field import GeolocationField
from plone.z3cform import layout
from zope import schema as zchema
from zope.interface import Interface
from plone.formwidget.geolocation.interfaces import IGeolocation


class IRealEstateSettings(Interface):
    """ Define settings data structure """

    owner_email = zchema.ASCIILine(
        title=_(u'Owner e-mail'),
        description=_(u'Default e-mail use to send request reservation.')
    )

    start_high = zchema.TextLine(
        title=_(u'High season starting'),
        description=_(u'Date like 01/07 for first July'),
        default=_(u'01/07')
    )

    start_low = zchema.TextLine(
        title=_(u'High season starting'),
        description=_(u'Date like 01/10 for first October'),
        default=_(u'01/10')
    )

    directives.widget(condition=WysiwygFieldWidget)
    condition = zchema.Text(
        title=_(u'General condition'),
        description=_(u'This text is added below all real estate.')
    )

    marker_icons = zchema.ASCIILine(
        title=_(u'Marker icons'),
        description=_(u'Update marker path.'),
        required=False
    )
    latitude = zchema.TextLine(title=_(u'Latitude'), required=False)
    longitude = zchema.TextLine(title=_(u'Longitude'), required=False)


class RealEstateSettingsEditForm(RegistryEditForm):
    """
    Define form logic
    """
    schema = IRealEstateSettings
    schema_prefix = 'collective.realestate'
    label = _(u'Real Estate settings')


RealEstateSettingsView = layout.wrap_form(
    RealEstateSettingsEditForm, ControlPanelFormWrapper)
