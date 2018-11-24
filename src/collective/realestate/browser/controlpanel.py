# -*- coding: utf-8 -*-
from collective.realestate import _
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper
from plone.app.registry.browser.controlpanel import RegistryEditForm
from plone.schema.email import Email
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
    schema_prefix = "collective.realestate"
    label = _(u'Real Estate settings')


RealEstateSettingsView = layout.wrap_form(
    RealEstateSettingsEditForm, ControlPanelFormWrapper)

#
# class RealEstateSettingsView(BrowserView):
#     """
#     View which wrap the settings form using ControlPanelFormWrapper to a HTML boilerplate frame.
#     """
#
#     def render(self):
#         view_factor = layout.wrap_form(
#             RealEstateSettingsEditForm,
#             ControlPanelFormWrapper
#         )
#         view = view_factor(self.context, self.request)
#         return view()


# from plone.app.controlpanel.form import ControlPanelForm
# from z3c.form import field
# class RealEstateControlPanel(ControlPanelForm):
#
#     label = _('Real Estate settings')
#     description = _('Lets you change the settings of Real Estate')
#     form_fields = field.Fields(IRealEstateSettings)
