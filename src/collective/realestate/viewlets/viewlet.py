# -*- coding: utf-8 -*-
from Acquisition import aq_base
from cgi import escape
from eea.facetednavigation.config import ANNO_FACETED_LAYOUT
from plone import api
from plone.app.layout.viewlets import ViewletBase
from plone.app.layout.viewlets.common import TitleViewlet
from plone.memoize.view import memoize
from Products.CMFPlone.interfaces import IPloneSiteRoot
from Products.CMFPlone.utils import safe_unicode
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.annotation.interfaces import IAnnotations
from zope.component import getMultiAdapter
from zope.i18n import translate


class LeadimageViewlet(ViewletBase):

    def available(self):
        return False

    def index(self):
        return ''


class BookingsViewlet(ViewletBase):
    """ A viewlet which renders files """

    index = ViewPageTemplateFile('bookings.pt')

    def available(self):
        return self.context.is_rent() and not api.user.is_anonymous()

    def get_data(self):
        # import ipdb; ipdb.set_trace()
        dates = []
        brains = api.content.find(context=self.context, portal_type='Booking')
        for brain in brains:
            obj_dates = brain.getObject().get_all_dates()
            dates += obj_dates
        # return json.dumps([date.__str__() for date in dates])
        return [date.__str__() for date in dates]


class GeneralCondViewlet(ViewletBase):

    def index(self):
        key = 'collective.realestate.condition'
        text = api.portal.get_registry_record(key)
        return text if text else ''


class MapViewlet(ViewletBase):

    index = ViewPageTemplateFile('map.pt')

    def available(self):
        if not getattr(self.context, 'layout', '') == 'facetednavigation_view':
            return False
        view_name = IAnnotations(self.context).get(
            ANNO_FACETED_LAYOUT, 'faceted-preview-items')

        if not view_name == 'faceted-map-view':
            return False
        return True


class HeadTitle(TitleViewlet):

    @property
    @memoize
    def page_title(self):
        if (hasattr(aq_base(self.context), 'isTemporary') and
                self.context.isTemporary()):
            # if we are in the portal_factory we want the page title to be
            # "Add fti title"
            portal_types = api.portal.get_tool('portal_types')
            fti = portal_types.getTypeInfo(self.context)
            return translate('heading_add_item',
                             domain='plone',
                             mapping={'itemtype': fti.Title()},
                             context=self.request,
                             default='Add ${itemtype}')

        # If we are on portal root, look up the portal title from registry
        if (IPloneSiteRoot.providedBy(self.context) or
                self.context.id.startswith('bienvenue-')):
            return self.site_title_setting

        context_state = getMultiAdapter((self.context, self.request),
                                        name=u'plone_context_state')
        return escape(safe_unicode(context_state.object_title()))
