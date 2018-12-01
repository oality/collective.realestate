# -*- coding: utf-8 -*-
""" Widget
"""
from collective.realestate import _
from collective.realestate.faceted.widgets.intrange.interfaces import DefaultSchemata
from collective.realestate.faceted.widgets.intrange.interfaces import LayoutSchemata
from eea.facetednavigation.widgets import ViewPageTemplateFile
from eea.facetednavigation.widgets.widget import Widget as AbstractWidget


class Widget(AbstractWidget):
    """ Widget
    """
    widget_type = 'intrange'
    widget_label = _('Int range field')

    groups = (DefaultSchemata, LayoutSchemata)
    index = ViewPageTemplateFile('widget.pt')

    @property
    def default(self):
        """ Return default
        """
        default = self.data.get('default', '')
        if not default:
            return ('', '')
        default = default.split('=>')
        if len(default) != 2:
            return ('', '')

        min, max = default
        return (min, max)

    def query(self, form):
        """ Get value from form and return a catalog dict query
        """
        query = {}

        # import ipdb; ipdb.set_trace()
        index = self.data.get('index', '')
        index = index.encode('utf-8', 'replace')
        if not index:
            return query

        if self.hidden:
            min, max = self.default
        else:
            value = form.get(self.data.getId(), '')
            if not value or len(value) != 2:
                return query
            min, max = value

        if not value:
            return query
        # portal_catalog({'price':{'query':[2,1000],'range':'min:max'}})
        if min:
            value = min
            range = 'min'
        elif max:
            value = max
            range = 'max'
        else:
            value = [min, max]
            range = 'min:max'
        query[index] = {'query': value, 'range': range}
        return query
