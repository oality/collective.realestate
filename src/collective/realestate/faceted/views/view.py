# -*- coding: utf-8 -*-
from Products.CMFPlone.utils import safe_unicode
from Products.Five.browser import BrowserView

import json


class MapView(BrowserView):

    def json(self):
        view = self.context.restrictedTraverse('faceted_query')
        brains = view.query(batch=False)
        json = get_json(brains)
        return json


def get_json(brains):
    geo_json = {
        'type': 'FeatureCollection',
    }
    features = []
    for brain in brains:
        obj = brain.getObject()
        if not getattr(obj, 'geolocation', None):
            continue
        latitude = getattr(obj.geolocation, 'latitude', None)
        longitude = getattr(obj.geolocation, 'longitude', None)
        if not latitude and not longitude:
            continue
        title = brain.Title
        description = brain.Description
        # title = getattr(obj, 'title', '')
        # description = getattr(obj, 'description', '')
        feature = {
            'type': 'Feature',
            'properties': {
                'popup': u'<a href="{0}"><h3>{1}</h3><p>{2}</p></a>'.format(
                    obj.absolute_url(),
                    safe_unicode(title),
                    safe_unicode(description)
                )
            },
            'geometry': {
                'type': 'Point',
                'coordinates': [
                    longitude,  # lng
                    latitude   # lat
                ]
            }
        }
        features.append(feature)
    geo_json['features'] = features
    return json.dumps(geo_json)
