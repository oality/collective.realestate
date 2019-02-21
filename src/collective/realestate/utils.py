# -*- coding: utf-8 -*-
from plone import api


def get_first_realestate_obj():
    brain = api.content.find(portal_type='Real estate')
    if len(brain) > 0:
        return brain[0].getObject()
    else:
        return None
