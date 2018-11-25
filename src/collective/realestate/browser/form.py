# -*- coding: utf-8 -*-
from collective.realestate import _
from collective.realestate import logger
from email.MIMEText import MIMEText
from plone import api
from plone.registry.interfaces import IRegistry
from plone.schema.email import Email
from plone.supermodel import model
from Products.CMFCore.utils import getToolByName
from smtplib import SMTPException
from z3c.form import button
from z3c.form import field
from z3c.form import form
from zope import schema
from zope.component import getUtility


class IBookingRequestForm(model.Schema):
    """ Define form fields """

    name = schema.TextLine(
        title=_(u'Your name')
    )
    email = Email(
        title=_(u'Your e-mail')
    )


class BookingRequestForm(form.Form):
    """ Define Form handling

    This form can be accessed as
    http://yoursite/real-estate-id/@@booking-request

    """
    # schema = IBookingRequestForm
    fields = field.Fields(IBookingRequestForm)
    ignoreContext = True

    label = _(u"What's your name?")  # noqa
    description = _(u'Simple, sample form')

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

    @button.buttonAndHandler(u"Cancel")
    def handleCancel(self, action):
        """User cancelled. Redirect back to the front page.
        """
        self.status = _(u'See you next time!')
        self.request.response.redirect(self.context.absolute_url())

    def send_message(self, data):
        subject = data.get('subject')

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
        message['Reply-To'] = data['sender_from_address']

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
