# -*- coding: utf-8 -*-
""" Widget
"""
from collective.realestate import _
from collective.realestate.faceted.widgets.moreorless.interfaces import DefaultSchemata
from collective.realestate.faceted.widgets.moreorless.interfaces import LayoutSchemata
from eea.facetednavigation.interfaces import ICriteria
from eea.facetednavigation.widgets import ViewPageTemplateFile
from eea.facetednavigation.widgets.widget import Widget as AbstractWidget


class Widget(AbstractWidget):
    """ Widget
    """

    widget_type = "moreorless"
    widget_label = _("More or less field")

    groups = (DefaultSchemata, LayoutSchemata)
    index = ViewPageTemplateFile("widget.pt")

    # @property
    # def css_class(self):
    #     css = super(Widget, self).css_class
    #     css += ' col-xs-12 col-sm-6 col-lg-6 users'
    #     return css

    @property
    def default(self):
        """ Return default
        """
        default = self.data.get("default", "")
        if not default:
            return ""
        return default

    def query(self, form):
        """ Get value from form and return a catalog dict query
        """
        query = {}

        # import ipdb; ipdb.set_trace()
        index = self.data.get("index", "")
        moreorless = self.data.get("moreorless", "")
        index = index.encode("utf-8", "replace")
        value = None
        if not index:
            return query

        if self.hidden:
            value = self.default
        else:
            value = form.get(self.data.getId(), "")

        if not value:
            return query
        # check if there are other criteria with same index
        second_value = None
        second_moreorless = None
        criteria = ICriteria(self.context)
        for cid, criterion in criteria.items():
            if cid in form.keys() and cid != self.data.getId():
                if criterion.index == index:
                    second_value = form.get(cid)
                    second_moreorless = criterion.moreorless

        value = int(value)
        # portal_catalog({'price':{'query':[2,1000],'range':'min:max'}})
        if moreorless == u"more" and not second_value:
            range = "min"
        elif moreorless == u"less" and not second_value:
            range = "max"
        else:
            range = "min:max"
            if second_moreorless == u"more":
                value = [int(second_value), value]

        query[index] = {"query": value, "range": range}
        return query
