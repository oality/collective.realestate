# -*- coding: utf-8 -*-
""" Int Select widget
"""
from collective.realestate import _
from collective.realestate.faceted.widgets.intselect.interfaces import CountableSchemata  # noqa
from collective.realestate.faceted.widgets.intselect.interfaces import DefaultSchemata  # noqa
from collective.realestate.faceted.widgets.intselect.interfaces import DisplaySchemata  # noqa
from collective.realestate.faceted.widgets.intselect.interfaces import LayoutSchemata  # noqa
from eea.facetednavigation.widgets import ViewPageTemplateFile
from eea.facetednavigation.widgets.widget import CountableWidget
from Products.CMFPlone.utils import safeToInt

import operator


def intcompare(a, b):
    return cmp(safeToInt(a), safeToInt(b))


class Widget(CountableWidget):
    """ Widget
    """
    widget_type = 'intselect'
    widget_label = _('Int Select')

    groups = (
        DefaultSchemata,
        LayoutSchemata,
        CountableSchemata,
        DisplaySchemata
    )

    index = ViewPageTemplateFile('widget.pt')

    @property
    def default(self):
        """ Get default values
        """
        default = super(Widget, self).default or u''
        return default.encode('utf-8')

    def query(self, form):
        """ Get value from form and return a catalog dict query
        """
        query = {}
        index = self.data.get('index', '')
        index = index.encode('utf-8', 'replace')
        if not index:
            return query

        if self.hidden:
            value = self.default
        else:
            value = form.get(self.data.getId(), '')

        if not value:
            return query

        query[index] = int(value)
        return query

    def vocabulary(self, **kwargs):
        """ Return data vocabulary
        """
        reverse = safeToInt(self.data.get('sortreversed', 0))
        values = self.catalog_vocabulary()
        mapping = {}

        res = [(val, mapping.get(val, val)) for val in values]
        res.sort(key=operator.itemgetter(1), cmp=intcompare)

        if reverse:
            res.reverse()
        return res
