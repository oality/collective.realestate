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

import locale


class IRealEstate(model.Schema):
    """ Marker interface and Dexterity Python Schema for RealEstate
    """
    # If you want, you can load a xml model created TTW here
    # and customize it in Python:

    # model.load('real_estate.xml')

    # directives.widget(level=RadioFieldWidget)
    sale_or_rent = schema.Choice(
        title=_(u'Sale or rent?'),
        vocabulary=u'collective.realestate.RealEstateFor',
    )
    type = schema.Choice(
        title=_(u'Type of real estate'),
        vocabulary=u'collective.realestate.RealEstateTypes',
    )

    # text = RichText(
    #     title=_(u'Text'),
    #     required=False
    # )

    persons = schema.Int(
        title=_(u'Number of person(s)'),
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

    price = schema.Float(
        title=_(u'Price'),
        required=False
    )


@implementer(IRealEstate)
class RealEstate(Container):
    """
    """
    def is_rent(self):
        return self.sale_or_rent == 'rent'

    def is_sale(self):
        return self.sale_or_rent == 'sale'

    def get_formatted_price(self, days=7, devise='&euro;'):
        price = self.get_price(days)
        locale.setlocale(locale.LC_ALL, '')
        formatted_price = '{0} {1}'.format(
            locale.currency(float(price), symbol='', grouping=True),
            devise
        )
        return formatted_price

    def get_price(self, days=7):
        if self.is_sale():
            return '{0:.0f}'.format(self.price)
        else:
            return '{0:.2f}'.format(self.price * days)

    def get_low_price(self, days=7):
        return '{0:.2f}'.format(self.price * days)

    def get_high_price(self, days=7):
        return '{0:.2f}'.format(self.price * days)
