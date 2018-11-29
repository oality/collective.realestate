# -*- coding: utf-8 -*-
from collective.realestate import _
from collective.realestate import logger
from datetime import date
from datetime import timedelta
from email.MIMEText import MIMEText
from plone import api
from plone.registry.interfaces import IRegistry
from plone.schema.email import Email
from plone.supermodel import model
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.interfaces.controlpanel import IMailSchema
from Products.statusmessages.interfaces import IStatusMessage
from smtplib import SMTPException
from z3c.form import button
from z3c.form import field
from z3c.form import form
from zope import schema
from zope.component import getUtility


def date_default_value(offset=0):
    return date.today() + timedelta(offset)


def start_default_value():
    return date_default_value()


def end_default_value():
    return date_default_value(7)


class IBookingRequestForm(model.Schema):
    """ Define form fields """

    name = schema.TextLine(
        title=_(u'Your name')
    )
    email = Email(
        title=_(u'Your e-mail'),
        required=True,
    )
    phone = schema.TextLine(
        title=_(u'Your phone number'),
        description=_(u'Your phone will be used only to take contact with you.'),  # noqa
        required=False,
    )
    start = schema.Date(
        title=_(u'Start of booking'),
        defaultFactory=start_default_value,
    )
    end = schema.Date(
        title=_(u'End of booking'),
        defaultFactory=end_default_value,
    )


class BookingRequestForm(form.Form):
    """ Define Form handling

    This form can be accessed as
    http://yoursite/real-estate-id/@@booking-request

    """
    # schema = IBookingRequestForm
    fields = field.Fields(IBookingRequestForm)
    ignoreContext = True

    label = _(u"Request booking")  # noqa
    description = _(u'Form to make request booking')

    @button.buttonAndHandler(u'Send')
    def handleApply(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return

        # Do something with valid data here

        # Set status on this form page
        # (this status message is not bind to the session and does not go thru redirects)
        self.send_message(data)
        self.status = _(u'Your request has been send to the owner')
        self.request.response.redirect(self.context.absolute_url())

    @button.buttonAndHandler(_(u'Cancel'))
    def handleCancel(self, action):
        """User cancelled. Redirect back to the front page.
        """
        self.status = _(u'See you next time!')
        self.request.response.redirect(self.context.absolute_url())

    def generate_mail(self, variables, encoding='utf-8'):
        template = self.context.restrictedTraverse('booking-request-email')
        variables['realestate_url'] = self.context.absolute_url()
        return template(self.context, **variables).encode(encoding)

    def send_message(self, data):
        subject = _(u'Request booking')

        portal = api.portal.get()
        registry = getUtility(IRegistry)
        mail_settings = registry.forInterface(IMailSchema, prefix='plone')
        send_to_address = mail_settings.email_from_address
        from_address = mail_settings.email_from_address
        registry = getUtility(IRegistry)
        encoding = registry.get('plone.email_charset', 'utf-8')
        host = getToolByName(self.context, 'MailHost')

        data['url'] = portal.absolute_url()
        message = self.generate_mail(data, encoding)
        message = MIMEText(message, 'plain', encoding)
        message['Reply-To'] = data['email']

        try:
            # This actually sends out the mail
            host.send(
                message,
                send_to_address,
                from_address,
                subject=subject,
                charset=encoding
            )
        except (SMTPException, RuntimeError), e:
            logger.error(e)
            plone_utils = getToolByName(portal, 'plone_utils')
            exception = plone_utils.exceptionString()
            message = _(u'Unable to send mail: ${exception}',
                        mapping={u'exception': exception})
            IStatusMessage(self.request).add(message, type=u'error')
