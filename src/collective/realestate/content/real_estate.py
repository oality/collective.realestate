# -*- coding: utf-8 -*-
from collective.realestate import _
# from plone.app.textfield import RichText
# from plone.autoform import directives
from plone.dexterity.content import Container
# from plone.namedfile import field as namedfile
from plone.supermodel import model
# from plone.supermodel.directives import fieldset
# from z3c.form.browser.radio import RadioFieldWidget
from zope import schema
from zope.interface import implementer


class IRealEstate(model.Schema):
    """ Marker interface and Dexterity Python Schema for RealEstate
    """
    # If you want, you can load a xml model created TTW here
    # and customize it in Python:

    # model.load('real_estate.xml')

    # directives.widget(level=RadioFieldWidget)
    type = schema.Choice(
        title=_(u'Type of real estate'),
        vocabulary=u'collective.realestate.RealEstateTypes',
    )

    # text = RichText(
    #     title=_(u'Text'),
    #     required=False
    # )

    persons = schema.Int(
        title=_(u'Number of peron(s)'),
        required=False
    )

    rooms = schema.Int(
        title=_(u'Number of bedroom(s)'),
        required=False
    )

    bathrooms = schema.Int(
        title=_(u'Number of bathroom(s)'),
        required=False
    )

    area = schema.Float(
        title=_(u'Area'),
        description=_(u'Area in m²'),
        required=False
    )

    parking = schema.Bool(
        title=_(u'Parking'),
        description=_(u'Is there a free parking'),
        required=False
    )

    pets = schema.Bool(
        title=_(u'Pets'),
        description=_(u'Are pets authorised?'),
        required=False
    )

    low_price = schema.Float(
        title=_(u'Price low season (for one day)'),
        required=False
    )

    high_price = schema.Float(
        title=_(u'Price high season (for one day)'),
        required=False
    )

    # fieldset('Images', fields=['logo', 'advertisement'])
    # logo = namedfile.NamedBlobImage(
    #     title=_(u'Logo'),
    #     required=False,
    # )

    # advertisement = namedfile.NamedBlobImage(
    #     title=_(u'Advertisement (Gold-sponsors and above)'),
    #     required=False,
    # )

    # directives.read_permission(notes='cmf.ManagePortal')
    # directives.write_permission(notes='cmf.ManagePortal')
    # notes = RichText(
    #     title=_(u'Secret Notes (only for site-admins)'),
    #     required=False
    # )


@implementer(IRealEstate)
class RealEstate(Container):
    """
    """
