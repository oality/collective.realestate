# -*- coding: utf-8 -*-

from plone.app.layout.viewlets import ViewletBase


class LeadimageViewlet(ViewletBase):

    def render(self):
        self.message = '''<li class="heading" i18n:translate="">
          Simple Viewlet!
        </li>'''
        return self.message
